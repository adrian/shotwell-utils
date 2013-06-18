#!/usr/bin/env python

import time
import shotwell_utils
import logging
import sqlite3
import sys

def add_all_videos_to_events(conn):
    """This method loops through all videos with no event (event_id = -1) and
    links them to an event.

    Each video is linked to the event falling on the same day as the video's
    timestamp. I chose this field rather than the exposure_time as none of my
    videos had a value for exposure_time.

    If there's no event for the video then a new event is created.

    If there's more than one event for the video an error is printed to stderr
    and the video is skipped.

    In addition to linking the video to an event, the video's timestamp is
    copied to the exposure_time."""

    videos = conn.execute('select * from videotable where event_id = -1')
    #videos = conn.execute('select * from videotable where id = 315')
    for video in videos:
        logging.debug("Processing video: %s" % str(video))
        events = shotwell_utils.events_for_secs(conn, video[7])
        logging.debug("Events for timestamp %s: %s" % (str(video[7]), events))

        if len(events) == 0:
            logging.debug("Creating a new event")
            new_event_id = shotwell_utils.create_event(conn)

            logging.debug("Updating event_id on video %s to %s" \
                % (video[0], new_event_id))
            events = shotwell_utils.set_video_event(conn, video[0],
                new_event_id)

            # This has to be done so the video appears in the event rather than
            # listed as "Undated"
            if video[8] == 0:
                logging.debug("Updating exposure_time on video %s to %s" \
                    % (video[0], video[7]))
                shotwell_utils.set_video_exposure_time(conn, video[0], video[7])
        elif len(events) == 1:
            event_id = events[0][0]
            logging.debug("Updating event_id on video %s to %s" \
                % (video[0], event_id))
            events = shotwell_utils.set_video_event(conn, video[0],
                event_id)

            # Might as well set the video's exposure time if it's not alreay set
            if video[8] == 0:
                logging.debug("Updating exposure_time on video %s to %s" \
                    % (video[0], video[7]))
                shotwell_utils.set_video_exposure_time(conn, video[0], video[7])
        elif len(events) > 1:
            sys.stderr.write("More than one event for timestamp %s, %s\n" % \
                (video[6], events))

if  __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    conn = sqlite3.connect('photo.db')
    add_all_videos_to_events(conn)
    conn.commit()
    conn.close()

