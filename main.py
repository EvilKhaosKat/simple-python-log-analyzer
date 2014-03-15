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


filename = get_filename()

source_file = open(filename)
dest_file = open(get_dest_filename(filename), 'w')

#TODO fabric methods for creating filters instances with settings
content_filter_settings = ContentSettings(get_strings_for_searching())
content_filter = ContentFilter(settings=content_filter_settings)

result = content_filter.apply(source_file)

for line in result:
    dest_file.write(line)

source_file.close()
dest_file.close()