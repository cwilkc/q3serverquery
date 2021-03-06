import setuptools

script_version = '0.2'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='q3serverquery',
    version=script_version,
    author='Chris Wilkins',
    author_email='cbw182@gmail.com',
    description='A library to query Quake 3 master servers and game servers.',
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: MIT License",
        "Operating System :: OS Independent"
    ],
)