from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.md")
version = read_file("VERSION")
requirements = read_requirements("requirements.txt")

setup(
    name = 'pydnevnik',
    version = version,
    author = 'Urufusan',
    author_email = 'urufusan@discord.gg',
    url = 'https://github.com/Urufusan/pydnevnik',
    description = 'A Python library for E-Dnevnik (ocjene.skole.hr)',
    long_description_content_type = "text/markdown",  # If this causes a warning, upgrade your setuptools package
    long_description = long_description,
    license = "GNU Affero General Public License v3",
    packages = find_packages(exclude=["test"]),  # Don't include test directory in binary distribution
    install_requires = requirements,
    python_requires='>=3.9',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
    ]  # Update these accordingly
)
