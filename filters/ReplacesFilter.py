from filters.Filter import Filter, Settings


class ReplacesFilter(Filter):

    def apply(self, source):
        result = []

        for line in source:
            for old, new in self.settings.replaces.items():
                line = line.replace(old,new)
            result.append(line)

        return result


class ReplacesSettings(Settings):
    replaces = {}

    def __init__(self, raw_settings):
        """
        @param replaces dictionary 'old:new' values to be changed in file
        @return
        """
        self.replaces = self.parse_raw_settings(raw_settings)

    def parse_raw_settings(self, raw_settings):
        replaces = {}

        replaces.update({key:value for key, value in [replace.split("::") for replace in raw_settings.split(";")]})
        #I've made it just for lulz
        #one line of code that splits 'test1::new_test1;test2::new_test2' and makes dict

        return replaces


    def __str__(self, *args, **kwargs):
        return "replaces:" + str(self.replaces)


