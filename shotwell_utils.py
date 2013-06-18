import time
import datetime

def start_of_day(epoch):
    """Return the epoch for the start of the day within which the given epoch
    resides.

    Parameters:
        epoch: Time to find the start of the day for"""
    st = time.strftime("%Y%m%d", time.gmtime(epoch))
    t = time.strptime(st + " UTC", "%Y%m%d %Z")
    return time.mktime(t)

def end_of_day(epoch):
    """Return the epoch for the end of the day within which the given epoch
    resides.

    Parameters:
        epoch: Time to find the end of the day for"""
    st = time.strftime("%Y%m%d", time.gmtime(epoch))
    t = time.strptime(st + " 23:59:59 UTC", "%Y%m%d %H:%M:%S %Z")
    return time.mktime(t)

def events_for_secs(conn, secs):
    """Return a list of event ids for the given secs (seconds since the epoch).

    Parameters:
        conn: A sqlite3 database connection
        secs: seconds since the epoch
    """
    events = conn.execute("select distinct event_id from phototable where "
                 "exposure_time >= :start_time and exposure_time <= :end_time "
                 "and event_id != -1",
                 {"start_time": start_of_day(secs),
                 "end_time": end_of_day(secs)})
    return events.fetchall()

def set_video_event(conn, video_id, event_id):
    conn.execute("update videotable set event_id = :event_id "
                 "where id = :video_id", locals())

def set_video_exposure_time(conn, video_id, exposure_time):
    conn.execute("update videotable set exposure_time = :exposure_time "
                 "where id = :video_id", locals())

def create_event(conn):
    cur = conn.cursor()
    cur.execute("insert into eventtable (time_created) "
                "values (?)", (str(time.time()),))
    new_event_rowid = cur.lastrowid
    cur.execute("select id from eventtable where rowid = ?", (new_event_rowid,))
    return cur.fetchone()[0]

