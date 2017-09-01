import zipfile
stuff = zipfile.ZipFile('testfile.docx', 'r')

# list of files
# print(stuff.namelist())

# extract one of them, as xml string
#print(stuff.read('word/comments.xml'))

from lxml import etree

# pretty-print to file --- apparrntly tostring returns as bytes for some reason.

#with open("testdump.txt", "wb") as tw:
#    tw.write(etree.tostring(etree.fromstring(stuff.read('word/comments.xml')), pretty_print=True))

def pretty_print_to_file(xmlfile_in_zip, myzipfile, filename):
    with open(filename, "wb") as fn:
        fn.write(etree.tostring(etree.fromstring(myzipfile.read(xmlfile_in_zip)), pretty_print=True))

#pretty_print_to_file('word/footnotes.xml', stuff, "test_footnotes.txt")

def pretty_print_to_screen(xmlfile_in_zip, myzipfile):
    text = etree.tostring(etree.fromstring(myzipfile.read(xmlfile_in_zip)), pretty_print=True).decode("latin1") 
    print(text)

# quotes are buggered up unless decoded in latin-1 as above.  can I do this further up the chain for purposes of working with documents?  but would have to get back into latin-1 for word later?  not important if I'm just extracting, I can do utf-8 like a normal person.


# pretty_print_to_screen('word/comments.xml', stuff)

# how to extract everything in <w:smallCaps/>

# hardcoding this per here: https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree but should just do it by parsing the string

namespaces = {"wpc":"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
              "mo":"http://schemas.microsoft.com/office/mac/office/2008/main",
              "mc":"http://schemas.openxmlformats.org/markup-compatibility/2006",
              "mv":"urn:schemas-microsoft-com:mac:vml",
              "o":"urn:schemas-microsoft-com:office:office",
              "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
              "m":"http://schemas.openxmlformats.org/officeDocument/2006/math",
              "v":"urn:schemas-microsoft-com:vml",
              "wp14":"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
              "wp":"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
              "w10":"urn:schemas-microsoft-com:office:word",
              "w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main",
              "w14":"http://schemas.microsoft.com/office/word/2010/wordml",
              "wpg":"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
              "wpi":"http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
              "wne":"http://schemas.microsoft.com/office/word/2006/wordml",
              "wps":"http://schemas.microsoft.com/office/word/2010/wordprocessingShape"}

tree = etree.fromstring(stuff.read('word/footnotes.xml'))

#all_smallcaps = tree.findall('.//w:smallCaps', namespaces)

#print(all_smallcaps)

# correctly produces node.

#print(" ".join(first_smallcaps.itertext())) # https://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml

#print([" ".join(x.itertext()) for x in all_smallcaps])

# no good, they're all blank.  itertext is wrong method to call here or something, doesn't actually get text inside.

#print([" ".join(x.text()) for x in all_smallcaps])
# also doesn't work.  will have to continue later.

# aaah the reason it doesn't work is because text isn't actually within smallcaps tag.  rather, each chunk of text apparently has properties node and text node.  Example:

# <w:r w:rsidRPr="00C62D63">
#    <w:rPr>
#      <w:rFonts w:ascii="Century Schoolbook" w:hAnsi="Century Schoolbook"/>
#      <w:smallCaps/>
#      <w:sz w:val="16"/>
#      <w:szCs w:val="16"/>
#    </w:rPr>
#    <w:t>Alexander M. Bickel, The Least Dangerous Branch: The Supreme Court at the Bar of Politics</w:t>
#  </w:r>


first_sc = tree.find('.//w:smallCaps', namespaces)

sc_parent = first_sc.getparent() # should be the w:rPr -- and it is!
print(sc_parent)

sc_textnode = sc_parent.getnext() # should be w:t -- and it is!
print(sc_textnode)

# and it should have text, so:
#print("".join(sc_textnode.itertext()))
# that works!  I can now extract smallcaps! 

# while I'm at it, can I just get the nsmap??

#print(tree.nsmap)

# yes, I can.  So can I do the same thing as above, but with nsmap built in?

again_first_sc = tree.find('.//w:smallCaps', tree.nsmap)
again_sc_parent = again_first_sc.getparent()
again_sc_textnode = again_sc_parent.getnext()
print("".join(again_sc_textnode.itertext()))

# yes, I can!  thank goodness!
