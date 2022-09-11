from typing import List
import docker
import dockerfile
import os
import tarfile
import io

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

    def __init__(self):
        self.client = docker.from_env()
        self.commands = dockerfile.parse_file(os.getcwd() + "/Dockerfile")
        self.required_binaries = []

    def run(self):
        self.parse_dockerfile()

    def get_required_binaries(self, cmd) -> List[str]:
        # print(cmd)
        commands = []
        for command in cmd.value:
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
            bin_apps = [p for p in tar_file.getnames() if "bin" in p]
            print(f"Available binaries: {bin_apps}")


if __name__ == "__main__":
    run_checker = RunChecker()
    run_checker.run()
