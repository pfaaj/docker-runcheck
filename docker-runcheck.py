import fileinput
from importlib.resources import path
import sys
from typing import List
import docker
import dockerfile
import os
import tarfile
import io
from rich.console import Console
from rich.table import Table
import shutil


class Binary:
    def __init__(self, name, status):
        self.name = name
        self.status = status


def get_binaries(required_binaries, available_binaries):
    binaries = []
    for bin in required_binaries:
        b = Binary(bin, "missing")
        for available_bin in available_binaries:
            if bin in available_bin:
                b = Binary(bin, "present")
        binaries.append(b)
    return binaries


def print_table(binaries):

    table = Table(title="Missing binaries")
    table.add_column("Binary", justify="right", no_wrap=True)
    table.add_column("Status", justify="right")
    binaries.sort(key=lambda b: b.status)
    for binary in binaries:
        table.add_row(
            "[green]" + binary.name
            if binary.status == "present"
            else "[red]" + binary.name,
            "[green]" + binary.status
            if binary.status == "present"
            else "[red]" + binary.status,
        )

    console = Console()
    console.print(table)


# commands between EOFS are not being properly parsed

# https://stackoverflow.com/questions/39155958/how-do-i-read-a-tarfile-from-a-generator
def generator_to_stream(generator, buffer_size=io.DEFAULT_BUFFER_SIZE):
    class GeneratorStream(io.RawIOBase):
        def __init__(self):
            self.leftover = None

        def readable(self):
            return True

        def readinto(self, b):
            try:
                l = len(b)  # : We're supposed to return at most this much
                chunk = self.leftover or next(generator)
                output, self.leftover = chunk[:l], chunk[l:]
                b[: len(output)] = output
                return len(output)
            except StopIteration:
                return 0  # : Indicate EOF

    return io.BufferedReader(GeneratorStream())


class RunChecker:

    ignore = []

    def preprocess_dockerfile(self, path_dockerfile):
        data = []
        with open(path_dockerfile, "r") as file:
            data = file.readlines()
            in_eof_block = False
            for i, line in enumerate(data):
                if in_eof_block:
                    data[i] = "RUN " + line
                if "<<EOF" in line:
                    print("found EOF")
                    data[i] = ""
                    in_eof_block = True
                elif "EOF" in line:
                    data[i] = ""
                    in_eof_block = False
        with open(path_dockerfile, "w") as file:
            file.writelines(data)

    def __init__(self):
        self.client = docker.from_env()
        self.path_dockerfile = os.getcwd() + "/Dockerfile"
        shutil.copy(self.path_dockerfile, os.getcwd() + "/.Dockerfile")
        self.preprocess_dockerfile(os.getcwd() + "/.Dockerfile")
        self.commands = dockerfile.parse_file(os.getcwd() + "/.Dockerfile")
        self.required_binaries = []
        self.available_binaries = []

    def run(self):
        self.parse_dockerfile()
        print_table(
            get_binaries(
                required_binaries=self.required_binaries,
                available_binaries=self.available_binaries,
            )
        )

    def get_required_binaries(self, cmd) -> List[str]:
        # print(cmd)
        commands = []
        for command in cmd.value:
            print(cmd)
            commands = [c.strip() for c in commands + command.split("&&")]
        command_names = [c.split(" ")[0] for c in commands]
        # print(command_names)
        return command_names

    def parse_dockerfile(self):
        for cmd in self.commands:
            if cmd.cmd == "RUN":
                self.required_binaries += self.get_required_binaries(cmd)
            if cmd.cmd == "FROM":
                print(f"FROM: {cmd.value}")
                if type(cmd.value) is tuple:
                    for i, v in enumerate(cmd.value):
                        if v.casefold() == "as":
                            if i + 1 < len(cmd.value):
                                RunChecker.ignore.append(cmd.value[i + 1])
                self.list_available_binaries(cmd)
                print(f"Required binaries {self.required_binaries}")
                # just for testing the table print, we need available - required

    def list_available_binaries(self, cmd):
        if cmd.value[0] not in RunChecker.ignore:
            images = self.client.images.list(cmd.value[0])
            for image in images:
                print(f"{image} {cmd.value[0]} is available.")
            container = None
            try:
                container = self.client.containers.create(cmd.value[0])
            except docker.errors.ImageNotFound:
                print(f"Pulling image: {cmd.value[0]}...")
                self.client.images.pull(cmd.value[0])
                container = self.client.containers.create(cmd.value[0])

            print("Created container")

            exported = container.export()
            stream = generator_to_stream(exported)
            tar_file = tarfile.open(fileobj=stream, mode="r|*")

            # print(f"Container contents {tar_file.getnames()}")
            self.available_binaries += [p for p in tar_file.getnames() if "bin" in p]
            # print(f"Available binaries: {bin_apps}")


if __name__ == "__main__":
    run_checker = RunChecker()
    run_checker.run()
