from deconstruct import deconstruct
from lxml import etree
from more_itertools import unique_everseen

def get_footnote_tree(filename):
    docx = deconstruct(filename)
    footnotes = docx['word/footnotes.xml']
    return etree.fromstring(footnotes)

def extract_clean_text_from_node(node):
    outlist = []
    for x in node.itertext():
        if x is not None:
            outlist.append(x.strip() + " ")
    penultimate = "".join(outlist)
    ultimate = " ".join(penultimate.split())
    return ultimate

def get_parent_footnote_from_node(innernode):
    for x in innernode.iterancestors():
        if x.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footnote":
            return x

def get_all_smallcaps_footnote_nodes(fntree):
    all_smallcaps = fntree.findall('.//w:smallCaps', fntree.nsmap)
    return {"smallcaps_nodes": all_smallcaps,
            "footnote_nodes": [get_parent_footnote_from_node(x) for x in all_smallcaps]}

def get_text_of_smallcaps_node(smallcapsnode):
    parent = smallcapsnode.getparent()
    textnode = parent.getnext()
    return extract_clean_text_from_node(textnode)

def get_all_smallcaps_text(smallcaps_nodes):
    return [get_text_of_smallcaps_node(x) for x in smallcaps_nodes]

# FOR IMPORTING INTO OTHER MODULES
def extract_footnotes_and_smallcaps_from_file(filename):
    tree = get_footnote_tree(filename)
    nodes = get_all_smallcaps_footnote_nodes(tree)
    footnotes = unique_everseen([extract_clean_text_from_node(x) for x in nodes["footnote_nodes"]])
    smallcaps = get_all_smallcaps_text(nodes["smallcaps_nodes"])
    return {"footnotes": footnotes, "smallcaps": smallcaps}


test = extract_footnotes_and_smallcaps_from_file('testfile_cleaned.docx')
for x in test["footnotes"]:
    print(x + "\n")

for x in test["smallcaps"]:
    print(x + "\n")

#print(get_all_smallcaps_text(get_footnote_tree('testfile_cleaned.docx')))
# works


