from __future__ import annotations

from collections import OrderedDict
import logging

from lxml import etree
import pint

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Solution:
    def __init__(self, filename: str):
        tree = etree.parse(filename)
        self.root = tree.getroot()

    def solution_info(self) -> OrderedDict:
        """
        Return a dict containing information about the solution.
        """
        ureg = pint.UnitRegistry()
        info = OrderedDict([
            ('SID', self.root.get('SID')),
            ('SOLUTION_TIME', self.root.find('SOLUTION_TIME').text),
            ('OBSERVATION_TIME_START', self.root.find('OBSERVATION_TIME').get('START')),
            ('OBSERVATION_TIME_END', self.root.find('OBSERVATION_TIME').get('END')),
            ('CONTRIBUTOR_EMAIL', self.root.find('CONTRIBUTOR/EMAIL').text),
            ('RINEX_FILE', self.root.find('DATA_SOURCES/RINEX_FILE').text),
            ('EPHEMERIS_FILE_TYPE', self.root.find('DATA_SOURCES/EPHEMERIS_FILE').get('TYPE')),
            ('ANTENNA_NAME', self.root.find('DATA_SOURCES/ANTENNA/NAME').text),
            ('ANTENNA_ARP_HEIGHT', self.root.find('DATA_SOURCES/ANTENNA/ARP_HEIGHT').text),
            # Using a Quanity object in pint will make fiona unhappy
            #('ANTENNA_ARP_HEIGHT', self.root.find('DATA_SOURCES/ANTENNA/ARP_HEIGHT').text * ureg(self.root.find('DATA_SOURCES/ANTENNA/ARP_HEIGHT').get('UNIT'))),
        ])
        return info

    def mark_info(self) -> OrderedDict:
        """
        Returns a dict containing information about the mark.
        """
        info = OrderedDict()
        elems = ['PID', 'DESIGNATION', 'STAMPING', 'MONUMENT_TYPE', 'MONUMENT_DESC', 'STABILITY', 'DESCRIPTION']
        for e in elems:
            try:
                path = 'MARK_METADATA/' + e
                info[e] = self.root.find('{}'.format(path)).text
            except:
                info[e] = 'None'
        return info

    def data_quality(
        self,
        unit: str = 'm'
    ) -> tuple[list[float], float, list[int], list[int]]:
        """
        Extract the information from an OPUS XML file DATA_QUALITY element, and return it in the desired units.

        Parameters
        ----------
        unit (str) : distance units of the returned coordinate, valid values are 'm' or 'sft'.

        Returns
        -------
        accuracy (float Quantity array) : array of Quanity contining x,y,z coordinate accuracies.
        rms (float Quantity) : the RMS value
        used (int array) : array of observations [total, used]
        fixed (int array) : array of observation ambiguities [total, fixed]
        """
        quality = self.root.find('DATA_QUALITY')

        ureg = pint.UnitRegistry()
        accuracy_lat = float(quality.find('ACCURACY/LAT').text) * ureg(quality.find('ACCURACY').get('UNIT'))
        accuracy_long = float(quality.find('ACCURACY/LONG').text) * ureg(quality.find('ACCURACY').get('UNIT'))
        accuracy_el_height = float(quality.find('ACCURACY/EL_HEIGHT').text) * ureg(quality.find('ACCURACY').get('UNIT'))

        accuracy_src = [accuracy_long, accuracy_lat, accuracy_el_height]
        accuracy = [c.to(unit) for c in accuracy_src]

        rms_src = float(quality.find('RMS').text) * ureg(quality.find('RMS').get('UNIT'))
        rms = rms_src.to(unit)

        used = [int(quality.find('PERCENT_OBS_USED').get('TOTAL')), int(quality.find('PERCENT_OBS_USED').get('USED'))]
        fixed = [int(quality.find('PERCENT_AMB_FIXED').get('TOTAL')), int(quality.find('PERCENT_AMB_FIXED').get('FIXED'))]

        return accuracy, rms, used, fixed

    def plane_coords(
        self,
        system: str = 'UTM',
        unit: str = 'm'
    ) -> list[float]:
        """
        Extract the coordinate from an OPUS XML file PLANE_COORD_SPEC elements, and return it in the desired units and coordinate spec type.

        Parameters
        ----------
        system (str) : coordinate projection of the returned coordinate, valid values are 'UTM' or 'SPC'.
        unit (str) : distance units of the returned coordinate, valid values are 'm', 'ft' or 'sft'.

        Returns
        -------
        coords (float Quantity array) : x,y,z coordinates as array of pint Quantity.
        """
        ureg = pint.UnitRegistry()
        try:
            pcs = self.root.find('PLANE_COORD_INFO/PLANE_COORD_SPEC[@TYPE="{}"]'.format(system))
        except:
            logger.error("Unable to find a {} position".format(system))

        e_src = float(pcs.find('EASTING').text) * ureg(pcs.find('EASTING').get('UNIT'))
        n_src = float(pcs.find('NORTHING').text) * ureg(pcs.find('NORTHING').get('UNIT'))
        h_src = float(self.root.find('ORTHO_HGT').text) * ureg(self.root.find('ORTHO_HGT').get('UNIT'))

        coords_src = [e_src, n_src, h_src]
        coords = [c.to(unit) for c in coords_src]

        return coords

    def position(
        self,
        system='LLA',
        ref_frame='NAD_83(2011)',
        unit='m'
    ) -> list[float]:
        """
        Extract the coordinate from an OPUS XML file POSITION elements, and return it in the desired units and coordinate spec type.

        Parameters
        ----------
        system (str) : coordinate projection of the returned coordinate, valid values are 'LLA', 'LLH', or 'XYZ'.
        ref_frame (str) : the reference frame to select, OPUS currently offers NAD_83(2011) and IGS08.
        unit (str) : distance units of the returned coordinate, valid values are 'm', 'ft' or 'sft'.

        Returns
        -------
        coords (float Quantity array) : array of pint Quantity containing ellipsoidal coordinates (LLA or LLH), or rectilinear XYZ coordinates.
        """
        ureg = pint.UnitRegistry()
        try:
            position = self.root.find('POSITION[REF_FRAME="{}"]'.format(ref_frame))
        except:
            logger.error("Unable to find a position with reference frame: {}".format(ref_frame))

        if system in ['LLA', 'LLH']:
            lat_d = int(position.find('COORD_SET/ELLIP_COORD/LAT/DEGREES').text) * ureg('arcdeg')
            lat_m = int(position.find('COORD_SET/ELLIP_COORD/LAT/MINUTES').text) * ureg('arcmin')
            lat_s = float(position.find('COORD_SET/ELLIP_COORD/LAT/SECONDS').text) * ureg('arcsec')
            lon_d = int(position.find('COORD_SET/ELLIP_COORD/EAST_LONG/DEGREES').text) * ureg('arcdeg')
            lon_m = int(position.find('COORD_SET/ELLIP_COORD/EAST_LONG/MINUTES').text) * ureg('arcmin')
            lon_s = float(position.find('COORD_SET/ELLIP_COORD/EAST_LONG/SECONDS').text) * ureg('arcsec')

            lat = lat_d + lat_m + lat_s
            lon = lon_d + lon_m + lon_s
            if lon.magnitude > 180:
                lon = lon - 360 * ureg('arcdeg')

            if system == 'LLA':
                h_src = float(position.find('COORD_SET/ELLIP_COORD/EL_HEIGHT').text) * ureg(position.find('COORD_SET/ELLIP_COORD/EL_HEIGHT').get('UNIT'))
            elif system == 'LLH':
                h_src = float(self.root.find('ORTHO_HGT').text) * ureg(self.root.find('ORTHO_HGT').get('UNIT'))
            h = h_src.to(unit)

            return [lon, lat, h]
        elif system == 'XYZ':
            X = float(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="X"]').text) * ureg(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="X"]').get('UNIT'))
            Y = float(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="Y"]').text) * ureg(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="Y"]').get('UNIT'))
            Z = float(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="Z"]').text) * ureg(position.find('COORD_SET/RECT_COORD/COORDINATE[@AXIS="Z"]').get('UNIT'))

            coords_src = [X, Y, Z]
            coords = [c.to(unit) for c in coords_src]

            return coords
        else:
            logger.error("{} is not an accepted value for system".format(system))
            raise

    def ref_frames(self) -> str:
        ref_frames = self.root.xpath('//REF_FRAME/text()')
        return ref_frames
