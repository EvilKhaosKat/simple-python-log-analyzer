import sys
from filters.ContentFilter import ContentFilter, ContentSettings

#TODO named parameters instead of hardcoded order
from filters.TimeFilter import TimeSettings, TimeFilter


def get_filename():
    """
    From sys.args returns first parameter - source filename
    @return: first parameter - source filename, or value by default
    "qa_transfer.log"
    """
    args = sys.argv

    #for arg in args:
    #    print(arg, sep="\n")

    if len(args) > 1:
        return args[1]
    else:
        return "qa_transfer.log"

def get_strings_for_searching():
    """
    Temporal method for parsing paramaters of launching
    @return: list of lines - what should be found in log file
    """
    result = []

    args = sys.argv
    args = args[3:]

    for arg in args:
        result.append(arg)

    return result

def get_hours_offset():
    args = sys.argv
    return int(args[2])


def get_dest_filename(source_filename):
    """
    Calculates destination filename by source filename
    @param source_filename: string with source filename
    @return: this realization returns 'dest_' + source filename
    """
    return "dest_" + source_filename


print("Simple realization. Assumed that first parameter of launching - filename for parsing (or qa_transfer.log by default)")
print("2 parameter - offset in hours from current moment")
print("3...n parameters - templates to be found in line to be added in result file. For example it could be name of the classes.")
print("")

filename = get_filename()

source_file = open(filename)
print("Source file '{0}' opened.".format(filename))

dest_filename = get_dest_filename(filename)
dest_file = open(dest_filename, 'w')
print("File destination - '{0}'".format(dest_filename))

#TODO fabric methods for creating filters instances with settings
strings_for_searching = get_strings_for_searching()
print("Strings for searching:" + str(strings_for_searching))

content_filter_settings = ContentSettings(strings_for_searching)
content_filter = ContentFilter(settings=content_filter_settings)

first_date = TimeSettings.get_date_by_offset(get_hours_offset())
print("First date for logging:" + str(first_date))

time_filter_settings = TimeSettings(first_date)
time_filter = TimeFilter(settings=time_filter_settings)

result = content_filter.apply(source_file)
print("Content filter applied.")
result = time_filter.apply(result)
print("Time filter applied.")

for line in result:
    dest_file.write(line)
print("Result file created.")

source_file.close()
dest_file.close()
print("Files closed.")