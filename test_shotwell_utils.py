import unittest
import shotwell_utils
import sqlite3

class BasicTests(unittest.TestCase):

    def test_start_of_day(self):
        t1 = 1371407028.968546
        start_t1 = shotwell_utils.start_of_day(t1)
        self.assertEquals(start_t1, 1371340800)

    def test_end_of_day(self):
        t1 = 1371458174.968546
        start_t1 = shotwell_utils.end_of_day(t1)
        self.assertEquals(start_t1, 1371513599)

    def test_events_for_secs(self):
        conn = sqlite3.connect('photo.db')
        events = shotwell_utils.events_for_secs(conn, 1345766399)
        self.assertEquals(len(events), 2)
