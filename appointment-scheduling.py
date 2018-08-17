#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import csv
from random import randrange
from pprint import pprint


class Interval:
    """Represents time interval using datetime module"""

    def __init__(self, start, end, time_format='%Y-%m-%dT%H:%M:%SZ'):
        """
        Initializes object with specified start time, end time and time format string

        Args:
            start (datetime): Start time string.
            end (datetime): End time string.
            time_format (str, optional): Time format string.

        Attributes:
            start (datetime): Start time structure.
            end (datetime): End time structure.
            time_format (str): Time format string.
        """

        self.start = start
        self.end = end
        self.time_format = time_format

    def __repr__(self):
        """
        Overloads __repr__ method

        Returns:
            str: String representation of the object
        """

        return '{start} — {end}'.format(start=self.start.strftime(self.time_format),
                                        end=self.end.strftime(self.time_format))


def generate_bookings(min_start, max_end, booking_count=10, time_format='%Y-%m-%dT%H:%M:%SZ'):
    """
    Generates random booking intervals in specified time window

    Args:
        min_start (str): Start time string.
        max_end (str): End time string.
        booking_count (int, optional): Number of booking intervals
        time_format (str, optional): Time format string.

    Returns:
        :obj:`list` of :obj:`Interval`: Returns list of bookings
    """

    t_min_start = datetime.strptime(min_start, time_format)
    t_max_end = datetime.strptime(max_end, time_format)
    t_delta = t_max_end - t_min_start
    bookings = []

    for i in range(booking_count):
        t_start_offset = randrange(t_delta.seconds)
        t_start = t_min_start + timedelta(seconds=t_start_offset)
        t_end_offset = randrange(t_delta.seconds-t_start_offset)
        t_end = t_start + timedelta(seconds=t_end_offset)
        bookings.append(Interval(t_start, t_end))

    return bookings


def read_bookings_from_csv(csv_path, time_format='%Y-%m-%dT%H:%M:%SZ'):
    """
    Reads booking time intervals from input csv file

    Args:
        csv_path (str): Path to input csv file with booking time intervals.
        time_format (str): Time format string to use with time module.

    Returns:
        :obj:`list` of :obj:`Interval`: Returns list of bookings
    """

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        booking_intervals = [Interval(datetime.strptime(row[0], time_format),
                                      datetime.strptime(row[1], time_format),
                                      time_format)
                             for row in reader]
        return booking_intervals


def schedule_bookings(booking_intervals, endpoints_overlap_flag=False):
    """
    Schedules bookings using minimum number of rooms.

    Args:
        booking_intervals (:obj:`list` of :obj:`Interval`): List of Interval objects
            with defined start time, end time and time format for each.
        endpoints_overlap_flag (bool): If True the end of the previous Interval
            can be equal to the start of the next Interval

    Returns:
        int: Returns minimum number of rooms required for provided booking intervals.
    """

    sorted_b_intervals = sorted(booking_intervals, key=lambda x: x.start)
    rooms = []

    for b_interval in sorted_b_intervals:
        need_room_flag = True
        for room in rooms:
            # Check if start of current interval is not in last added interval of current room
            if (b_interval.start > room[-1].end and endpoints_overlap_flag is False) \
                    or (b_interval.start >= room[-1].end and endpoints_overlap_flag is True):
                need_room_flag = False
                room.append(b_interval)
                break

        if need_room_flag:
            rooms.append([b_interval,])

    print('Rooms list:')
    pprint(rooms)

    return len(rooms)


if __name__ == '__main__':
    csv_path = 'src/booking_intervals.csv'
    time_format = '%Y-%m-%dT%H:%M:%SZ'

    # Try pre-define csv to test endpoints_overlap_flag=True|False
    # booking_intervals = read_bookings_from_csv(csv_path, time_format)

    booking_intervals = generate_bookings('2018-08-01T00:00:00Z', '2018-08-01T02:59:59Z', booking_count=20)
    room_count = schedule_bookings(booking_intervals, endpoints_overlap_flag=False)

    print('\nMinimum number of rooms: {0}'.format(room_count))
