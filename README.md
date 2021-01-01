# POCDAB

This repository contains a receiver, which is able to receive arbitrary DAB+ packages.

## Requirements

The required libraries can be automatically installed via the build.sh file, and consist of:

librtlsdr-dev
fftw3
git
g++
cmake
autoconf
libasio-dev
gnuradio-dev
libboost-dev
libtins-dev
pkg-config

## Building
```
$ git clone https://github.com/chissie13/POCDAB.git
$ cd POCDAB
$ ./build.sh
```
The resulting binaries can be found in `<build-directory>/products/Release/bin`

## Running

Per default, the packager packages the incoming data in way that makes it look
like it comes from `10.0.0.2` and goes to `10.0.0.1`. It also sets `1000` as
the DAB packet address. Thus you need to make sure to pass `10.0.0.1` and
`1000` as the `receiver`s arguments.

### Receiver
Running the receiver requires an SDR device compatible with **librtlsdr**.
The receiver requires **root** access to create the virtual network device:
```
$ ./run.sh
```

### Receiving data
On the machine that is running the receiver, you will simply listen on the address of the virtual network
interface for UDP datagrams on the port specified in the packager
(default 4242):
```
$ python receive.py
```
