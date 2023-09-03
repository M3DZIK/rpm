#!/usr/bin/python3

from urllib.request import urlopen
import re

url = "https://developer.android.com/studio/preview"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

versions = re.findall("Download Android Studio .* \| (.*) Beta .*", html)

print(versions[0])
