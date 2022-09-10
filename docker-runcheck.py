import docker
import dockerfile
import os
import tarfile
import io

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

    def run(self):
        self.parse_dockerfile()

    def parse_dockerfile(self):
        for cmd in self.commands:
            if cmd.cmd == "FROM":
                print(f"FROM: {cmd.value}")
                if type(cmd.value) is tuple:
                    for i, v in enumerate(cmd.value):
                        if v.casefold() == "as":
                            if i + 1 < len(cmd.value):
                                RunChecker.ignore.append(cmd.value[i + 1])
                self.list_available_binaries(cmd)

    def list_available_binaries(self, cmd):
        if cmd.value[0] not in RunChecker.ignore:
            print(f"Pull image: {cmd.value[0]}")
            container = self.client.containers.create(cmd.value[0])
            print("Created container")

            exported = container.export()
            stream = generator_to_stream(exported)
            tar_file = tarfile.open(fileobj=stream, mode="r|*")

            # print(f"Container contents {tar_file.getnames()}")
            bin_apps = [p for p in tar_file.getnames() if "bin" in p]
            print(f"/usr/bin: {bin_apps}")


if __name__ == "__main__":
    run_checker = RunChecker()
    run_checker.run()
