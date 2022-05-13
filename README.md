# docker-soapy2tcp
A Docker image to expose any SoapySDR compatible device as an rtl_tcp stream, with rtlmuxer interposed to allow multiple clients to consume the same data.

Note: This has only been tested with an RTL-SDR device.

---

## Configuration options

| Variable | Description | Required | Default |
|----------|-------------|---------|--------|
| `SOAPY` | The SoapySDR device string you would pass to `SoapySDRUtil --find` to list your device. | Yes | Unset |
| `RATE` | Sampling rate to set. | No | `2100000` |
| `FREQ` | Frequency to tune to. | No | `133000000` |
| `PPM` | PPM frequency correction to set. | No | `0` |
| `GAIN` | Numerical gain to set. If this is set to the string `agc`, automatic gain control will be enabled (the default). | No | `agc` |
| `TCP_PORT` | Port where rtlmuxer will accept requests. | No | `7374` |
