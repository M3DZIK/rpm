#!/usr/bin/python3

from urllib.request import urlopen
import re

url = "https://developer.android.com/studio/preview"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

versions = re.findall("android-studio-(.*)-linux.tar.gz*", html)

# The beta version is smaller than canary version so take it.
version = min(versions)

print(version)
