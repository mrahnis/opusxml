========
OPUSXML
========

OPUSXML is a Python library to read OPUSXML files produced by the Online Positioning User Service (OPUS_) hosted by the National Geodetic Survey. It prints information from OPUSXML files and converts them to formats supported by GDAL.

.. image:: https://github.com/mrahnis/opusxml/workflows/Python%20package/badge.svg
    :target: https://github.com/mrahnis/opusxml/actions?query=workflow%3A%22Python+package%22
    :alt: Python Package

.. image:: https://github.com/mrahnis/opusxml/workflows/Conda%20package/badge.svg
    :target: https://github.com/mrahnis/opusxml/actions?query=workflow%3A%22Conda+package%22
    :alt: Conda Package

.. image:: https://readthedocs.org/projects/opusxml/badge/?version=latest
    :target: http://opusxml.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Installation
============

.. image:: https://img.shields.io/pypi/v/opusxml.svg
    :target: https://pypi.python.org/pypi/opusxml/

.. image:: https://anaconda.org/mrahnis/opusxml/badges/version.svg
    :target: https://anaconda.org/mrahnis/opusxml

To install from the Python Package Index:

.. code:: console

    pip install opusxml

To install from Anaconda Cloud:

If you are starting from scratch the first thing to do is install the Anaconda Python distribution, add the necessary channels to obtain the dependencies and install opusxml.

.. code:: console

    conda config --append channels conda-forge
    conda install opusxml -c mrahnis

To install from the source distribution execute the setup script in the opusxml directory:

.. code:: console

    python setup.py install

Examples
========

TODO

License
=======

BSD

Documentation
=============

Latest `html`_

.. _OPUS: http://www.ngs.noaa.gov/OPUS/

.. _`Python 2.7 or 3.x`: http://www.python.org
.. _lxml: http://lxml.de
.. _Click: http://click.pocoo.org
.. _pint: http://pint.readthedocs.io/
.. _shapely: https://github.com/Toblerity/Shapely
.. _fiona: https://github.com/Toblerity/Fiona

.. _Continuum Analytics: http://continuum.io/
.. _Enthought: http://www.enthought.com
.. _release page: https://github.com/mrahnis/opusxml/releases

.. _html: http://opusxml.readthedocs.org/en/latest/