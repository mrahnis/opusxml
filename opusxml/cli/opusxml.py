"""
This script prints information from an OPUS XML file.

Examples:
# print some info about an opus xml file in state plane feet
opusxml.exe info opus/2010096o.10o.xml -u sft -s SPC

# convert two xml files to a json file containing the geometries and solution information
opusxml.exe convert  -u sft -s XYZ outfile.json ./examples/opus/2010096o.10o.xml ./examples/opus/JV4124_11132132452.xml

"""

from __future__ import print_function

import os
import sys
import re
import logging
import click

import xml.etree.ElementTree as xml
import fiona
from fiona.crs import from_epsg

from shapely.geometry import Point, mapping

from opusxml import Solution
from opusxml.tools.fips_mapping import NAD83_2011, NAD83_CORS96

# map unit names recognized by pint to names recognized by proj4
unit_mapping = {
    'meter' : 'm',
    'm' : 'm',
    'foot' : 'ft',
    'ft' : 'ft',
    'survey_foot' : 'us-ft',
    'sft' : 'us-ft'
}

def print_dict(info):
    """
    Print a dict
    """
    for k, v in info.items():
        print('{:>24} : {}'.format(k, v))

@click.group()
def cli():
    pass

@click.command()
@click.argument('files', nargs=-1, type=click.Path(exists=True), metavar='FILES')
@click.option('-u', '--unit', metavar='UNIT', type=click.Choice(['meter', 'm', 'foot', 'ft', 'survey_foot', 'sft']), default='m', help="Distance units")
@click.option('-s', '--system', metavar='SYSTEM', type=click.Choice(['UTM', 'SPC', 'XYZ', 'LLA', 'LLH']), default='UTM', help="Coordinate system")
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def info(files, unit, position, verbose):

    if verbose is True:
        loglevel = 2
    else:
        loglevel = 0

    logging.basicConfig(stream=sys.stderr, level=loglevel or logging.INFO)
    logger = logging.getLogger('opusxml')

    for file in files:
        sln = Solution(file)
        print("POSITION")
        print(sln.position(system='XYZ'))
        print("SPC")
        print(sln.plane_coords(unit=unit, system=system))
        print("QUALITY")
        print(sln.data_quality(unit=unit))
        print()

        info = sln.solution_info()
        print('------------------------')
        print("SOLUTION INFO")
        print('------------------------')
        print_dict(info)
        print()

        info = sln.mark_info()
        print('------------------------')
        print("MARK INFO")
        print('------------------------')
        print_dict(info)

@click.command()
@click.argument('outfile', nargs=1, type=click.Path(exists=False), metavar='OUTFILE')
@click.argument('files', nargs=-1, type=click.Path(exists=True), metavar='FILES')
@click.option('-u', '--unit', metavar='UNIT', type=click.Choice(['meter', 'm', 'foot', 'ft', 'survey_foot', 'sft']), default='m', help="Distance units")
@click.option('-s', '--system', metavar='SYSTEM', type=click.Choice(['UTM', 'SPC', 'XYZ', 'LLA', 'LLH']), default='UTM', help="Coordinate system")
@click.option('-f', '--frame', type=click.Choice(['IGS08', 'NAD_83']), default='IGS08', metavar='FRAME', help="Reference frame")
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
def convert(outfile, files, unit, system, frame, verbose):

    if verbose is True:
        loglevel = 2
    else:
        loglevel = 0

    logging.basicConfig(stream=sys.stderr, level=loglevel or logging.INFO)
    logger = logging.getLogger('opusxml')

    # determine the driver for writing to outfile
    ext = str(outfile.split('.')[-1]).lower()
    if ext == 'shp':
        driver = 'ESRI Shapefile'
    elif ext == 'json' or ext == 'geojson':
        driver = 'GeoJSON'
    elif ext == 'dxf':
        driver = 'DXF'
    elif ext == 'dgn':
        driver = 'DGN'
    else:
        logger.error("Cannot write to format: {}".format(ext))
        sys.exit(0)

    # determine crs for writing to outfile and check each file for consistency with respect to zone or reference frame
    if os.getenv('GDAL_DATA') == None:
        logger.warning('GDAL_DATA environment variable must be set in order to output state plane coordinates')
    zones = {}
    ref_frames = {}
    for file in files:
        sln = Solution(file)
        if system in ['UTM', 'SPC']:
            pos = sln.root.find('PLANE_COORD_INFO/PLANE_COORD_SPEC[@TYPE="{}"]'.format(system))
            zones[file] = pos.attrib['ZONE']
            if system == 'UTM':
                crs = {'no_defs': True, 'ellps': 'WGS84', 'proj': 'utm', 'zone': int(zones[file]), 'units': unit_mapping[unit]}
            elif system == 'SPC':
                pattern = re.compile(r'^(\d+)\((\D+)\)$')
                fips, name = pattern.search(zones[file]).groups()
                # 'NAD83(2011)' not in GDAL v 1.x database
                if 'NAD_83(2011)' in sln.ref_frames():
                    try:
                        crs = from_epsg(NAD83_2011[int(fips)][unit])
                    except:
                        logger.error("Unable to get crs for FIPS:{}, NAD83(2011). Check your GDAL installation.".format(fips))
                else:
                    try:
                        crs = from_epsg(NAD83_CORS96[int(fips)][unit])
                    except:
                        logger.error("Unable to get crs for FIPS:{}, NAD83(CORS96).".format(fips))
        elif system in ['LLA', 'LLH', 'XYZ']:
            pos = sln.root.xpath('POSITION[starts-with(REF_FRAME/text(), "{}")]'.format(frame))
            ref_frame = pos[0].xpath('REF_FRAME/text()')
            ref_frames[file] = ref_frame[0]
            if frame == 'NAD_83':
                datum, ellps = ('NAD83', 'GRS80')
            elif frame == 'IGS08':
                datum, ellps = ('WGS84', 'WGS84')
            if system in ['LLA', 'LLH']:
                proj = 'longlat'
            elif system == 'XYZ':
                proj = 'geocent'
            crs = {'no_defs': True, 'ellps': ellps, 'datum': datum, 'proj': proj, 'units': unit_mapping[unit]}

    zones_set = set(list(zones.values()))
    frames_set = set(list(ref_frames.values()))
    if len(zones_set) > 1:
        logger.error("Found more than one UTM or SPC zone in fileset")
        logger.info("Unique zones: {}".format(zones_set))
        logger.info(print_dict(zones))
        sys.exit("Output file not written")
    if len(frames_set) > 1:
        logger.error("Found more than one reference frame in fileset")
        logger.info("Unique reference frames: {}".format(frames_set))
        logger.info(print_dict(ref_frames))
        sys.exit("Output file not written")

    properties_schema = {
        'SID':'str',
        'SOLUTION_TIME':'str',
        'OBSERVATION_TIME_START':'str',
        'OBSERVATION_TIME_END':'str',
        'CONTRIBUTOR_EMAIL':'str',
        'RINEX_FILE':'str',
        'EPHEMERIS_FILE_TYPE':'str',
        'ANTENNA_NAME':'str',
        'ANTENNA_ARP_HEIGHT':'float',
    }

    with fiona.open(outfile, 'w',
                    crs=crs,
                    driver=driver,
                    schema={'geometry': 'Point', 'properties': properties_schema}
                   ) as sink:

        for file in files:
            sln = Solution(file)
            if system in ['LLA', 'LLH', 'XYZ']:
                x, y, z = sln.position(system=system, ref_frame=ref_frames[file], unit=unit)
            elif system in ['UTM', 'SPC']:
                x, y, z = sln.plane_coords(system=system, unit=unit)
            point = Point(x.magnitude, y.magnitude, z.magnitude)
            sink.write({
                'properties': sln.solution_info(),
                'geometry': mapping(point)
            })

cli.add_command(info)
cli.add_command(convert)
