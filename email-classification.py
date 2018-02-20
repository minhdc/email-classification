from argparse import ArgumentParser, FileType
from email import message_from_file
import os
import quopri
import base64

__description__ = "Util to parse header from EML files"
__authors__ = "Minh Dinh"
__date__ = 111111


def get_eml_header(input_file):
    return message_from_file(input_file)._headers


def print_full_header(eml_header):
    for key, value in eml_header:
        print(" {} : {} ".format(key,value))


def get_value_by_key(eml_header,key_to_search):
    for key,value in eml_header:
        if key == key_to_search:
            return value
    return None    


def main(input_file):
    
    eml_header = get_eml_header(input_file)

    

if __name__ == '__main__':
    parser = ArgumentParser(
        description = __description__,
        epilog = "developed by {} on {}".format(", ".join(__authors__),__date__)
    )
    parser.add_argument("EML_FILE",help = "Path to EML File", type=FileType('r'))
    args = parser.parse_args()
    
    main(args.EML_FILE)
