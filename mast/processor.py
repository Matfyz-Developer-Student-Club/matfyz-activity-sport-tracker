from math import radians, cos, sin, asin, sqrt
import xml.etree.ElementTree as ET
from pathlib import Path
import os
from re import findall
import logging


class GPXProcessor(object):
    EARTH_RADIUS = 6378
    LANDING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'landing')
    XML_SUFFIX = '.xml'
    __TRKSEG_ELM = 'trkseg'
    __TRKPT_ELM = 'trkpt'

    def __init__(self):
        super().__init__()

    def process_input_data(self) -> str:
        """
        Purpose of this method is to iterate over each .xml file
        within landing layer, load its content and fetch all
        coordinates in order to calculate total distance in Km.
        """

        output_buffer = []
        try:
            for input_file in os.listdir(self.LANDING_DIR):
                tree = ET.parse(Path(os.path.join(self.LANDING_DIR, input_file)).with_suffix(self.XML_SUFFIX))
                root = tree.getroot()

                # Find the child element of tracking point including namespace
                trk = findall('\{.*\}.*', root[1].tag)
                # Cut of namespace prefix
                namespace = trk[0][:-3]

                activity = (root.find(trk[0])).find(namespace + self.__TRKSEG_ELM).findall(namespace +  self.__TRKPT_ELM)
                output_buffer.append(self.__calculate_orthodromic_distance(activity))
        except Exception as ex:
            logging.ERROR("Processing of the landing directory was unsuccessful!\n", ex)
        return output_buffer

    def __calculate_orthodromic_distance(self, coords: list) -> str:
        """
        Purpose of this method is to calculate distance between provided
        coordinates in order to obtain total distance.
        :param coords: List of coordinates.
        :return: Total distance achieved.
        """
        buffer = 0

        for index in range(len(coords) - 1):
            lat1 = radians(float(coords[index].attrib['lat']))
            lat2 = radians(float(coords[index + 1].attrib['lat']))
            lon1 = radians(float(coords[index].attrib['lon']))
            lon2 = radians(float(coords[index + 1].attrib['lon']))

            dist_lat = lat2 - lat1
            dist_lon = lon2 - lon1
            pom = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2

            buffer += self.EARTH_RADIUS * (2 * asin(sqrt(pom)))
        return '{:.3f} Km'.format(buffer)

