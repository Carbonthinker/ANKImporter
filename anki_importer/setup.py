from setuptools import setup, find_packages

setup(
    name="anki-importer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'anki-importer=anki_importer.__main__:main',
        ],
    },
    author="Barthélémy Coquoz",
    author_email="cobarth2@gmail.com",
    description="A tool to import flashcards into Anki",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Carbonthinker/ANKImporter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
) 