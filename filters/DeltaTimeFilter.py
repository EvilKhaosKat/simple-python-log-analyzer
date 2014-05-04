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

                    if self.settings.is_html:
                        result.append("<hr>")
                    else:
                        result.append("-"*80)
                        result.append("\n")

                previous_date = current_date

            result.append(line)

        return result


class DeltaTimeSettings(Settings):
    def __init__(self, time_delta_separation, is_html):
        self.time_delta_separation = time_delta_separation
        self.is_html = is_html

        self.time_delta = datetime.timedelta(seconds=time_delta_separation)