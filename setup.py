from setuptools import setup, find_packages

setup(
    name="untold-lang",
    version="2.2.0",
    description="Untold Lang v2.2.0 — The Language Without Limits",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Antony Jude",
    author_email="thedrjude@github.com",
    url="https://github.com/thedrjude/untold-lang",
    project_urls={
        "Documentation": "https://thedrjude.github.io/untold-lang/",
        "Source": "https://github.com/thedrjude/untold-lang",
    },
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
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
    ],
    include_package_data=True,
)