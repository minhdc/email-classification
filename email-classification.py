'''
    1. get header
    2. get @From field, save as folder name
    3. check if folder name existence:
        1: check if email exists
        0: create folder
    4. copy email to corresponding folder
'''
from argparse import ArgumentParser, FileType
from email import message_from_file
import os
import quopri
import base64
import shutil
__description__ = "Util to classify email"
__authors__ = "Minh Dinh"
__date__ = 111111

#constant


def get_list_of_incoming_emails(current_eml_path):
    email_list = []
    for each_element in os.listdir():
        if each_element.endswith(".eml"):
            email_list.append(each_element)
    if not email_list:
        return None
    return email_list


def get_eml_header(input_file_path):
    '''
        return full email_header in input_file
    '''
    input_file_as_path = open(input_file_path,"r")
    return message_from_file(input_file_as_path)._headers


def print_full_header(eml_header):
    for key, value in eml_header:
        print(" {} : {} ".format(key,value))


def get_value_by_key(eml_header,key_to_search):
    '''
        return value of key_to_search,
        return None if not found
    '''
    for key,value in eml_header:
        if key == key_to_search:
            return value
    return None


def get_email_from_obfuscated_string(obfuscated_string):
    '''
        extract email_address from a obfuscated string
        email should be wrapped between < and >
        return None if notfound
    '''
    email_address = []
    start_point = obfuscated_string.index("<")+1
    stop_point = obfuscated_string.index(">")
    for i in range(start_point,stop_point):
        email_address.append(obfuscated_string[i])

    if not email_address:
        print("\n[ERR]none email address found in input string\n")
        return None
    return ''.join(email_address)


def create_email_storing_folder_if_not_exists(folder_name,folder_path):
    '''
        create a folder to store email from a specific address
        folder_name = @From field in eml-header
    '''
    absolute_path_to_folder = folder_path + os.sep + folder_name
    if os.path.isdir(absolute_path_to_folder):
        print("folder %s already exists"%folder_name)
        #check for duplicated file and copy
    else:
        os.mkdir(absolute_path_to_folder)
        print("newly created folder %s "%folder_name)


def copy_email_to_storing_folder(src,dst,email_file_name):
    '''
        if email doestn't exist in storing folder, copy it
    '''
    #check if email exists
    if not os.path.isfile(open(dst + os.sep + email_file_name,"r")):
        shutil.copy2(src,dst + os.sep + email_file_name)
        print("successfully copied new email file")
    else:
        print("email file: %s already exist "%(email_file_name))


def move_copied_email_to_treasure(src,treasure_name,dst = None):
    '''
        move copied email to treasure, if exists, delete it
    '''
    if dst is not None:
        if not os.path.isfile(dst + os.sep + treasure_name):
            shutil.move(src + os.sep + treasure_name, dst + os.sep + treasure_name)
        else:
            os.remove(src + os.sep + treasure_name)
    else:
        if not os.path.isfile(open(dst + os.sep + treasure_name,"r")):
            shutil.move(src + os.sep + treasure_name, dst + os.sep + treasure_name)
        else:
            os.remove(src + os.sep + treasure_name)


def main(path):
    current_path = path
    treasure_name = "treasure"
    eml_key_to_search = "From"

    print("current emails in %s:"%path)
    email_list = get_list_of_incoming_emails(current_path)
    print(email_list)

    for each_mail in email_list:
        eml_header = get_eml_header(current_path + os.sep + each_mail)
        from_addr = get_email_from_obfuscated_string(get_value_by_key(eml_header,eml_key_to_search))
        create_email_storing_folder_if_not_exists(from_addr,current_path)
        copy_email_to_storing_folder(current_path, current_path + os.sep + from_addr,each_mail )
        move_copied_email_to_treasure(current_path,current_path + os.sep + treasure_name)





if __name__ == '__main__':
    parser = ArgumentParser(
        description = __description__,
        epilog = "developed by {} on {}".format(", ".join(__authors__),__date__)
    )
    parser.add_argument("EML_FILE",help = "Path to EML File")
    args = parser.parse_args()

    main(args.EML_FILE)
