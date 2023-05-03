from setuptools import setup, find_packages

VERSION = "0.0.1"

INSTALL_REQUIRES = (
    "Pillow",
    "pikepdf"
)
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
]

setup(
    name="pic2pdf",
    version=VERSION,
    author="mashu3",
    description="This program convert an entire directory of images into a single PDF file.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="image pdf converter",
    url="https://github.com/mashu3/pic2pdf",
    license='MIT',
    package_dir={"": "src"},
    py_modules=["pic2pdf"],
    packages = find_packages("src"),
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "pic2pdf=pic2pdf:main",
        ]
    }
)