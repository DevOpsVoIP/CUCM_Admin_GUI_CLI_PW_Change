import csv
import paramiko
from paramiko_expect import SSHClientInteraction
import paramiko_expect
import sys
from datetime import datetime


# Define function which is responsible for opening SSH connection and running specified commands
def ChangeGUIPW(ip, username, oldpassword, newpassword):
    command = "utils reset_application_ui_administrator_password"
    sshsession = paramiko.SSHClient()
    sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshsession.connect(ip, username=username, password=oldpassword)
    # "display=True" is just to show you what script does in real time. While in production you can set it to False
    interact = SSHClientInteraction(sshsession, timeout=600, display=True)
    # program will wait till session is established and CUCM returns admin prompt
    interact.expect('admin:')
    interact.send(command)
    interact.expect('.*password:.*')
    interact.send(newpassword)
    interact.expect('.*Password:.*')
    interact.send(newpassword)
    interact.expect('admin:')
    interact.send('exit')
    output = interact.current_output # program saves output of show status command to the "output" variable
    with open("ChangeLog.txt", 'a') as outfile:
        lines = output.splitlines()
        last_line = lines[-1]
        outfile.write("{0} | CLI | {1} | {2} | {3}".format(datetime.now(), ip, newpassword, last_line))
        outfile.close()
    sshsession.close()

def ChangeCLIPW(ip, username, oldpassword, newpassword):
    command = "set password user admin"
    sshsession = paramiko.SSHClient()
    sshsession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshsession.connect(ip, username=username, password=oldpassword)
    # "display=True" is just to show you what script does in real time. While in production you can set it to False
    interact = SSHClientInteraction(sshsession, timeout=600, display=True)
    # program will wait till session is established and CUCM returns admin prompt
    # "display=True" is just to show you what script does in real time. While in production you can set it to False
    interact = SSHClientInteraction(sshsession, timeout=600, display=True)
    # program will wait till session is established and CUCM returns admin prompt
    interact.expect('admin:')
    interact.send(command)
    interact.expect('.*password:.*')
    interact.send(oldpassword)
    interact.expect('.*password:.*')
    interact.send(newpassword)
    interact.expect('.*password.*')
    interact.send(newpassword)
    interact.expect('admin:')
    interact.send('exit')
    output = interact.current_output  # program saves output of show status command to the "output" variable
    with open("ChangeLog.txt", 'a') as outfile:
        lines = output.splitlines()
        last_line = lines[-1]
        outfile.write("{0} | CLI | {1} | {2} | {3}".format(datetime.now(), ip , newpassword, last_line))
        outfile.close()
    sshsession.close()

def main():
    print()
    with open('input.csv', newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    ## print(your_list)
    for count in range(len(your_list)):
        print()
        print('##################################################################################')
        print(your_list[count][0] + ' ' + your_list[count][1])
        if your_list[count][0] == 'CLI':
            ChangeCLIPW(your_list[count][1], your_list[count][2], your_list[count][3], your_list[count][4])
        elif your_list[count][0] == 'GUI':
            ChangeGUIPW(your_list[count][1], your_list[count][2], your_list[count][3], your_list[count][4])

if __name__ == "__main__":
    main()
