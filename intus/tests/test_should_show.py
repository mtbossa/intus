import datetime
import unittest

from intus import utils


class TestShouldShow(unittest.TestCase):
    def test_check_dates_and_times(self):
        # Already started
        # Start date 2021-9-27 10:10:10 AM - 1632748210
        # End date 2021-9-27 09:20:10 PM - 1632788410
        # Now date 2021-9-27 10:20:10 AM - 1632748810
        # True
        start_datetime = datetime.datetime.fromtimestamp(1632748210)
        end_datetime = datetime.datetime.fromtimestamp(1632788410)
        now_datetime = datetime.datetime.fromtimestamp(1632748810)
        self.assertTrue(utils.check_dates_and_times(start_datetime, end_datetime, now_datetime))

        # Shouldn't start yet
        # Start date 2021-10-10 05:10:10 AM - 1633853410
        # End date 2021-11-25 08:30:50 PM - 1637839850
        # Now date 2021-10-08 07:25:10 PM - 1633731910
        # True
        start_datetime = datetime.datetime.fromtimestamp(1633853410)
        end_datetime = datetime.datetime.fromtimestamp(1637839850)
        now_datetime = datetime.datetime.fromtimestamp(1633731910)
        self.assertFalse(utils.check_dates_and_times(start_datetime, end_datetime, now_datetime))

        # Ended
        # Start date Thursday, November 25, 2021 8:30:50 AM GMT-03:00 - 1637839850
        # End date Tuesday, November 30, 2021 10:30:50 PM GMT-03:00- 1638322250
        # Now date Tuesday, November 30, 2021 11:30:50 PM GMT-03:00 - 1638325850
        # True
        start_datetime = datetime.datetime.fromtimestamp(1637839850)
        end_datetime = datetime.datetime.fromtimestamp(1638322250)
        now_datetime = datetime.datetime.fromtimestamp(1638325850)
        self.assertFalse(utils.check_dates_and_times(start_datetime, end_datetime, now_datetime))

        # Start now hour and end now hour
        # Start date Sunday, January 10, 2021 7:10:10 AM GMT-03:00 - 1610273410
        # End date Sunday, January 10, 2021 7:50:10 AM GMT-03:00 - 1610275810
        # Now date Sunday, January 10, 2021 7:15:10 AM GMT-03:00 - 1610273710
        # True
        start_datetime = datetime.datetime.fromtimestamp(1610273410)
        end_datetime = datetime.datetime.fromtimestamp(1610275810)
        now_datetime = datetime.datetime.fromtimestamp(1610273710)
        self.assertTrue(utils.check_dates_and_times(start_datetime, end_datetime, now_datetime))

        # Start now hour and end now hour
        # Start date Tuesday, June 15, 2021 2:30:00 PM GMT-03:00 - 1623778200
        # End date Sunday, June 20, 2021 2:40:00 PM GMT-03:00 - 1624210800
        # Now date Tuesday, June 15, 2021 2:20:00 PM GMT-03:00 - 1623777600
        # True
        start_datetime = datetime.datetime.fromtimestamp(1623778200)
        end_datetime = datetime.datetime.fromtimestamp(1624210800)
        now_datetime = datetime.datetime.fromtimestamp(1623777600)
        self.assertFalse(utils.check_dates_and_times(start_datetime, end_datetime, now_datetime))


if __name__ == '__name__':
    unittest.main()
