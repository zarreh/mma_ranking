from setuptools import find_packages, setup

# Read requirements.txt and use its contents for the install_requires option
with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="mma_ranking",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "mma_ranking = mma_app.scripts.main:main",
        ],
    },
    author="Ali Zarreh",
    author_email="ali@zarreh.ai",
    description="A Python package for MMA ranking and statistics analysis",
    keywords="mma ranking sports",
    url="http://app.zarreh.ai/mma_app",  # Optional project URL
)
