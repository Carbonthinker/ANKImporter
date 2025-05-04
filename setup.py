from setuptools import setup, find_packages

setup(
    name="anki_importer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'anki-importer=anki_importer.app:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to import flashcards into Anki",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/anki_importer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
) 