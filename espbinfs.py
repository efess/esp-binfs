import sys
import getopt
from fsblobmaker import FsBlobMaker

class EspBinFS:

    @staticmethod
    def main(argv):
        options = EspBinFS.parse_arguments(argv)

        if options['usage']:
            EspBinFS.print_commandline_help()
            return

        blob_maker = FsBlobMaker()
        blob_maker.make_it(options)

    @staticmethod
    def print_commandline_help():
        print "Usage: espbinfs [options]"
        print "\n\t-h,--help \t\tprint this help and exit"
        print "\t-p,--path\t\troot path to file system contents"
        print "\t-m,--max-size\t\tMaximum size of flash "
        print "\t-o,--output\t\tOutput file "

    @staticmethod
    def parse_arguments(args):
        try:
            parsed_opts, parsed_args = getopt.getopt(args, "hmp:", ["help", "max-size=", 'path='])
            parsed_opts, parsed_args = getopt.getopt(args, "ho:m:p:", ["help","output=", "max-size=", 'path='])
        except getopt.GetoptError as ex:
            print ex.msg
            exit(1)

        # defaults
        options = {
            'usage': False,
            'path': './',
            'max_size': 524288,  # 512Kb
            'output': "espbinfs.bin"
        }

        for opt, arg in parsed_opts:
            if opt in ('-h', '--help'):
                options['usage'] = True
            if opt in ('-m', '--max-size'):
                options['max_size'] = arg
            if opt in ('-p', '--path'):
                options['path'] = arg
            if opt in ('-o', '--output'):
                options['output'] = arg

        return options

if __name__ == '__main__':
    raise SystemExit(EspBinFS.main(sys.argv[1:]))