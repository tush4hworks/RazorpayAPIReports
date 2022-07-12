import os

from pkg_resources import parse_requirements
from setuptools import setup, find_packages

version = '1.0'
lib_name = "razorpay-transactions-summary"


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


resources = package_files('razorpay_transactions/images')

with open('requirements.txt') as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in parse_requirements(requirements_txt)
    ]

setup(
    name=lib_name,
    version=version,
    description='Automate Reports Generation',

    author_email='tsharma@cloudera.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7'
    ],

    keywords='razorpay payments summary description filter',
    packages=find_packages(
    ),
    package_data={'': resources},
    python_requires='>=3.7',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['razorpay-transactions-summary=razorpay_transactions.driver:main'],
    }
)
