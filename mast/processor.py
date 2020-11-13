from math import radians, cos, sin, asin, sqrt
import xml.etree.ElementTree as ET
from pathlib import Path
import os
from re import findall
import logging
from dateutil import parser


class GPXProcessor(object):
    EARTH_RADIUS = 6378
    LANDING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'landing')
    __ALLOWED_EXTENSIONS = ['.gpx', '.xml']
    __TRKSEG_ELM = 'trkseg'
    __TRKPT_ELM = 'trkpt'
    __TIME_ELM = 'time'
    __TRK_ELM = 'trk'

    def __init__(self):
        super().__init__()

    def process_input_data(self, input_file: str) -> zip:
        """
        Purpose of this method is to iterate over each .xml file
        within landing layer, load its content and fetch all
        coordinates in order to calculate total distance in Km.
        """

        output_buffer = []
        total_time = []
        activity_start = []
        try:
            input_file = os.path.join(self.LANDING_DIR, input_file)
            if Path(input_file).suffix in self.__ALLOWED_EXTENSIONS:
                tree = ET.parse(os.path.join(self.LANDING_DIR, input_file))
                root = tree.getroot()

                # Find the child element of tracking point including namespace
                pom_elem = findall('\{.*\}.*', root[0].tag if len(root) > 1 else root[0].tag)
                # Cut of namespace prefix
                namespace = findall('\{.*\}', pom_elem[0])[0]
                trk = root.find(namespace + self.__TRK_ELM)
                activities = trk.find(namespace + self.__TRKSEG_ELM).findall(
                    namespace + self.__TRKPT_ELM)

                if activities[0].find(namespace + self.__TIME_ELM) is not None:
                    time_seg = [activity.find(namespace + self.__TIME_ELM) for activity in activities]
                    activity_start.append(parser.parse(time_seg[0].text))
                    total_time.append(self.__calculate_total_time(time_seg))
                output_buffer.append(round(self.__calculate_orthodromic_distance(activities), 1))
            else:
                raise AssertionError("Forbidden file extension encountered!")
        except Exception as ex:
            logging.error("Processing of the landing directory was unsuccessful!\n", ex)
        return list(zip(output_buffer, total_time, activity_start))

    def __calculate_total_time(self, time_segments: list):
        """
        Purpose of this method is to calculate the time of the give activity.
        : param time_segments: List of timestamps.
        :return: Total time spent on activity.
        """
        return parser.parse(time_segments[-1].text) - parser.parse(time_segments[0].text)

    def __calculate_orthodromic_distance(self, coords: list) -> float:
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
        return buffer

    def landing_cleanup(self, input_file: str):
        """
        Purpose of this method is clean up landing zone.
        """
        try:
            os.remove(os.path.join(self.LANDING_DIR, input_file))
            logging.info(f"File {input_file} has been removed successfully.")
        except Exception as ex:
            logging.warning("Deletion was unsuccessful!", ex)


if __name__ == '__main__':
    print(list(GPXProcessor().process_input_data('test.gpx')))