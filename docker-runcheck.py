import docker
import dockerfile
import os
import tarfile


class RunChecker:
    ignore = []


if __name__ == "__main__":
    client = docker.from_env()
    docker_cmds = dockerfile.parse_file(os.getcwd() + "/Dockerfile")
    for cmd in docker_cmds:
        if cmd.cmd == "FROM":
            print(f"FROM: {cmd.value}")
            if type(cmd.value) is tuple:
                for i, v in enumerate(cmd.value):
                    if v.casefold() == "as":
                        if i + 1 < len(cmd.value):
                            RunChecker.ignore.append(cmd.value[i + 1])

            if cmd.value[0] not in RunChecker.ignore:
                print(f"Pull image: {cmd.value[0]}")
                container = client.containers.create(cmd.value[0])
                print("Created container")

                exported = container.export()

                print(f"Exported containt filesystem to tar file {exported}")
