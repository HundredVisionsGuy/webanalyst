import pytest
from html.parser import HTMLParser
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

for i in response['messages']:
    print(i)

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #self.feed(data)
        self.starttags = []
        self.endtags = []

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        self.starttags.append(tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        self.endtags.append(tag)

    def handle_data(self, data,):
        print("Encountered some data  :", data)

    def return_startags(self):
        return self.starttags

    def return_endtags(self):
        return self.endtags

parser = MyHTMLParser()

parser.feed(file)

input("press enter to get temp file")
starttags = parser.return_startags()
endtags = parser.return_endtags()
print("Start Tags are: {}".format(starttags))
print("End Tags are: {}".format(endtags))
