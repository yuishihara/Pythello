#/usr/bin/env bash

BUILD_DIRECTORY_NAME='build2'

mkdir ${BUILD_DIRECTORY_NAME}
cd ${BUILD_DIRECTORY_NAME}
cmake .. -DPYBIND11_PYTHON_VERSION=2.7
make clean
make
cp *.so ..
