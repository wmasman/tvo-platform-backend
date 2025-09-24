from setuptools import find_packages, setup

setup(
    name="directus_client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests==2.32.3", "pyyaml==6.0.2"],
    extras_require={
        "dev": [
            "pytest",
            "requests_mock",
            "black",
            "flake8",
            "mypy",
            "isort",
        ],
    },
    python_requires=">=3.10",
)
