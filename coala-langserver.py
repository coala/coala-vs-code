#!/usr/local/bin/python3

import traceback
from coala_langserver import langserver

while True:
    try:
        langserver.main()
    except Exception as e:
        tb = traceback.format_exc()
        print("FATAL ERROR: {} {}".format(e, tb))
