shotwell-utils
==============
A collection of tools for interacting with the Shotwell database.


add_all_videos_to_events.py
---------------------------
This program adds all videos with no associated event to an event.

If there's an existing event matching the video's timestamp it will be used. If
there's no event on that date a new one will be created.

WARNING: This program updates Shotwell's photo.db. Make a backup before running
it.


check_video_dates.py
--------------------
Iterate through all videos that have no associated event and report on those
whose path date is different to their last modified time. For example, given a
video with this path, /home/adrian/Videos/2012/03/14/testing.mp4, we would
expect the file to have a last modified time sometime during the day
2012/03/14. If it didn't this program would report it.

The reason I wrote this program was to verify each video's original shooting
date. The only two dates I had to go on were the path date and last modified
date. If both of these dates were the same it increased my confidence that it
was the actual shooting date.

