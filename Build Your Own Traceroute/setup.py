from setuptools import setup, find_packages

setup(
    name="mytraceroute",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mytraceroute=src.cli:main'
        ]
    },
    include_package_data=True,
    description='A small traceroute learning tool',
)
