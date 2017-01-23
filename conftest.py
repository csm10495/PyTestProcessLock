import contextlib
import random
import time

from runner import *

@contextlib.contextmanager
def lock(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', port)
    while True:
        try:
            sock.bind(server_address)
            break
        except Exception as ex:
            time.sleep(.1)
    yield
    sock.close()

def safePrint(port, txt):
    with lock(port):
        sys.stderr.write(txt + "\n")

@pytest.fixture(scope='session')
def constantObj():
    name = random.randint(0, MAX_SERIAL) # randint is inclusive.
    with open(SERIAL_TO_PORT_FILE, 'rb') as f:
        d = pickle.loads(f.read())
    
    port = d[name]
    return {'serial' : name, 'port' : port, 'safePrint' : lambda txt: safePrint(d[PRINT_PORT], txt)}    

@pytest.fixture(scope='function')
def sync(constantObj):
    port = int(constantObj['port'])
    with lock(port):
        yield