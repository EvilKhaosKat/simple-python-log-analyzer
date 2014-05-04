import sys
from filters.ContentFilter import ContentFilter, ContentSettings
from filters.DeltaTimeFilter import DeltaTimeSettings, DeltaTimeFilter
from filters.HtmlFilter import HtmlFilter
from filters.ReplacesFilter import ReplacesSettings, ReplacesFilter
from filters.TimeFilter import TimeSettings, TimeFilter

PARAM_FILENAME = "-filename"
PARAM_TEMPLATES = "-templates"
PARAM_HOURS_OFFSET = "-hours_offset"
PARAM_REPLACE = "-replace"
PARAM_IS_HTML = "-is_html"
PARAM_TIME_DELTA_SEPARATION = "-time_delta_separation"


def get_filename():
    """
    From sys.args returns named parameter -filename
    @return: source filename
    """
    args = sys.argv[1:]

    #for arg in args:
    #    print(arg, sep="\n")

    for argument in args:
        if argument.startswith(PARAM_FILENAME):
            return argument.split("=")[1]

    raise Exception("Filename wasn't specified.")

#filters initialization
def get_strings_for_searching():
    """
    Temporal method for parsing parameters of launching.
    @return: list of lines - what should be found in log file
    """
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_TEMPLATES):
            values = argument.split("=")[1]
            return values.split(";")

    return []

def get_hours_offset():
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_HOURS_OFFSET):
            value = argument.split("=")[1]
            return int(value)

    return None

def get_replaces():
    replaces = {}

    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_REPLACE):
            value = argument[argument.find("=") + 1:]
            replaces.update({key:value for key, value in [replace.split("::") for replace in value.split(";")]})
            #I've made it just for lulz
            #one line of code that splits 'test1::new_test1;test2::new_test2' and makes dict

    return replaces

def get_is_html():
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_IS_HTML):
            return True

    return False

def get_time_delta_separation():
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_TIME_DELTA_SEPARATION):
            value = argument.split("=")[1]
            return int(value)

    return None


def get_dest_filename(source_filename, is_html):
    """
    Calculates destination filename by source filename
    @param source_filename: string with source filename
    @param is_html: if it's html file - add .html in the end
    @return: this realization returns 'dest_' + source filename
    """
    filename = "dest_" + source_filename

    if is_html:
        return filename + ".html"
    else:
        return filename


print("Supported input parameters:")
print(PARAM_FILENAME)
print(PARAM_TEMPLATES + " | ;-separated strings to be found in file")
print(PARAM_HOURS_OFFSET)
print(PARAM_REPLACE + " | with format old::new;old1::new1")
print(PARAM_IS_HTML)
print(PARAM_TIME_DELTA_SEPARATION + " | value in seconds")
print("")


filename = get_filename()

source_file = open(filename)
print("Source file '{0}' opened.".format(filename))

is_html = False
is_html = get_is_html()

dest_filename = get_dest_filename(filename, is_html)
dest_file = open(dest_filename, 'w')
print("File destination - '{0}'".format(dest_filename))
print("")

result = source_file

#TODO fabric methods for creating filters instances with settings

strings_for_searching = get_strings_for_searching()
print("Strings for searching:" + str(strings_for_searching))
if strings_for_searching:
    content_filter_settings = ContentSettings(strings_for_searching)
    content_filter = ContentFilter(settings=content_filter_settings)
    result = content_filter.apply(result)
    print("Content filter applied.")
print("")

hours_offset = get_hours_offset()
print("Hours offset:" + str(hours_offset))
if hours_offset:
    first_date = TimeSettings.get_date_by_offset(hours_offset)
    print("First date for logging:" + str(first_date))
    time_filter_settings = TimeSettings(first_date)
    time_filter = TimeFilter(settings=time_filter_settings)
    result = time_filter.apply(result)
    print("Time filter applied.")
print("")

replaces = get_replaces()
print("Replaces:" + str(replaces))
if replaces:
    replaces_settings = ReplacesSettings(replaces)
    replaces_filter = ReplacesFilter(settings=replaces_settings)
    result = replaces_filter.apply(result)
    print("Replaces filter applied.")
print("")

print("Is html:" + str(is_html))
if is_html:
    html_filter = HtmlFilter()
    result = html_filter.apply(result)
    print("HTML filter applied.")
print("")

time_delta_separation = get_time_delta_separation()
print("Delta time separation: %s seconds" % time_delta_separation)
if time_delta_separation:
    delta_time_settings = DeltaTimeSettings(time_delta_separation, is_html)
    delta_time_filter = DeltaTimeFilter(settings=delta_time_settings)
    result = delta_time_filter.apply(result)
    print("Delta time filter applied.")
print("")


for line in result:
    dest_file.write(line)

print("--------------------")
print("Result file created.")

source_file.close()
dest_file.close()
print("Files closed.")