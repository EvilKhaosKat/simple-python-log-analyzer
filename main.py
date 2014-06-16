import sys
from SettingsAnalyzer import SettingsAnalyzer
#import statprof


PARAM_FILENAME = "-filename"
PARAM_OUTPUT_FILENAME = '-output_filename'
PARAM_SETTINGS_FILENAME = '-settings_filename'


class Main:
    filename = ""
    settings_filename = ""
    output_filename = ""

    def __init__(self, filename, settings_filename, output_filename):
        self.filename = filename
        self.settings_filename = settings_filename
        self.output_filename = output_filename

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def perform_analysis(self):
        # statprof.start()

        print("Main parameters")
        print(PARAM_FILENAME)
        print(PARAM_OUTPUT_FILENAME)
        print(PARAM_SETTINGS_FILENAME)
        print("")

        source_file = open(self.filename)
        print("Source file '{0}' opened.".format(self.filename))
        result = source_file

        print("settings_filename:" + self.settings_filename)
        print("")
        settings_analyzer = SettingsAnalyzer(self.settings_filename)
        filters_sequence = settings_analyzer.parse_settings()
        result = filters_sequence.apply(result)

        dest_filename = self.output_filename if self.output_filename else self.get_dest_filename(self.filename, filters_sequence.is_html)
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

        # statprof.stop()
        # statprof.display()


if __name__ == "__main__":
    main = Main(Main.get_filename(), Main.get_settings_filename(), None)
    main.perform_analysis()

    # embedded profiler
    # import profile
    # profile.run('main.perform_analysis()', sort=1)
    #
    # pycallgraph, nice graph
    #from pycallgraph import PyCallGraph
    # from pycallgraph.output import GraphvizOutput

    # with PyCallGraph(output=GraphvizOutput()):
    #     main.perform_analysis()
