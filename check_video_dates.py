#!/usr/bin/env python

import sqlite3
import re
import sys
import time
import os
import logging

"""Iterate through all videos that have no associated event and report on those
whose path date is different to their last modified time. For example, given a
video with this path, /home/adrian/Videos/2012/03/14/testing.mp4, we would
expect the file to have a last modified time sometime during the day
2012/03/14. If it didn't this program would report it.

Reporting is by means of printing the file's last modified time and full path
and file name to stderr."""

def path_date(path):
    """Return a tuple of (YYYY, MM, DD) taken from the given path where path
    is structured along the lines of /dir1/dir2/YYYY/MM/DD"""
    matches = re.search('(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})', path)
    return (int(matches.group('year')), int(matches.group('month')),
        int(matches.group('day')))

def lastupdate_date(path):
    last_modified_date = time.gmtime(os.stat(path).st_mtime)
    return (last_modified_date.tm_year, last_modified_date.tm_mon, last_modified_date.tm_mday)

def report_videos_with_bad_dates(conn):
    """Look through all videos with no event and report those whose path date
    if different to the last modified date. Return True if any such videos are
    found.

    Parameters
        conn: sqlite3 connection to shotwell database"""
    found_problem_videos = False
    videos = conn.execute('select * from videotable where event_id = -1')
    for video in videos:
        logging.debug("Processing %s" % str(video))

        video_lastupdate_date = lastupdate_date(video[1])
        video_path_date = path_date(video[1])

        logging.debug("lastupdate date: %s" % str(video_lastupdate_date))
        logging.debug("path date: %s" % str(video_path_date))

        if path_date(video[1]) != video_lastupdate_date:
            sys.stderr.write("%s %s\n" % (str(video_lastupdate_date).ljust(14),
                video[1]))
            found_problem_videos = True

    return found_problem_videos

if  __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    conn = sqlite3.connect('photo.db')
    found_problem_videos = report_videos_with_bad_dates(conn)
    conn.close()

    sys.exit(1 if found_problem_videos else 0)

