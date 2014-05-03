from filters.Filter import Filter, Settings


class ReplacesFilter(Filter):

    def apply(self, source):
        result = []

        for line in source:
            for old, new in self.settings.replaces.items():
                result.append(line.replace(old, new))

        return result


class ReplacesSettings(Settings):
    replaces = {}

    def __init__(self, replaces):
        super().__init__()
        self.replaces = replaces
