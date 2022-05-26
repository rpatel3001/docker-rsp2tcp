# docker-rsptcp
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rpatel3001/docker-rsptcp/Deploy%20to%20ghcr.io)](https://github.com/rpatel3001/docker-rsptcp/actions/workflows/deploy.yml)
[![Discord](https://img.shields.io/discord/734090820684349521)](https://discord.gg/sTf9uYF)

A Docker image to expose an SDRplay device as an rtl_tcp compatible stream using rsp_tcp, with rtlmuxer interposed to allow multiple clients to consume the same data.

Note: This has only been tested with an AliExpress clone of an SDRplay RSP1.

---

## Up and running

```
version: '3'

services:
  soapy2tcp:
    container_name: soapy2tcp
    hostname: soapy2tcp
    image: ghcr.io/rpatel3001/docker-soapy2tcp
    restart: always
    ports:
      - 7374:7374
    volumes:
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/bus/usb
    environment:
      - RATE=9450000
      - FREQ=134000000
      - AGC=-30
```

## Configuration options

| Variable | Description | Required | Default |
|----------|-------------|---------|--------|
| `RATE` | Sampling rate to set. | No | Unset |
| `FREQ` | Frequency to tune to. | No | Unset |
| `PPM` | PPM frequency correction to set. | No | `0` |
| `AGC` | Set this to a setpoint value to enable AGC. | No | Unset |
| `LNA` | LNA state to set. | No | Unset |
| `IFGR` | IF gain reduction to set (does nothing if AGC is enabled). | No | Unset |
| `TCP_PORT` | Port where rtlmuxer will accept requests. | No | `7374` |
