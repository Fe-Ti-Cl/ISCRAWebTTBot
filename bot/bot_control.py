#!/usr/bin/python3
# Copyright 2023 Fe-Ti aka T.Kravchenko
import socket
import json
from sys import argv
from pathlib import Path

def load_json(path):
    with open(path) as ifile:
        dictionary = json.loads(ifile.read())
    return dictionary

c_reload = "reload"
c_recompile = "recompile"
c_stop = "stop"
c_start = "start"
c_shutdown = "shutdown"
c_exit = "exit"

if __name__ == '__main__':

    cfg_filename = "config.json"
    if len(argv) > 1:
        for n, key in enumerate(argv):
            if "-c" == key:
                try:
                    cfg_filename = argv[n + 1]
                except:
                    print("Parameter -c requires argument.")
                    exit(1)
            elif n == 0:
                command = argv[1]
            elif argv[n-1] != "-c":
                command = argv[1]
            else:
                print("Usage: bot -c CFG_FILE COMMAND")
                exit(1)
    else:
        print("""Specify command:
    start       - start bot operation
    stop        - stop bot operation
    recompile   - recompile scenery from python source into json
    reload      - reload scenery from json and its API
    shutdown    - stop bot and save user database
    exit        - stop bot and exit control daemon process
""")
        exit()

    if Path(cfg_filename).exists():
        config = load_json(cfg_filename)
    else:
        print(f"Can't find config file. Please place it as '{cfg_filename}'")
        exit(1)
    
    HOST = config["address"] # Symbolic name meaning all available interfaces
    PORT = config["port"] # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes(command, "ascii"))
        data, _, _, _ = s.recvmsg(1024)
    print('Received', repr(data))
