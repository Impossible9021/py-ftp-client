import os
import ftplib
from ftplib import FTP
from ftplib import FTP_TLS

def connect():
    print("------Connect------")
    mode = input("Use FTP or FTPS (default - FTP): ").lower()
    if (mode !="ftps" and mode !="ftp"):
        mode = "ftp"
        print("Using default protocol: FTP.")
    
    host = input("Address of server to connect(exit to quit): ")
    if (host == "exit"):
        exit()
    
    port = input("Port number(def for default): ")
    if (port != ""):
        port = int(port) #convert port to int without getting ValueError when it's empty

    user = input("User? (leave empty for anonymous login): ")
    if (user == ""):
        if (mode == "ftps"):
            shell(host, port, "", "", True)
        else:
            shell(host, port, "", "", False)
    else:
        passwd = str(input("Password: "))
        if (mode == "ftps"):
            shell(host, port, user, passwd, True)
        else:
            shell(host, port, user, passwd, False)
    

def parse(input_str):
    """ A parser of user input for shell(). Returns command and args """
    if (input_str == None or input_str == ""):
        cmd = ""
        arg = ""
    elif (input_str[:2] == "cd"):
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
    elif (input_str[:3] == "cmd"):
        cmd = "cmd"
        arg = input_str[4:]
    elif (input_str[:6] == "getbin"):
        cmd = "getbin"
        arg = input_str[6:]
    elif (input_str[:6] == "gettxt"):
        cmd = "gettxt"
        arg = input_str[6:]
    else:
        cmd = "unknown"
        arg = ""
    return cmd, arg

def shell(host, port, user, passwd, use_ftps):
    """ Shell Mode function. Provides a CLI to interact with FTP server """
    """ Args: host address, port number to connect, user[name] and passw[or]d to login, """
    """ use_ftps - if true use FTPS instead of FTP """
    #preparation: connect to the server
    try:
        if (use_ftps == True):
            if (user != ""): #if username defined ---> use it
                if (port == "def" or port == ""): #use default port 21
                    ftps = FTP_TLS(host=host, user=user, passwd=passwd)
                else:
                    ftps = FTP_TLS(host=host, user=user, passwd=passwd, acct=port)
            else: #anon login
                if (port == "def" or port == ""): #use default port 21
                    ftps = FTP_TLS(host=host)
                    ftps.login()
                else:
                    ftps = FTP_TLS(host=host, acct=port, user=user, passwd=str(passwd))
                    ftps.login()
            print("Connecting to host '{0}' through port '{1}'... ".format(host, port))
            
            os.system("echo Entering Shell Mode in 2 seconds")
            os.system("sleep 2")
            os.system("clear")
            print("Server response:\n" + ftp.getwelcome())
        
        if (use_ftps == False):
            if (user != ""): #if username defined ---> use it
                if (port == "def" or port == ""): #use default port 21
                    ftp = FTP(host=host, user=user, passwd=passwd)
                else:
                    ftp = FTP(host=host, user=user, passwd=passwd, acct=port)
            else: #anon login
                if (port == "def" or port == ""): #use default port 21
                    ftp = FTP(host=host)
                    ftp.login()
                else:
                    ftp = FTP(host=host, acct=port, user=user, passwd=str(passwd))
                    ftp.login()
            print("Connecting to host '{0}' through port '{1}'... ".format(host, port))
            
            os.system("echo Entering Shell Mode in 2 seconds")
            os.system("sleep 2")
            os.system("clear")
            print("Server response:\n" + ftp.getwelcome())
    except ftplib.all_errors as ex:
                print("An error occured while login: {0}".format(ex))
                return
        
    
    #enter shell mode
    while(1):
        try:
            if (use_ftps == False):

                cmd = input("ftp@{0}~#".format(host))
                cmd, arg = parse(cmd)
                if (cmd == "cd"):
                    ftp.cwd(arg)
                elif (cmd == "exit"):
                    ftp.quit()
                    return
                elif (cmd == "ls"):             #unix's LS without flags support
                    print(ftp.dir())
                elif (cmd == "cmd"):            #send a command to the server
                    ftp.sendcmd(arg)
                elif (cmd == "getbin"):         #download file in binary mode
                    ftp.retrbinary(arg)
                elif (cmd == "gettxt"):         #download file on text mode
                    ftp.retrlines(arg)
                elif (cmd == "unknown"):
                    print("Unknown command.")
        except ftplib.all_errors as ex:
                print("Shell mode error: {0}".format(ex))

def print_help():
    print("This is a little FTP client written in Python 3\n")
    print("---Connect---")
    print("Enter FTP server address and port.\n If you are going to use default port type 'def'\n\n")
    print("---Shell mode---")
    print("Usage is simular to bash/sh/zsh/whatever shell you are using.")
    print("Commands:")
    print("cd * - [C]hange (working) [D]irectory")
    print("getbin - Get a binary file from server")
    print("gettxt - Get a text file from server")
    print("exit - Quit the FTP connection\n\n")
    print("\n\n  LFTP v.0.1 by Impossible9021")
    print("See https://github.com/Impossible9021/py-ftp-client\n\n")




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
