
from setuptools import find_namespace_packages, setup


setup(
    name="safetab",
    version="0.0.1",
    packages=find_namespace_packages(exclude=["tests"]),
    include_package_data=True,
    url="https://github.com/opensafely-core/safetab-action",
    description="Command line tool for redaction of small numbers",
    long_description="Command line tool for redaction of small numbers in "
                     "descriptive or contingency tables.",
    license="GPLv3",
    author="OpenSAFELY",
    author_email="tech@opensafely.org",
    python_requires=">=3.7",
    entry_points={"console_scripts": ["safetab=safetab:main"]},
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
)
