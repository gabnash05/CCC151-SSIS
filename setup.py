from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="CCC151_SSIS",
    version="0.1.0",
    packages=find_packages(where="src"),  # Assumes your code is in 'src/'
    package_dir={"": "src"},  # Set the package directory
    install_requires=required,  # Install dependencies from requirements.txt
)