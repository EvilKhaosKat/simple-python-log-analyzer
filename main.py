import sys

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

prev_line_added = False
for line in source_file:
    if need_to_append_line(line, prev_line_added):
        dest_file.write(line)
        prev_line_added = True
    else:
        prev_line_added = False

source_file.close()
dest_file.close()