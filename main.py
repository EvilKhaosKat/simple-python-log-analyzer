import sys
from filters.ContentFilter import ContentFilter, ContentSettings
from filters.TimeFilter import TimeSettings, TimeFilter

PARAM_FILENAME = "-filename"
PARAM_TEMPLATES = "-templates"
PARAM_HOURS_OFFSET = "-hours_offset"


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


def get_dest_filename(source_filename):
    """
    Calculates destination filename by source filename
    @param source_filename: string with source filename
    @return: this realization returns 'dest_' + source filename
    """
    return "dest_" + source_filename


print("Supported input parameters:")
print(PARAM_FILENAME)
print(PARAM_TEMPLATES)
print(PARAM_HOURS_OFFSET)
print("")

filename = get_filename()

source_file = open(filename)
print("Source file '{0}' opened.".format(filename))

dest_filename = get_dest_filename(filename)
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

for line in result:
    dest_file.write(line)

print("--------------------")
print("Result file created.")

source_file.close()
dest_file.close()
print("Files closed.")