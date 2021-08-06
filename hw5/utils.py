import os
import time


def run(cmd):
    print(f'[{time.strftime("%c")}] ' + cmd)
    os.system(cmd)


def docker_run(image, cmd):
    run(f"docker run -it --rm --security-opt label=disable -v $PWD:/app "
        f"-w /app {image} {cmd}")


def googleDownload(id):
    docker_run('docker.io/library/python:3.9',
               'bash -c "pip install gdown && '
               f'gdown https://drive.google.com/uc?id={id}"')


def docker_build(image, dockerfile):
    run(f"docker build -t {image} . -f {dockerfile}")
