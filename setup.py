from setuptools import setup, find_packages


# Parse the version from the shapely module
for line in open('opusxml/__init__.py', 'r'):
    if line.find("__version__") >= 0:
        version = line.split("=")[1].strip()
        version = version.strip('"')
        version = version.strip("'")
        continue

#open('VERSION.txt', 'wb').write(bytes(version, 'UTF-8'))
with open('VERSION.txt', 'w') as fp:
    fp.write(version)


setup(name='opusxml',
	version=version,
	author='Michael Rahnis',
	author_email='michael.rahnis@fandm.edu',
	description='Python library to read and convert OPUSXML files.',
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
	]
)

