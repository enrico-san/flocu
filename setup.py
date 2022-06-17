from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name = 'leo',
    version = '0.0.1',
    author = 'Enrico Santoemma',
    author_email = 'enrico.santoemma@gmail.com',
    license = 'MIT',
    description = 'A command line tool to manage in-context documentation',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com',
    py_modules = ['leo', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        leo=leo:cli
    '''
)