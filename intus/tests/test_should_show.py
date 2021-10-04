import datetime
import unittest

from intus import utils


class TestShouldShow(unittest.TestCase):

    def test_check_dates_and_times(self):
        # Date Tests
        # Already started date (same day now day)
        # True
        start_date = datetime.date.fromisoformat('2021-10-27')
        end_date = datetime.date.fromisoformat('2021-10-28')

        start_time = datetime.time.fromisoformat('19:00:00')
        end_time = datetime.time.fromisoformat('20:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-10-27 19:30:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Shouldn't start yet by date (now day less than start day)
        # True
        start_date = datetime.date.fromisoformat('2021-11-10')
        end_date = datetime.date.fromisoformat('2021-12-10')

        start_time = datetime.time.fromisoformat('19:00:00')
        end_time = datetime.time.fromisoformat('20:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-10-27 19:30:00')
        self.assertFalse(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Ended date
        # False
        start_date = datetime.date.fromisoformat('2021-05-15')
        end_date = datetime.date.fromisoformat('2021-05-25')

        start_time = datetime.time.fromisoformat('19:00:00')
        end_time = datetime.time.fromisoformat('20:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 19:30:00')
        self.assertFalse(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Show hour earlier than now
        # True
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('15:30:00')
        end_time = datetime.time.fromisoformat('20:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 16:30:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Show hour same than now
        # True
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('15:30:00')
        end_time = datetime.time.fromisoformat('20:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 15:31:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Show hour end same than now
        # True
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('15:30:00')
        end_time = datetime.time.fromisoformat('17:30:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 17:00:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Show start hour end hour same than now
        # True
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('18:10:00')
        end_time = datetime.time.fromisoformat('18:50:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 18:10:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Don't show already passed hour
        # False
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('09:00:00')
        end_time = datetime.time.fromisoformat('11:30:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 11:31:00')
        self.assertFalse(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        # Don't show already passed hour
        # False
        start_date = datetime.date.fromisoformat('2021-05-14')
        end_date = datetime.date.fromisoformat('2021-06-25')

        start_time = datetime.time.fromisoformat('09:00:00')
        end_time = datetime.time.fromisoformat('11:30:00')

        now_datetime = datetime.datetime.fromisoformat('2021-06-10 12:31:00')
        self.assertFalse(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

        start_date = datetime.date.fromisoformat('2021-09-22')
        end_date = datetime.date.fromisoformat('2021-11-10')

        start_time = datetime.time.fromisoformat('10:00:00')
        end_time = datetime.time.fromisoformat('19:00:00')

        now_datetime = datetime.datetime.fromisoformat('2021-10-02 12:57:00')
        self.assertTrue(utils.check_dates_and_times(start_time, end_time, start_date, end_date, now_datetime))

    def test_today_recurrence(self):
        # Date Tests
        # Current year
        # True
        recurrence = {
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-06-25')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # Next year
        # False
        recurrence = {
            "year": 2022
        }

        today = datetime.date.fromisoformat('2021-06-25')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "month": 11,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-11-03')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "month": 11,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-10-02')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "day": 15,
            "month": 11,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-11-15')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "day": 15,
            "month": 11,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-11-16')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 3,
            "day": 10,
            "month": 2,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-02-10')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "isoweekday": 3,
            "day": 10,
            "month": 2,
            "year": 2021
        }

        today = datetime.date.fromisoformat('2021-03-10')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "month": 5,
        }

        today = datetime.date.fromisoformat('2021-05-10')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "month": 5,
        }

        today = datetime.date.fromisoformat('2021-05-23')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "month": 5,
        }

        today = datetime.date.fromisoformat('2021-06-10')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "day": 13,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-13')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "day": 13,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-14')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "day": 13,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-05-13')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 7,
            "day": 13,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-13')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 7,
            "day": 13,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2022-06-13')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 2,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-01')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 2,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-08')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "isoweekday": 2,
            "month": 6,
        }

        today = datetime.date.fromisoformat('2021-06-09')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "day": 10
        }

        today = datetime.date.fromisoformat('2021-01-10')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "day": 10
        }

        today = datetime.date.fromisoformat('2021-02-10')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "day": 10
        }

        today = datetime.date.fromisoformat('2021-01-11')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 1,
            "day": 10
        }

        today = datetime.date.fromisoformat('2021-05-10')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "isoweekday": 1,
            "day": 10
        }

        today = datetime.date.fromisoformat('2021-06-10')
        self.assertFalse(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 7,
        }

        today = datetime.date.fromisoformat('2021-01-03')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # True
        recurrence = {
            "isoweekday": 7,
        }

        today = datetime.date.fromisoformat('2021-02-07')
        self.assertTrue(utils.today_recurrence(recurrence, today))

        # False
        recurrence = {
            "isoweekday": 7,
        }

        today = datetime.date.fromisoformat('2021-04-07')
        self.assertFalse(utils.today_recurrence(recurrence, today))


if __name__ == '__name__':
    unittest.main()
