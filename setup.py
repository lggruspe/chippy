import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="chippy-emu",
    version="0.1.1",
    author="Levi Gruspe",
    author_email="mail.levig@gmail.com",
    description="Chip-8 interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lggruspe/chippy",
    packages=setuptools.find_packages(),
    package_data={
        "chippy": ["roms/*"],
    },
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
    install_requires=["pygame"],
    python_requires=">=3.7",
)
