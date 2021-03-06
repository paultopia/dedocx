from deconstruct import deconstruct
from lxml import etree

docx = deconstruct('testfile_cleaned.docx')
footnotes = docx['word/footnotes.xml']
fntree = etree.fromstring(footnotes)
#first_fn = fntree.find('.//w:footnote', fntree.nsmap)
#smallcaps_from_first_fn = first_fn.find('.//w:smallCaps', fntree.nsmap)
# should be None
#print(smallcaps_from_first_fn) # and it is!

# let's find all smallcaps
#all_fns = fntree.findall('.//w:footnote', fntree.nsmap)
#smallcapfns = []
#for x in all_fns:
#    if x.find('.//w:smallCaps', fntree.nsmap):
#        print(x)
#        smallcapfns.append(x)
# ok, that doesn't work and I'm not terribly sure why... let's search for something that's definitely in the first footnote.

#pfns = []
#for x in all_fns:
#    if x.find('.//w:p', fntree.nsmap):
#        print(x)
# weird, it works there...  I get a bunch of nodes showing up.  Could it be that smallcaps isn't in the footnote field?  Let's go up the tree.

all_smallcaps = fntree.findall('.//w:smallCaps', fntree.nsmap)
#print(all_smallcaps[0].tag)

def get_parent_footnote_from_node(innernode):
    for x in innernode.iterancestors():
        if x.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnote":
            return x


fns_with_smallcaps = [get_parent_footnote_from_node(x) for x in all_smallcaps]

# print(fns_with_smallcaps)

def extract_text_from_footnote(fnnode):
    outlist = []
    for x in fnnode.itertext():
        if x is not None:
            outlist.append(x.strip() + " ")
    penultimate = "".join(outlist)
    ultimate = " ".join(penultimate.split())
    return ultimate

allfns = list(set([extract_text_from_footnote(x) for x in fns_with_smallcaps]))

for x in allfns:
    print(x + '\n')


# works, but has lots of duplication because of changes and such.  should try with cleaned up final version.  Switching from testfile.docx to testfile_cleaned.docx where the latter has all changes accepted then track changes turned off.

# still a bit dirty but I can work it with a set and such.

