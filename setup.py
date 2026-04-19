from setuptools import setup, find_packages

setup(
    name="untold-lang",
    version="0.1.0",
    description="Untold Lang — The Language Without Limits",
    author="Antony Jude",
    author_email="thedrjude@github.com",
    url="https://github.com/thedrjude/untold-lang",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "untold=cli.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)