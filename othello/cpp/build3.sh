#/usr/bin/env bash

BUILD_DIRECTORY_NAME='build3'

mkdir ${BUILD_DIRECTORY_NAME}
cd ${BUILD_DIRECTORY_NAME}
cmake .. -DPYBIND11_PYTHON_VERSION=3.6
make clean
make
cp *.so ..
