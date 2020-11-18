from math import radians, cos, sin, asin, sqrt
import xml.etree.ElementTree as ET
from pathlib import Path
import os
import sys
from re import findall
import logging
from dateutil import parser
import datetime


class GPXProcessor(object):
    EARTH_RADIUS = 6378
    LANDING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'landing')
    __ALLOWED_EXTENSIONS = ['.gpx', '.xml']
    __TRKSEG_ELM = 'trkseg'
    __TRKPT_ELM = 'trkpt'
    __TIME_ELM = 'time'
    __TRK_ELM = 'trk'

    __namespace = ''
    __track_time = True

    def __init__(self):
        super().__init__()

    def process_input_data(self, input_file: str) -> list:
        """
        Purpose of this method is to iterate over each .xml file
        within landing layer, load its content and fetch all
        coordinates in order to calculate total distance in Km.
        """

        total_distance = 0
        activity_duration = None
        activity_start = None
        try:
            input_file = os.path.join(self.LANDING_DIR, input_file)
            if Path(input_file).suffix in self.__ALLOWED_EXTENSIONS:
                with open(os.path.join(self.LANDING_DIR, input_file), mode='rb') as xml_inp:
                    tree = ET.parse(xml_inp)
                    root = tree.getroot()

                    # Find the child element of tracking point including __namespace
                    pom_elem = findall('{.*}.*', root[0].tag if len(root) > 1 else root[0].tag)
                    # Cut of namespace prefix
                    self.__namespace = findall('{.*}', pom_elem[0])[0]
                    trk = root.find(self.__namespace + self.__TRK_ELM)
                    # Find all trk segments
                    trk_seg = [seg for seg in trk.findall(self.__namespace + self.__TRKSEG_ELM)]

                    # Create dict where key is the seg and its value is array of activity points
                    segments = {seg: seg.findall(self.__namespace + self.__TRKPT_ELM) for seg in trk_seg}

                    try:
                        timestamp_start = segments[list(segments.keys())[0]][0].find(self.__namespace + self.__TIME_ELM)
                        if timestamp_start is not None:
                            activity_start = parser.parse(timestamp_start.text)
                        else:
                            self.__track_time = False
                    except Exception as e:
                        logging.info("No timestamp for activity start present.", e)
                        self.__track_time = False

                    inter_segment = [None, None]
                    segments_distance = []
                    segments_time = []

                    # If there is no timestamp skip
                    for segment in segments.values():
                        if inter_segment[0] is not None:
                            inter_segment[1] = segment[0]
                            segments_time.append(self.__calculate_total_time(inter_segment))
                            segments_distance.append(self.__calculate_orthodromic_distance(inter_segment))

                        segments_time.append(self.__calculate_total_time(segment))
                        segments_distance.append(self.__calculate_orthodromic_distance(segment))

                        inter_segment[0] = segment[-1]
                    total_distance = round(sum(segments_distance), 1)
                    activity_duration = sum(segments_time, datetime.timedelta())

                    xml_inp.close()
            else:
                raise AssertionError("Forbidden file extension encountered!")
        except Exception as ex:
            logging.error("Processing of the landing directory was unsuccessful!\n", ex)
        return [total_distance, activity_duration, activity_start]

    def __calculate_total_time(self, segment: list) -> datetime.timedelta:
        """
        Purpose of this method is to calculate the time of the give activity.
        :param segment: List of track points.
        :return: Total time spent on activity.
        """
        if not self.__track_time:
            return datetime.timedelta()
        segment_time = [c_activity.find(self.__namespace + self.__TIME_ELM) for c_activity in segment]
        return parser.parse(segment_time[-1].text) - parser.parse(segment_time[0].text)

    def __calculate_orthodromic_distance(self, segment: list) -> float:
        """
        Purpose of this method is to calculate distance between provided
        coordinates in order to obtain total distance.
        :param segment: List of track points.
        :return: Total distance achieved.
        """
        buffer = 0

        for index in range(len(segment) - 1):
            lat1 = radians(float(segment[index].attrib['lat']))
            lat2 = radians(float(segment[index + 1].attrib['lat']))
            lon1 = radians(float(segment[index].attrib['lon']))
            lon2 = radians(float(segment[index + 1].attrib['lon']))

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
    print(GPXProcessor().process_input_data(sys.argv[1]))
