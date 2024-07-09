import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_requirements(requirements_file):
    with open(requirements_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            package = line.strip()
            if package:
                install(package)


if __name__ == "__main__":
    requirements_file = "requirements.txt"
    install_requirements(requirements_file)
