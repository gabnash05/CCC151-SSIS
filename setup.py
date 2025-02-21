from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = [line.strip() for line in f.readlines() if not line.startswith("-e")]

setup(
    name="CCC151_SSIS",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"}, 
    install_requires=required,
)
