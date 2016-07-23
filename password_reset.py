#!/usr/bin/env python3
import configparser
import simplecrypt
import getpass
import sys

def get_file_path(username):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    for section in config.sections():
        if(config.get(section, 'username') == username):
            return config.get(section, 'file')
    print(username + ' is not a valid username!')
    sys.exit()

def get_passwords():
    oldpassword = getpass.getpass('Enter old password: ')
    newpassword = getpass.getpass('Enter new password: ')
    _newpassword = getpass.getpass('Enter new password again: ')
    if newpassword == _newpassword:
        return oldpassword, newpassword
    else:
        print('Passwords does not match!')
        get_passwords()

if __name__ == '__main__':
    print('---------------------------------')
    print('Password reset tool for Segreto 3')
    print('---------------------------------')
    username = input('Enter your username: ')
    filepath = get_file_path(username)
    oldpassword, newpassword = get_passwords()
    print('Please wait...')
    with open(filepath, 'rb') as infile:
        filedata = infile.read()
    try:
        data = simplecrypt.decrypt(oldpassword, filedata)
    except simplecrypt.DecryptionException:
        print('Old password is wrong')
        sys.exit()
    filedata = simplecrypt.encrypt(newpassword, data)
    with open(filepath, 'wb') as outfile:
        outfile.write(filedata)
    print('Password changed!')
