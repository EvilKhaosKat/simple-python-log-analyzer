import sys
from SettingsAnalyzer import SettingsAnalyzer

PARAM_FILENAME = "-filename"
PARAM_OUTPUT_FILENAME = '-output_filename'
PARAM_SETTINGS_FILENAME = '-settings_filename'


def get_settings_filename():
    """
    From sys.args returns named parameter -settings_filename
    @return: source filename
    """
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_SETTINGS_FILENAME):
            return argument.split("=")[1]

    return 'settings.json'

def get_filename():
    """
    From sys.args returns named parameter -filename
    @return: source filename
    """
    args = sys.argv[1:]

    for argument in args:
        if argument.startswith(PARAM_FILENAME):
            return argument.split("=")[1]

    raise Exception("Filename wasn't specified.")

def get_dest_filename(source_filename, is_html):
    """
    Calculates destination filename by source filename
    @param source_filename: string with source filename
    @param is_html: if it's html file - add .html in the end
    @return: this realization returns 'dest_' + source filename
    """

    args = sys.argv[1:]
    for argument in args:
        if argument.startswith(PARAM_OUTPUT_FILENAME):
            return argument.split("=")[1]

    filename = "dest_" + source_filename

    if is_html:
        return filename + ".html"
    else:
        return filename

def perform_analysis(filename, settings_filename, output_filename):
    print("Main parameters")
    print(PARAM_FILENAME)
    print(PARAM_OUTPUT_FILENAME)
    print(PARAM_SETTINGS_FILENAME)
    print("")

    source_file = open(filename)
    print("Source file '{0}' opened.".format(filename))
    result = source_file

    print("settings_filename:" + settings_filename)
    print("")
    settings_analyzer = SettingsAnalyzer(settings_filename)
    filters_sequence = settings_analyzer.parse_settings()
    result = filters_sequence.apply(result)

    dest_filename = output_filename if output_filename else get_dest_filename(filename, filters_sequence.is_html)
    dest_file = open(dest_filename, 'w')
    print("")
    print("File destination - '{0}'".format(dest_filename))
    print("")

    for line in result:
        dest_file.write(line)

    print("--------------------")
    print("Result file created.")

    source_file.close()
    dest_file.close()
    print("Files closed.")


if __name__ == "__main__":
    perform_analysis(get_filename(), get_settings_filename(), None)
