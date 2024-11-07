import setuptools

setuptools.setup(
    name="opt-gramformer",
    version="1.0",
    author="Mitchell Shibilski-Unkel",
    author_email="",
    description="Optimized Gramformer",
    long_description="A framework for detecting, highlighting, and correcting grammatical errors on natural language text. Built off the original Gramformer by Prithiviraj Damodaran.",
    url="https://github.com/MitchellShibilski-Unkel/Optimized-Gramformer.git",
    packages=setuptools.find_packages(),
    #install_requires=['transformers', 'sentencepiece==0.1.95', 'python-Levenshtein==0.12.2', 'fuzzywuzzy==0.18.0',  'tokenizers==0.10.2', 'fsspec==2021.5.0', 'lm-scorer==0.4.2', 'errant'],
    install_requires=['transformers', 'sentencepiece', 'python-Levenshtein', 'fuzzywuzzy',  'tokenizers', 'fsspec', 'errant', 'torch],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
)

