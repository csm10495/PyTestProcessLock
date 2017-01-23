import os
import pickle
import pytest
import socket
import sys
import timeit
from multiprocessing import Process

NUMBER_OF_PROCESSES = 64
MAX_SERIAL = 0 

SOCKETS_TO_PRE_SCAN = max(2, MAX_SERIAL + 2) # need 1 for the PRINT_PORT and other since we include 0 as a possible serial
PRINT_PORT = SOCKETS_TO_PRE_SCAN - 1

SERIAL_TO_PORT_FILE = 'S2P.pickle'

def run():
    p = Process(target=callPytest)
    p.start()
    return p

def callPytest():
    os.system('python -m pytest test.py -s')
     
def placeSerialToPorts():
    d = {}
    sockets = []
    for i in range(SOCKETS_TO_PRE_SCAN):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 0)
        sock.bind(server_address)
        port = sock.getsockname()[1]
        sockets.append(sock)
        d[i] = port
    
    for i in sockets:
        i.close()
     
    with open(SERIAL_TO_PORT_FILE, 'wb') as f:
        f.write(pickle.dumps(d))
    
def main():
    
    processes = []
    for i in range(NUMBER_OF_PROCESSES):
        processes.append(run())
        
    for i in processes:
        i.join()
        
    os.remove('S2P.pickle')

if __name__ == '__main__':
    stpTime = timeit.timeit(placeSerialToPorts, number=1)
    print ("Actual runtime took: %d second(s)" % (timeit.timeit(main, number=1)))
    print ("Time to generate S2P: %d second(s)" % stpTime)
