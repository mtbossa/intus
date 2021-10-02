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

if __name__ == '__name__':
    unittest.main()
