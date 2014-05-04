from filters.Filter import Filter


class HtmlFilter(Filter):
    def apply(self, source):
        result = ["<html>\n"]

        for line in source:
            result.append(line)
            result.append("<br>")

        result.append("\n</html>")

        return result