import os
import ftplib
from ftplib import FTP
from ftplib import FTP_TLS

class color:
    red = "\033[0;31m"
    green = "\033[0;32m"
    blue = "\033[0;34m"
    std = "\033[0m"

# Vars
host = "0"
user = "0"
passwd = "0"
port = "0"
use_ftps = "0"

# Functions

def read_config():
    """
    This function reads the config.
    If it doesn't exist it creates one with default settings and runs using them.
    If the conf file is disabled or its creation had failed, it also runs with default settings
    """
    
    global host
    global user
    global passwd
    global port
    global use_ftps
    
    #reading config
    try:
        conf = open("$HOME/.pftp_config", 'r')
        options = conf.readlines()
        conf.close()
        if (options[0] != "use_config=y"):
            print ("Config file is turned off [.pftp_config]. Using prompting. Returnning...")
            #all vars are "0" so manual input will be required
            return
        if (len(options) < 6):
            print("Config file was corrupt. PFTP will create it and use default settings")
            try:
                system("rm -f $HOME/.pftp_config")
                defaults = ["use_config=y\n", "host=0\n", "user=0\n", "passwd=0\n", "port=0\n", "use_ftps=0"]
                conf = open("$HOME/.pftp_config", 'x')
                conf.writelines(defaults)
                conf.close()
            except OSError as ex:
                print(color.red + "An error happened when creating config file. Using prompting. Returning..." + color.std)
                return
        
        #if alright, setting the vars
        host = str(options[0])
        user = str(options[1])
        passwd = str(options[2])
        port = str(options[3])
        #exclude 'parameter='-like substrings and '\n'
        host = host[5:-1]
        user = user[5:-1]
        passwd = passwd[8:-1]
        port = options[4:-1]
    
    except (IOError, OSError) as ex: #on some systems with old Python3  IOError != OSError
        print(color.red + "[Error]" + color.std + "File not found or no rights to read")
        print("Using defaults")
        return
        #all vars are still "0"

def connect():
    """
    This function connects the client to the specified server and calls shell()
    Before connection it checks the if all the required vars are set
    If some a var is not set it prompts user for value
    """
    
    global host
    global user
    global passwd
    global port
    global use_ftps
    
    print("------Connect------")
    
    use_config = input("Do you want to use the config? [y/n]")
    if (use_config == "y"):
        read_config()
    
    if (use_ftps == "0"):
        use_ftps = input("Use FTPS instead of FTP? (default - use FTP)[y/n]: ").lower()
    if (use_ftps != "ftps" and use_ftps != "ftp"):
        use_ftps = "ftp"
        print("Using default protocol: FTP.")
    
    if (host == "0"):
        host = input("Address of server to connect(exit to quit): ")
        if (host == "exit"): #foolproof: imagine this would always run and conf file would set "host=exit" :)
            exit()
    
    if (port == "0"):
        port = input("Port number(def for default): ")
    
    try:
        if (port != ""):
            port = int(port) #convert port to int without getting ValueError when it's empty
    except ValueError:       #but if the value is like "ololo" we'll still get ValueError
        port = 21            #so we set it to default port from FTP spec
        print(color.red + "Invalid port received from stdin or conf. Using default 21" + color.std)

    if (user == "0"):
        user = input("User? (leave empty for anonymous login): ")
    if (user == ""):
        if (use_ftps == "y"):
            shell(host, port, "", "", "y")
        else:
            shell(host, port, "", "", "n")
    else:
        passwd = str(input("Password: "))
        if (use_ftps == "y"):
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
        cmd = "getbin"
        arg = input_str[6:]
    elif (input_str[:6] == "gettxt"):
        cmd = "gettxt"
    elif (input_str[:6] == "getbin"):
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
        if (use_ftps == "y"):
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
        
        if (use_ftps == "n"):
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
                print(color.red + "An error occured while login: {0}".format(ex) + color.std)
                return
        
    
    #enter shell mode
    while(1):
        try:
            if (use_ftps == "n"):
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
            
            else: #FTPS
                cmd = input("ftps@{0}~#".format(host))
                cmd, arg = parse(cmd)
                if (cmd == "cd"):
                    ftps.cwd(arg)
                elif (cmd == "exit"):
                    ftps.quit()
                    return
                elif (cmd == "ls"):             #unix's LS without flags support
                    print(ftps.dir())
                elif (cmd == "cmd"):            #send a command to the server
                    ftps.sendcmd(arg)
                elif (cmd == "getbin"):         #download file in binary mode
                    ftps.retrbinary(arg)
                elif (cmd == "gettxt"):         #download file on text mode
                    ftps.retrlines(arg)
                elif (cmd == "unknown"):
                    print("Unknown command.")
            
        except ftplib.all_errors as ex:
                print(color.red + "Shell mode error: {0}".format(ex) + color.std)

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
    print("---Config---")
    print("The config file is situated at $HOME/.pftp_config")
    print("use_config - if set to n the prog will always ask you to enter the values")
    print("host - an address to the server to connect")
    print("user - username to use for connection")
    print("password - password to use for the connection")
    print("port - port to connect\n\n")
    print("---Credits---")
    print("\n\n  LFTP v.0.2 by Impossible9021")
    print("See https://github.com/Impossible9021/py-ftp-client\n\n")


# Entry point

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
