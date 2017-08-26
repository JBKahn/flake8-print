# coding: utf-8

from __future__ import with_statement
from setuptools import setup


def get_version(fname='flake8_print.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


install_requires = ['flake8>=1.5', 'six', 'pycodestyle']

test_requires = ['pytest', 'flake8>=1.5', 'pycodestyle']

setup(
    name='flake8-print',
    version=get_version(),
    description="print statement checker plugin for flake8",
    long_description=get_long_description(),
    keywords='flake8 print',
    author='Joseph Kahn',
    author_email='josephbkahn@gmail.com',
    url='https://github.com/jbkahn/flake8-print',
    license='MIT',
    py_modules=['flake8_print'],
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'T = flake8_print:PrintChecker',
        ],
    },
    install_requires=install_requires,
    tests_require=test_requires,
    setup_requires=['pytest-runner'],
    test_suite="nose.collector",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
