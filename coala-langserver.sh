#!/bin/sh

cd "$(dirname "$0")" > /dev/null
exec python3 ./coala-langserver.py
cd - /dev/null
