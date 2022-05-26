from lib2to3.pytree import Base
from os import environ
from struct import pack
from time import sleep
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.settimeout(5)
    connected = False
    while not connected:
        try:
            sock.connect(("127.0.0.1", 7373))
            connected = True
        except BaseException:
            pass

    sock.settimeout(None)
    print(f"Connection made with rsp_tcp server at 127.0.0.1:7373")

    try:
        rate = int(environ["RATE"])
        print("Setting sample rate to: %d"%rate)
        sock.sendall(pack(">ci", b"\x02", rate))
    except KeyError:
        print("Missing RATE env var!")
        exit(1)

    try:
        freq = int(environ["FREQ"])
        print("Setting center frequency to: %d"%freq)
        sock.sendall(pack(">ci", b"\x01", freq))
    except KeyError:
        print("Missing FREQ env var!")
        exit(1)

    try:
        ppm = int(environ["PPM"])
        print("Setting frequency correction to: %d"%ppm)
        sock.sendall(pack(">ci", b"\x05", ppm))
    except KeyError:
        pass

    try:
        lna = int(environ["LNA"])
        print("Setting LNA state to: %d"%lna)
        sock.sendall(pack(">ci", b"\x20", lna))
    except KeyError:
        pass

    try:
        ifgr = int(environ["IFGR"])
        print("Setting IFGR to: %d"%ifgr)
        sock.sendall(pack(">ci", b"\x21", ifgr))
    except KeyError:
        pass

    try:
        agc = int(environ["AGC"])
        print("Enabling AGC with setpoint at: %d"%agc)
        sock.sendall(pack(">ci", b"\x22", 1))
        sock.sendall(pack(">ci", b"\x23", agc))
    except KeyError:
        sock.sendall(pack(">ci", b"\x22", 0))

while True:
    sleep(86400)