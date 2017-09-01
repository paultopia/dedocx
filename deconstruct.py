from zipfile import ZipFile
from lxml import etree

def cleanup(xmlstring):
    tree = etree.fromstring(xmlstring)
    cleanstring = etree.tostring(tree, pretty_print=True).decode("latin1")
    return cleanstring

def deconstruct(docx):
    doczip = ZipFile(docx)
    output = {}
    for xmlfilename in doczip.namelist():
        output[xmlfilename] = cleanup(doczip.read(xmlfilename))
    return output

# print(deconstruct('testfile.docx')['word/comments.xml'])

# let's see if this works on pretty-printed, and as a base for subsequent extraction:

teststring = deconstruct('testfile.docx')['word/comments.xml']

tree = etree.fromstring(teststring)

first_text = tree.find('.//w:t', tree.nsmap)
text_in_first_text = "".join(first_text.itertext())
print(text_in_first_text)
# yes!!
