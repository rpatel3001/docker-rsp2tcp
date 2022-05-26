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
        rateb = pack(">ci", b"\x02", rate)
        rates = ' '.join('{:02x}'.format(x) for x in rateb)
        print("Setting sample rate to: %d (%s)"%(rate,rates))
        sock.sendall(rateb)
    except KeyError:
        print("Missing RATE env var!")
        exit(1)

    try:
        freq = int(environ["FREQ"])
        freqb = pack(">ci", b"\x01", freq)
        freqs = ' '.join('{:02x}'.format(x) for x in freqb)
        print("Setting center frequency to: %d (%s)"%(freq,freqs))
        sock.sendall(freqb)
    except KeyError:
        print("Missing FREQ env var!")
        exit(1)

    try:
        ppm = int(environ["PPM"])
        ppmb = pack(">ci", b"\x05", ppm)
        ppms = ' '.join('{:02x}'.format(x) for x in ppmb)
        print("Setting frequency correction to: %d (%s)"%(ppm,ppms))
        sock.sendall(ppmb)
    except KeyError:
        pass

    try:
        lna = int(environ["LNA"])
        lnab = pack(">ci", b"\x20", lna)
        lnas = ' '.join('{:02x}'.format(x) for x in lnab)
        print("Setting LNA state to: %d (%s)"%(lna,lnas))
        sock.sendall(lnab)
    except KeyError:
        pass

    try:
        ifgr = int(environ["IFGR"])
        ifgrb = pack(">ci", b"\x21", ifgr)
        ifgrs = ' '.join('{:02x}'.format(x) for x in ifgrb)
        print("Setting IFGR to: %d (%s)"%(ifgr,ifgrs))
        sock.sendall(ifgrb)
    except KeyError:
        pass

    try:
        gain_index = int(environ["GAIN_INDEX"])
        gain_indexb = pack(">ci", b"\x21", gain_index)
        gain_indexs = ' '.join('{:02x}'.format(x) for x in gain_indexb)
        print("Setting IFGR to: %d (%s)"%(gain_index,gain_indexs))
        sock.sendall(gain_indexb)
    except KeyError:
        pass

    try:
        agc = int(environ["AGC"])
        agcenb = pack(">ci", b"\x22", 1)
        agcens = ' '.join('{:02x}'.format(x) for x in agcenb)
        agcb = pack(">ci", b"\x23", agc)
        agcs = ' '.join('{:02x}'.format(x) for x in agcb)
        print("Enabling AGC with setpoint at: %d (%s, %s)"%(agc,agcens,agcs))
        sock.sendall(agcenb)
        sock.sendall(agcb)
    except KeyError:
        agcenb = pack(">ci", b"\x22", 1)
        agcens = ' '.join('{:02x}'.format(x) for x in agcenb)
        print("Disabling AGC (%s)"%(agcens))
        sock.sendall(agcenb)

while True:
    sleep(86400)