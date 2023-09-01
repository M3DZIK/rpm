#!/usr/bin/python3

import sys

from pkg_resources import parse_version

if parse_version(sys.argv[1]) < parse_version(sys.argv[2]):
  sys.exit(0)
else:
  sys.exit(1)
