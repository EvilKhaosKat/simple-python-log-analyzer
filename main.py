import sys
from filters.ContentFilter import ContentFilter, ContentSettings

__author__ = 'EvilKhaosKat'

#TODO named parameters instead of hardcoded order
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
    args = args[2:]

    for arg in args:
        result.append(arg)

    return result


def get_dest_filename(source_filename):
    """
    Calculates destination filename by source filename
    @param source_filename: string with source filename
    @return: this realization returns 'dest_' + source filename
    """
    return "dest_" + source_filename


def need_to_append_line(line, prev_line_added):
    return True

print("Simple realization. Assumed that first parameter of launching - filename for parsing (or qa_transfer.log by default)")
print("2...n parameters - templates to be found in line to be added in result file. For example it could be name of the classes.")
print("")

filename = get_filename()

source_file = open(filename)
print("Source file {0} opened.".format(filename))

dest_filename = get_dest_filename(filename)
dest_file = open(dest_filename, 'w')
print("File destination name '{0}'".format(dest_filename))

#TODO fabric methods for creating filters instances with settings
content_filter_settings = ContentSettings(get_strings_for_searching())
content_filter = ContentFilter(settings=content_filter_settings)

result = content_filter.apply(source_file)
print("Content filter applied.")

for line in result:
    dest_file.write(line)

source_file.close()
dest_file.close()