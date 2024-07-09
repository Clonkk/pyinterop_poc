#!/bin/sh
cd rustpy
cargo build --release && cp target/release/librustpy.dylib ../examply_rs.so
cd ..
if [ $# -eq 1 ]; then
    python3 main.py
fi

