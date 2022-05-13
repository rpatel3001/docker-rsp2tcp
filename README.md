# docker-soapy2tcp
A Docker image to expose any SoapySDR compatible device as an rtl_tcp stream, with rtlmuxer interposed to allow multiple clients to consume the same data.

Note: This has only been tested with an RTL-SDR device.

---

## Up and running

```
version: '3'

services:
  soapy2tcp:
    container_name: soapy2tcp
    hostname: soapy2tcp
    build: ghcr.io/rpatel3001/docker-soapy2tcp
    restart: always
    ports:
      - 7374:7374
    volumes:
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/bus/usb
    environment:
      - SOAPY=driver=rtlsdr,serial=00000136
      - RATE=2310000
      - FREQ=136000000
      - PPM=35
      - GAIN=40.2
```

## Configuration options

| Variable | Description | Required | Default |
|----------|-------------|---------|--------|
| `SOAPY` | The SoapySDR device string you would pass to `SoapySDRUtil --find` to list your device. | Yes | Unset |
| `RATE` | Sampling rate to set. | No | `2100000` |
| `FREQ` | Frequency to tune to. | No | `133000000` |
| `PPM` | PPM frequency correction to set. | No | `0` |
| `GAIN` | Numerical gain to set. If this is set to the string `agc`, automatic gain control will be enabled (the default). | No | `agc` |
| `TCP_PORT` | Port where rtlmuxer will accept requests. | No | `7374` |
