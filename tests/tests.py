import pytest
from html.parser import HTMLParser

import webanalyst.validator as validator
response = validator.get_markup_validity('./project/sample.html')

# Check validator
input("Press enter to check response")
for i in response:
    print(i)

f = open("./project/sample.html", "r")
file = f.read()
file = file.replace('\n', '')
file = file.replace('  ', '')
type(file)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # self.feed(data)
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
