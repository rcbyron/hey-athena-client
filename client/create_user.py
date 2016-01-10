'''
Created on Jan 9, 2016

@author: Connor
'''
import os, yaml
import client.settings as settings

def safe_input(prompt):
    answer = '(none)'
    confirm = 'N'
    while (len(confirm) < 1 or confirm.upper()[0] is not 'Y'):
        answer = input(prompt)
        print("\n~ Input:", answer)
        confirm = input("~ Confirm (Y / N): ")
        print()
    return answer

def generate():
    print("#########################################")
    print("#                                       #")
    print("#    USER CONFIG FILE GENERATOR 2000    #")
    print("#                                       #")
    print("#########################################")
    print("\n~ Please let me learn some things about you :)")
    print("\n~ All of the following is optional, of course.\n")
    user_info = {}
    print("** Username will be used as the .yml file name\n")
    user_info['username'] = safe_input("Username: ")
    user_info['full-name'] = safe_input("Full Name: ")
    user_info['nickname'] = safe_input("Nickname: ")
    user_info['phone'] = safe_input("Phone Number: ")
    user_info['email'] = safe_input("Email: ")
    file_loc = os.path.join(settings.USERS_DIR, user_info['username']+".yml")
    print("~ Writing to:", file_loc)
    with open(file_loc, 'w') as f:
        yaml.dump(user_info, f, default_flow_style=False)
    print("~ Success! Feel free to boot me up now.")
        
generate()