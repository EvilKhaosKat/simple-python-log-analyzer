import datetime
from filters import TimeFilter
from filters.Filter import Filter, Settings, is_line_separate_record


class DeltaTimeFilter(Filter):
    def apply(self, source):
        result = []

        previous_date = datetime.datetime.now()

        for line in source:
            if is_line_separate_record(line):
                current_date = TimeFilter.get_date_from_line(line)
                delta_date = current_date - previous_date
                #print("delta_date:" + str(delta_date))
                #print("time_delta:" + str(self.settings.time_delta))
                #print("")
                if delta_date > self.settings.time_delta:
                    #print("add separator")
                    result.append(self.settings.separator)
                    result.append("\n")
                previous_date = current_date
            result.append(line)

        return result


class DeltaTimeSettings(Settings):
    time_delta = None
    separator = None

    def __init__(self, raw_settings):
        time_delta_separation, self.separator = self.parse_raw_settings(raw_settings)

        self.time_delta = datetime.timedelta(seconds=time_delta_separation)

    def parse_raw_settings(self, raw_settings):
        seconds = raw_settings['seconds']
        separator = raw_settings.get('separator')

        return seconds, separator if separator else '-'*80

    def __str__(self, *args, **kwargs):
        return 'time_delta:' + str(self.time_delta)

