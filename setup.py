import sys

import setuptools

requires = [
    # crypto
    "base58",
    "binary-helpers",
    "coincurve",
    # client
    "requests >= 2.19.1",
    "backoff >= 1.6.0",
    "flatten_dict >= 0.3.0",
    # portal
    "click >= 8.1.2",
]

lint_require = [
    "black",
    "flake8",
    "flake8-isort",
    "flake8-debugger",
    "flake8-quotes",
]

tests_require = [
    "pytest-mock",
    "pytest-responses",
    "pytest>=3.6.1",
    "pytest-cov>=2.5.1",
]

extras_require = {"dev": requires + tests_require + lint_require}

setup_requires = ["pytest-runner"] if {"pytest", "test", "ptr"}.intersection(sys.argv) else []

setuptools.setup(
    name="portal",
    description="Portal between Ark's Ecosystems",
    version="0.1.0",
    author="deadlock",
    author_email="consol3@protonmail.com",
    url="https://github.com/deadlock-delegate/portal",
    package_dir={"": "src"},
    # packages=["portal", "portal_client", "portal_crypto"],
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=requires,
    extras_require=extras_require,
    tests_require=tests_require,
    setup_requires=setup_requires,
)
