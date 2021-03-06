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
    '''
        return a list of email in a specified folder path
    '''
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
    if os.path.isdir(os.path.join(folder_path,folder_name)):
        print("folder %s already exists"%folder_name)
        #check for duplicated file and copy
    else:
        os.mkdir(os.path.join(folder_path,folder_name))
        print("newly created folder %s "%folder_name)


def copy_email_to_storing_folder(src,dst,email_file_name):
    '''
        if email doestn't exist in storing folder, copy it
    '''
    #check if email exists
    if not os.path.isfile(os.path.join(dst,email_file_name)):
        try:
            shutil.copy2(os.path.join(src,email_file_name),os.path.join(dst,email_file_name))
            print("successfully copied new email file")
        except shutil.Error as e:
            print("duplicated file ",email_file_name)
    else:
        print("email file: %s already exist "%(email_file_name))


def move_copied_email_to_treasure(src,treasure_name,email_file_name,dst = None):
    '''
        move copied email to treasure, if exists, delete it
    '''
    create_email_storing_folder_if_not_exists(treasure_name,src)
    if dst is not None:
        if not os.path.isfile(dst + os.sep + treasure_name):
            try:
                shutil.move(os.path.join(src,email_file_name),os.path.join(dst,treasure_name))
            except shutil.Error as e:
                print("duplicated file~!",email_file_name   )
    else:
        if not os.path.isdir(os.path.join(src+ os.sep + treasure_name)):
            try:
                shutil.move(os.path.join(src,email_file_name),os.path.join(src,treasure_name))
            except shutil.Error as e:
                print("duplicated file~!",email_file_name)

def get_email_object(path_to_eml_file,file_name):
    return message_from_file(open(path_to_eml_file+os.sep+file_name,"r",encoding="ISO-8859-1"))


def extract_from_address_in_payload(email_object):
    '''
        extract value of 'from' address in the payload of provided email_obj
    '''
    start_point = 0
    stop_point = 0
    email_payload_as_string = email_object['From']

    #process the value of 'From' key in header
    print("raw value:",email_payload_as_string)
    try:
        start_point = email_payload_as_string.index('<')
        stop_point = email_payload_as_string.index('>')
    except ValueError as verr:
        return email_payload_as_string

    extracted_from_address = []
    for i in range(start_point+1,stop_point):
        extracted_from_address.append(email_payload_as_string[i])

    return ''.join(extracted_from_address)



def main(path):
    current_path = path
    treasure_name = "treasure"
    eml_key_to_search = "From"

    print("current emails in %s:"%path)
    try:
        email_list = get_list_of_incoming_emails(current_path)
        email_quantity = 0
        #print(email_list)

        for each_mail in email_list:
            #test the header
            #eml_header = get_eml_header(current_path + os.sep + each_mail)
            #print_full_header(eml_header)
            #print("====================")
            #from_addr = get_email_from_obfuscated_string(get_value_by_key(eml_header,eml_key_to_search))

            #test mail name
            from_addr = extract_from_address_in_payload(get_email_object(current_path,each_mail))
            #email_quantity += 1
            create_email_storing_folder_if_not_exists(from_addr,current_path)
            copy_email_to_storing_folder(current_path, os.path.join(current_path,from_addr), each_mail )
            move_copied_email_to_treasure(current_path,os.path.join(current_path,treasure_name),each_mail)
        print(email_quantity)
    except TypeError as err:
        print("empty email list")




if __name__ == '__main__':
    parser = ArgumentParser(
        description = __description__,
        epilog = "developed by {} on {}".format(", ".join(__authors__),__date__)
    )
    parser.add_argument("EML_FILE",help = "Path to EML File")
    args = parser.parse_args()

    main(args.EML_FILE)
