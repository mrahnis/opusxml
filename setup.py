from os import path
from setuptools import setup, find_packages


for line in open('opusxml/__init__.py', 'r'):
    if line.find("__version__") >= 0:
        version = line.split("=")[1].strip()
        version = version.strip('"')
        version = version.strip("'")
        continue

with open('VERSION.txt', 'w') as fp:
    fp.write(version)

current_directory = path.abspath(path.dirname(__file__))
with open(path.join(current_directory, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(name='opusxml',
      version=version,
      author='Michael Rahnis',
      author_email='mike@topomatrix.com',
      description='Python library to read and convert OPUSXML files',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/mrahnis/opusxml',
      license='BSD',
      packages=find_packages(),
      install_requires=[
          'lxml','click','pint','shapely','fiona'
      ],
      entry_points='''
          [console_scripts]
          opusxml=opusxml.cli.opusxml:cli
      ''',
      keywords='cross-section, topography, survey',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: GIS'
      ])
