from os import environ
import socket
import atexit
import SoapySDR
from SoapySDR import *
import numpy

try:
    args = dict(kv.split("=") for kv in environ["SOAPY"].split(","))
    print("Opening SoapySDR device with parameters: %s"%args)
    sdr = SoapySDR.Device(args)
except KeyError:
    print("Missing SOAPY env var!")
    exit(1)

try:
    rate = float(environ["RATE"])
    print("Setting sample rate to: %f"%rate)
    sdr.setSampleRate(SOAPY_SDR_RX, 0, rate)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, rate)
except KeyError:
    print("Missing RATE env var!")
    exit(1)

try:
    freq = float(environ["FREQ"])
    print("Setting center frequency to: %f"%freq)
    sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
except KeyError:
    print("Missing FREQ env var!")
    exit(1)

try:
    ppm = float(environ["PPM"])
    print("Setting frequency correction to: %f"%ppm)
    sdr.setFrequencyCorrection(SOAPY_SDR_RX, 0, ppm)
except KeyError:
    pass

try:
    bw = float(environ["BANDWIDTH"])
    print("Setting filter bandwidth to: %f"%bw)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bw)
except KeyError:
    pass

try:
    if environ["GAIN"] == "agc":
        sdr.setGainMode(SOAPY_SDR_RX, 0, True)
    else:
        sdr.setGainMode(SOAPY_SDR_RX, 0, False)
        try:
            gain = float(environ["GAIN"])
            print("Setting gain to: %f"%gain)
            sdr.setGain(SOAPY_SDR_RX, 0, gain)
        except ValueError:
            gains = dict(kv.split("=") for kv in environ["GAIN"].split(","))
            for g in gains.keys():
                print("Setting gain %s to: %f"%(g, float(gains[g])))
                sdr.setGain(SOAPY_SDR_RX, 0, g, float(gains[g]))
except KeyError:
    pass

rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS16)
atexit.register(sdr.closeStream, rxStream)

mtu = sdr.getStreamMTU(rxStream)
print("Using stream MTU: %d"%mtu)

buff = numpy.array([0]*mtu*2, numpy.int16)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 1234))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print(f"Connection accepted from {addr}")

        conn.sendall(b"RTL0\x00\x00\x00\x00\x00\x00\x00\x00")

        sdr.activateStream(rxStream)
        atexit.register(sdr.deactivateStream, rxStream)

        while True:
            status = sdr.readStream(rxStream, [buff], mtu)
            if status.ret < 0:
                print("failed to read stream: %s"%status)
                exit(1)
            conn.sendall(((buff[:2*status.ret].astype(numpy.int32)+32768)/256).astype(numpy.uint8))
