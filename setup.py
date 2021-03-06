#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='json_annotate',
    version='0.1.2',
    description="..",
    long_description=readme + '\n\n' + history,
    author="Aron Culotta",
    author_email='aronwc@gmail.com',
    url='https://github.com/aronwc/json_annotate',
    packages=[
        'json_annotate',
    ],
    package_dir={'json_annotate':
                 'json_annotate'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='json_annotate',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'json-annotate = json_annotate.main:main',
        ],
    },

    test_suite='tests',
    tests_require=test_requirements
)
