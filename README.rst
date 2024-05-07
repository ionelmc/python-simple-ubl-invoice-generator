========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |github-actions| |coveralls| |codecov|
    * - package
      - |version| |wheel| |supported-versions| |supported-implementations| |commits-since|

.. |github-actions| image:: https://github.com/ionelmc/python-simple-ubl-invoice-generator/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/ionelmc/python-simple-ubl-invoice-generator/actions

.. |coveralls| image:: https://coveralls.io/repos/github/ionelmc/python-simple-ubl-invoice-generator/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://coveralls.io/github/ionelmc/python-simple-ubl-invoice-generator?branch=main

.. |codecov| image:: https://codecov.io/gh/ionelmc/python-simple-ubl-invoice-generator/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://app.codecov.io/github/ionelmc/python-simple-ubl-invoice-generator

.. |version| image:: https://img.shields.io/pypi/v/simple-ubl-invoice-generator.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/simple-ubl-invoice-generator

.. |wheel| image:: https://img.shields.io/pypi/wheel/simple-ubl-invoice-generator.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/simple-ubl-invoice-generator

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/simple-ubl-invoice-generator.svg
    :alt: Supported versions
    :target: https://pypi.org/project/simple-ubl-invoice-generator

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/simple-ubl-invoice-generator.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/simple-ubl-invoice-generator

.. |commits-since| image:: https://img.shields.io/github/commits-since/ionelmc/python-simple-ubl-invoice-generator/v0.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/ionelmc/python-simple-ubl-invoice-generator/compare/v0.3.0...main

.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install simple-ubl-invoice-generator

You can also install the in-development version with::

    pip install https://github.com/ionelmc/python-simple-ubl-invoice-generator/archive/main.zip

Documentation
=============

Usage: ``sublig [-h] [--template TEMPLATE] [--output-path OUTPUT_PATH] [--verbose] [--version] CONFIG``

Command description.

positional arguments:
  ``CONFIG``                Invoice TOML config file.

options::

  -h, --help            show this help message and exit
  --template TEMPLATE, -t TEMPLATE
                        Invoice UBL Jinja2 template. Default: ???/site-packages/simple_ubl_invoice_generator/template.xml
  --output-path OUTPUT_PATH, -o OUTPUT_PATH
                        Output path for resulting invoice XML files. Default: $CWD
  --verbose, -v
  --version             show program's version number and exit

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
