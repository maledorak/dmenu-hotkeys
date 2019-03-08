from setuptools import find_packages, setup


def read(f):
    return open(f, "r", encoding="utf-8").read()


setup(
    name="dmenu-hotkeys",
    version="1.0.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    test_suite="runtests.runtests",
    include_package_data=True,
    description="Hotkeys for variety programs in dmenu style",
    long_description=read("README.md"),
    url="https://github.com/maledorak/dmenu-hotkeys",
    author="Mariusz 'Maledorak' Korzekwa",
    python_requires=">=3.5",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'dmenu-hotkeys=dmenu_hotkeys:main',
        ],
    }
)
