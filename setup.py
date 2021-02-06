import setuptools


with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

with open("djist/__init__.py", "r", encoding="utf-8") as meta:
    meta_info = meta.read()


def get_meta_info(info: str):
    for line in meta_info.splitlines():
        if line.startswith(f"__{info}__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version or author string.")


setuptools.setup(
    name="djist",
    version=get_meta_info("version"),
    author=get_meta_info("author"),
    author_email="buggyfirmware@protonmail.com",
    description="Django-inspired static templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llelse/djist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["djist = djist:main"]},
    install_requires=[
        "python-dateutil",
        "pyparsing",
    ],
)
