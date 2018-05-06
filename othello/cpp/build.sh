#/usr/bin/env bash

cd build
cmake ..
make clean
make
cp *.so ..
