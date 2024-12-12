from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crisiscore-processor",
    version="0.1.0",
    author="CrisisCore Systems",
    author_email="crisiscore.systems@proton.me",
    description="A professional-grade image processing suite with cyberpunk aesthetics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrisisCore-Systems/Image-processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=11.0.0",
        "tqdm>=4.65.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "crisiscore-processor=crisiscore.cli:main",
        ],
    },
)
