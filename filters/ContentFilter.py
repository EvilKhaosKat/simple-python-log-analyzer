from filters.Filter import Filter, Settings, is_line_separate_record


class ContentFilter(Filter):
    def apply(self, source):
        """
        Perform filtration logic
        @rtype : iter
        @param source: iterable of strings, that represents content for filtration
        @return: iterable of strings, result of applying logic of filtration
        """
        previous_line_suitable = False

        result = []

        for line in source:
            if is_line_separate_record(line):
                for template in self.settings.templates:
                    if template in line:
                        result.append(line)
                        previous_line_suitable = True
                        break
                previous_line_suitable = False
            else:
                if self.settings.multiple_lines_support and previous_line_suitable:
                    result.append(line)
                    previous_line_suitable = True
                else:
                    previous_line_suitable = False

        return result


class ContentSettings(Settings):
    templates = []
    multiple_lines_support = True

    def __init__(self, templates, multiple_lines_support = True):
        """

        @param templates: list of strings to be mentioned in suitable line
        @param multiple_lines_support: log messages could be multiple per one entry
        , should filter try to correctly add such type of entries
        @return:
        """
        self.templates = templates
        self.multiple_lines_support = multiple_lines_support

        #print(self.templates)