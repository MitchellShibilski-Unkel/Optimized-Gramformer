import setuptools

setuptools.setup(
    name="optgramformer",
    version="2.2",
    author="Mitchell Shibilski-Unkel",
    author_email="",
    description="Optimized Gramformer",
    long_description="A framework for detecting, highlighting, and correcting grammatical errors on natural language text. Built off the original Gramformer by Prithiviraj Damodaran.",
    url="https://github.com/MitchellShibilski-Unkel/Optimized-Gramformer.git",
    packages=setuptools.find_packages(),
    install_requires=['transformers', 'sentencepiece', 'python-Levenshtein', 'fuzzywuzzy',  'tokenizers', 'fsspec', 'errant', 'torch'],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
)

