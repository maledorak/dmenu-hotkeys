#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'importlib_resources>=1.0.0',
    'pathlib2'
]

setup_requirements = [ ]

test_requirements = [
    "mock",
    "coverage"
]

setup(
    author="Mariusz Korzekwa",
    author_email='maledorak@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Your hotkeys for various apps in 'dmenu' style.",
    entry_points={
        'console_scripts': [
            'dmenu_hotkeys=dmenu_hotkeys.cli:main',
        ],
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dmenu_hotkeys',
    name='dmenu_hotkeys',
    packages=find_packages(include=['dmenu_hotkeys']),
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    url='https://github.com/maledorak/dmenu_hotkeys',
    version='1.1.0',
    zip_safe=False,
)
