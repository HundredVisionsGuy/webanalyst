#import pytest
#from html.parser import HTMLParser
import requests
import pycurl
import certifi
import io
import json

f = open("./project/sample.html", "r")
file = f.read()
file = file.replace('\n','')
file = file.replace('  ', '')

crl = pycurl.Curl()
crl.setopt(crl.URL, 'https://validator.w3.org/nu/?out=json')
crl.setopt(pycurl.HTTPHEADER, ['Content-Type: text/html; charset=utf-8'])
crl.setopt(crl.CAINFO, certifi.where())
crl.setopt(crl.HTTPPOST, [
    ('fileupload', (
        # Upload the contents of the file
        crl.FORM_FILE, './project/sample.html',
    )),
])
contents = io.BytesIO()
crl.setopt(pycurl.WRITEFUNCTION, contents.write)

crl.perform()
response = contents.getvalue()
crl.close()
response = response.decode('utf-8')
response = json.loads(response)


if __name__ == "__main__":
  for i in response['messages']:
    print(i)