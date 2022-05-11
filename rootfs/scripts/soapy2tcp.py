from os import environ
import socket
import atexit
import SoapySDR
from SoapySDR import *
import numpy

args = dict(kv.split("=") for kv in environ["SOAPY"].split(","))
rate = float(environ["RATE"])
freq = float(environ["FREQ"])
ppm = float(environ["PPM"])
gain = float(environ["GAIN"])

print("Opening SoapySDR device with parameters: %s"%args)
sdr = SoapySDR.Device(args)

print("Setting sample rate to: %f"%rate)
sdr.setSampleRate(SOAPY_SDR_RX, 0, rate)

print("Setting center frequency to: %f"%freq)
sdr.setFrequency(SOAPY_SDR_RX, 0, freq)

print("Setting frequency corection to: %f"%ppm)
sdr.setFrequencyCorrection(SOAPY_SDR_RX, 0, ppm)

print("Setting gain to: %f"%gain)
sdr.setGain(SOAPY_SDR_RX, 0, gain)

rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CS8)
atexit.register(sdr.closeStream, rxStream)

mtu = sdr.getStreamMTU(rxStream)
print("Using max stream MTU: %d"%mtu)

buff = numpy.array([0]*mtu*2, numpy.uint8)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(("127.0.0.1", 1234))
    sock.listen()
    conn, addr = sock.accept()
    with conn:
        print(f"Connection accepted from {addr}")

        conn.sendall(str.encode("RTL0________"))

        sdr.activateStream(rxStream)
        atexit.register(sdr.deactivateStream, rxStream)

        while True:
            sdr.readStream(rxStream, [buff], len(buff))
            conn.sendall(buff)

#for i in range(10):
#    sr = sdr.readStream(rxStream, [buff], len(buff))
#    print(sr.ret) #num samples or error code
#    print(sr.flags) #flags set by receive operation
#    print(sr.timeNs) #timestamp for receive buffer
