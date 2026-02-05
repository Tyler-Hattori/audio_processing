from pathlib import Path
import re
from setuptools import setup, find_packages

# setup.py - packaging script for setuptools
# Edit metadata, requirements, and package/module names as needed.

HERE = Path(__file__).parent

def read_readme():
    readme_file = HERE / "README.md"
    if readme_file.exists():
        return readme_file.read_text(encoding="utf-8")
    return ""

def read_version(package_dir: str):
    init_path = HERE / package_dir / "__init__.py"
    if not init_path.exists():
        return "0.0.0"
    content = init_path.read_text(encoding="utf-8")
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
    return match.group(1) if match else "0.0.0"

# ---- User-editable metadata ----
PACKAGE_NAME = "guitar_processing"      # pip package name
PACKAGE_DIR = "guitar_processing"            # top-level python package directory
AUTHOR = "Tyler Hattori"
AUTHOR_EMAIL = "tylerwhattori@gmail.com"
DESCRIPTION = "Contains modules used for (1) adding audio effects to raw audio, (2) noise cancellation, (3) source separation, and (4) estimating a filter to match a guitar from a given song."
URL = "https://github.com/Tyler-Hattori/audio_processing"
LICENSE = "uhhhhhh"
PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = [
    "numpy",
    "padasip",
    "matplotlib",
    "scipy",
    "plotly",
    # "requests>=2.25.1",
]
EXTRAS_REQUIRE = {
    "dev": [
        "pytest",
        "flake8",
    ],
}
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
ENTRY_POINTS = {
    # "console_scripts": [
    #     "your-cmd=your_package.module:main",
    # ],
}

# ---- End editable section ----

setup(
    name=PACKAGE_NAME,
    version=read_version(PACKAGE_DIR),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=URL,
    license=LICENSE,
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=CLASSIFIERS,
    entry_points=ENTRY_POINTS,
)