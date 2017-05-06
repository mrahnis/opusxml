========
OPUSXML
========

OPUSXML is a Python library to read OPUSXML files produced by the Online Positioning User Service (OPUS_) hosted by the National Geodetic Survey. It prints information from OPUSXML files and converts them to formats supported by GDAL.

.. image:: https://travis-ci.org/mrahnis/opusxml.svg?branch=master
    :target: https://travis-ci.org/mrahnis/opusxml

.. image:: https://ci.appveyor.com/api/projects/status/github/mrahnis/opusxml?svg=true
	:target: https://ci.appveyor.com/api/projects/status/github/mrahnis/opusxml?svg=true

.. image:: https://readthedocs.org/projects/opusxml/badge/?version=latest
	:target: http://opusxml.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

Dependencies
============

OPUSXML 0.0.0 depends on:

* `Python 2.7 or 3.x`_
* lxml_
* Click_
* pint_
* shapely_
* fiona_

Installation
============

To install from the source distribution execute the setup script in the opusinfo directory:

	$python setup.py install

Windows users just getting started may choose to install a Python distribution to obtain the requirements:

* Install Anaconda from `Continuum Analytics`_ or Canopy from `Enthought`_

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