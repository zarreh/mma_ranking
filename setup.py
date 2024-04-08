from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # list your project's dependencies here
        # e.g., 'requests', 'pandas>=1.0.0',
    ],
    # if your package has scripts that should be made available to the command line
    entry_points={
        'console_scripts': [
            'your_script_name = your_module:main_function_name',
        ],
    },
)
