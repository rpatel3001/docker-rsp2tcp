from os import environ
import socket
import atexit
import SoapySDR
from SoapySDR import *
import numpy

args = dict(kv.split("=") for kv in environ["SOAPY"].split(","))
print("Opening SoapySDR device with parameters: %s"%args)
sdr = SoapySDR.Device(args)

rate = float(environ["RATE"])
print("Setting sample rate to: %f"%rate)
sdr.setSampleRate(SOAPY_SDR_RX, 0, rate)
sdr.setBandwidth(SOAPY_SDR_RX, 0, rate)

freq = float(environ["FREQ"])
print("Setting center frequency to: %f"%freq)
sdr.setFrequency(SOAPY_SDR_RX, 0, freq)

ppm = float(environ["PPM"])
print("Setting frequency correction to: %f"%ppm)
sdr.setFrequencyCorrection(SOAPY_SDR_RX, 0, ppm)

if environ["GAIN"] == "agc":
    sdr.setGainMode(SOAPY_SDR_RX, 0, True)
else:
    gain = float(environ["GAIN"])
    print("Setting gain to: %f"%gain)
    sdr.setGainMode(SOAPY_SDR_RX, 0, False)
    sdr.setGain(SOAPY_SDR_RX, 0, gain)

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
            conn.sendall((buff[:2*status.ret].astype(numpy.int16)+128).astype(numpy.uint8))
