import json
from filters.ContentFilter import ContentSettings, ContentFilter
from filters.DeltaTimeFilter import DeltaTimeFilter, DeltaTimeSettings
from filters.FiltersSequence import FiltersSequence
from filters.HtmlFilter import HtmlFilter
from filters.ReplacesFilter import ReplacesSettings, ReplacesFilter
from filters.TimeFilter import TimeFilter, TimeSettings


class SettingsAnalyzer:
    PARAM_TEMPLATES = "templates"
    PARAM_HOURS_OFFSET = "hours_offset"
    PARAM_REPLACE = "replace"
    PARAM_IS_HTML = "is_html"
    PARAM_TIME_DELTA_SEPARATION = "time_delta_separation"

    settings_filename = ''

    def __init__(self, settings_filename):
        self.settings_filename = settings_filename

        print("Supported input parameters:")
        print(self.PARAM_TEMPLATES + " | ;-separated strings to be found in file")
        print(self.PARAM_HOURS_OFFSET)
        print(self.PARAM_REPLACE + " | with format old::new;old1::new1")
        print(self.PARAM_IS_HTML)
        print(self.PARAM_TIME_DELTA_SEPARATION + " | value in seconds")
        print("")

    def parse_settings(self):
        filters = []
        is_html = False

        settings_file = open(self.settings_filename)
        settings = json.loads(settings_file.read())
        # print('settings_filename:' + self.settings_filename)
        # print('settings:' + str(settings))

        for param_name in settings.keys():
            param_value = settings[param_name]

            if param_name.startswith(self.PARAM_REPLACE):
                replaces_settings = ReplacesSettings(param_value)
                filters.append(ReplacesFilter(settings=replaces_settings))

            elif param_name.startswith(self.PARAM_HOURS_OFFSET):
                time_filter_settings = TimeSettings(param_value)
                filters.append(TimeFilter(settings=time_filter_settings))

            elif param_name.startswith(self.PARAM_TEMPLATES):
                content_filter_settings = ContentSettings(param_value)
                filters.append(ContentFilter(settings=content_filter_settings))

            elif param_name.startswith(self.PARAM_IS_HTML):
                #TODO HtmlFilter must be applied last
                filters.append(HtmlFilter())
                is_html = True

            elif param_name.startswith(self.PARAM_TIME_DELTA_SEPARATION):
                delta_time_settings = DeltaTimeSettings(param_value)
                filters.append(DeltaTimeFilter(settings=delta_time_settings))

        return FiltersSequence(filters, is_html)
