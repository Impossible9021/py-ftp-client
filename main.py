import os
import ftplib
from ftplib import FTP

def connect():
    print("------Connect------")
    host = input("Address of server to connect(exit to quit): ")
    
    if (host == "exit"):
        exit()
    
    port = input("Port number(def for default): ")
    shell(host, port)

def parse(input_str):
    """ A parser of user input for shell(). Returns command and args """
    if (input_str == None or input_str == ""):
        cmd = ""
        arg = ""
    elif (input_str[0] == 'c') and (input_str[2] == 'd'):
        """ cd command """
        cmd = "cd"
        if (len(input_str) == 2):
            cmd = "cd"
            arg = ""
        else:
            arg = input_str[3:] # to ignore space
    elif (input_str == "exit"):
        cmd = "exit"
        arg = ""
    elif (input_str == "ls"):
        cmd = "ls"
        arg = ""
    else:
        cmd = "unknown"
        arg = ""
    return cmd, arg

def shell(host = "", port = ""):
    """ Shell Mode function. Provides a CLI to interact with FTP server """
    #preparation: connect to the server
    try:
        if (port == "def" or port == "" or port == None):
            ftp = FTP(host)
        else:
            ftp = FTP(host, port)
        ftp.login() # anon login only in this version
        os.system("echo Entering Shell Mode in 3 seconds")
        os.system("sleep 3")
        os.system("clear")
    except ftplib.all_errors as ex:
        print("An error occured while login: {0}".format(ex))
        return
    print("Server response: " + ftp.getwelcome())
    
    #enter shell mode
    while(1):
        cmd = input("ftp@{0}~#".format(host))
        cmd, arg = parse(cmd)
        if (cmd == "cd"):
            try:
                ftp.cwd(arg)
            except ftplib.all_errors as ex:
                print("Can't cd: {0}".format(ex))
        if (cmd == "exit"):
            ftp.quit()
            return
        if (cmd == "ls"):
            print(ftp.retrlines('LIST'))
        if (cmd == "unknown"):
            print("Unknown command.")

def print_help():
    print("This is a little FTP client written in Python 3\n")
    print("---Connect---")
    print("Enter FTP server address and port.\n If you are going to use default port type 'def'")
    print("---Shell mode---")
    print("Usage is simular to bash/sh/zsh/whatever shell you are using.")
    print("Commands:")
    print("cd * - [C]hange (working) [D]irectory")
    print("upf * - [Up]load a [F]ile to the server")
    print("exit - Quit the FTP connection")

print("Welcome to PFTP - a little Python FTP Client for Linux")

while (1):
    action = input("[C]onnect | [H]elp | [E]xit?").lower()
    if (action == "c"):
        connect()
        break
    elif (action == "h"):
        print_help()
        break
    else:
        print("Invalid input: {0}".format(action))
        print("[C]onnect | [H]elp | [E]xit?")
