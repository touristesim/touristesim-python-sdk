from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="touristesim-python-sdk",
    version="1.0.0",
    author="Tourist eSIM",
    author_email="developers@touristesim.net",
    description="Official Python SDK for Tourist eSIM Partner API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/touristesim/touristesim-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.950",
        ],
    },
    keywords=["esim", "touristesim", "api", "sdk", "travel", "mobile", "data-plan", "international"],
)
