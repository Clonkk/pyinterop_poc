#!/bin/sh
nim c examply.nim
if [ $# -eq 1 ]; then
    python3 main.py
fi
