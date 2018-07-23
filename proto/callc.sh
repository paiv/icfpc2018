#!/usr/bin/env bash
pushd somelib/build > /dev/null
make
popd > /dev/null
./demo_ctypes.py
