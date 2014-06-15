import unittest
from filters.Filter import Filter, Settings, is_line_separate_record
import datetime


def get_date_from_line(line):
    """
    Try to parse suitable format log entry in to date object<br>
    like this one '=27.02.2014 18:31:13.384'
    Current version - pretty naive algorithm
    @param line: string to parse
    @return: datetime object
    """
    new_line = line[1:]

    splitted_line = new_line.split(' ')

    day_date = splitted_line[0].split('.')
    year = int(day_date[2])
    month = int(day_date[1])
    day = int(day_date[0])

    day_time = splitted_line[1].split(":")
    hour = int(day_time[0])
    minute = int(day_time[1])

    # print("year:" + year)
    # print("month:" + month)
    # print("day:" + day)
    # print("hour:" + hour)
    # print("minute:" + minute)

    return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)


class TimeFilter(Filter):
    #date = datetime.datetime.now()

    def apply(self, source):
        result = []
        first_date = self.settings.first_date

        moment_found = False
        for line in source:
            if moment_found:
                result.append(line)
            elif is_line_separate_record(line):
                date_from_line = get_date_from_line(line)
                if date_from_line >= first_date:
                    moment_found = True
                    result.append(line)

        return result


class TimeSettings(Settings):
    first_date = None

    def __init__(self, raw_settings):
        super().__init__()
        self.first_date = self.get_date_by_offset(self.parse_raw_settings(raw_settings))

    def parse_raw_settings(self, raw_settings):
        return int(raw_settings)

    @staticmethod
    def get_date_by_offset(hours_offset):
        """
        Calculates date from current minus offset hours
        @param hours_offset: hours offset for current date
        @return: first suitable date
        """
        cur_date = datetime.datetime.now()

        # year = cur_date.year
        # month = cur_date.month
        # day = cur_date.day
        hour = cur_date.hour
        # minute = cur_date.minute

        #print(cur_date.strftime("%d.%m.%y %H:%M"))

        delta = datetime.timedelta(hours=hours_offset)

        return cur_date - delta

    def __str__(self, *args, **kwargs):
        return 'first_date:' + str(self.first_date)


class TestTimeFilter(unittest.TestCase):
    def test_get_date_from_line(self):
        time_filter = TimeFilter()
        date = get_date_from_line("=16.03.2014 18:31:14.892")

        self.assertEquals(date.day, 16)
        self.assertEquals(date.month, 3)
        self.assertEquals(date.year, 2014)
        self.assertEquals(date.hour, 18)
        self.assertEquals(date.minute, 31)

if __name__ == '__main__':
    print("self-testing for TimeFilter.py")
    unittest.main()