import pickle
import socket
from config import WOL_PORT
import time


def load_store():
    try:
        with open('../store.pkl', 'rb') as f:
            store = pickle.load(f)
    except (FileNotFoundError, EOFError):
        store = {}
    return store


def write_store(store):
    with open('../store.pkl', 'wb') as f:
        pickle.dump(store, f)


def send_wol_packet(mac_address, attempts=3, delay=1):
    mac_address = ''.join(mac_address.split(':'))
    data = 'FF' * 6 + mac_address * 16
    magic_packet = bytes.fromhex(data)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for _ in range(attempts):
            sock.sendto(magic_packet, ('255.255.255.255', WOL_PORT))
            time.sleep(delay)
