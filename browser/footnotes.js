zip.workerScriptsPath = "zipjs/";

function findFootnotes(entrylist){
    for (let entry of entrylist){
        if (entry.filename === "word/footnotes.xml") return entry;}}

function parsexml(xmlstring){
    var parser = new DOMParser();
    return parser.parseFromString(xmlstring, "text/xml");}

function getScNodes(footnotelist){
    return Array.from(footnotelist).filter(x => x.getElementsByTagName("w:smallCaps").length !== 0);
}

function smallcapsText(smallcapsnode){
    var parent = smallcapsnode.parentNode;
    var text = parent.nextSibling;
    return text.textContent;}

function addtoDom(paragraph){
    let newParagraph = document.createElement('pre');
    newParagraph.textContent = paragraph;
    document.getElementsByTagName("body")[0].appendChild(newParagraph);
}

function findCitation(fntext, sctext){
    var rs1 = "(?:^|\\n\\s?|\\.\\s*|see),?\\s?(?:generally|e\\.g\\.)?.*?"
    var rs3 = ".*?\\(.*?(?:\\d\\d\\d\\d|forthcoming)\\)"
    var rstring = rs1 + _.escapeRegExp(sctext) + rs3;
    var regex = new RegExp(rstring, "i");
    addtoDom(rstring);
    addtoDom(fntext);
    addtoDom(JSON.stringify(fntext.match(regex)));
}

function extractFromFootnote(footnote){
    var smallcaps = Array.from(footnote.getElementsByTagName("w:smallCaps"));
    var smallcapsTexts = null;
    var footnoteText = footnote.textContent;
    if (smallcaps.length !== 0){
        smallcapsTexts = smallcaps.map(x => smallcapsText(x));
        for (let sc of smallcapsTexts){
            findCitation(footnoteText, sc);
        }
    }
    return {"text": footnoteText, "smallcaps": smallcapsTexts};
}

function addFootnotesToDom(fnlist){
    for (let footnote of fnlist){
        let text = JSON.stringify(extractFromFootnote(footnote), undefined, 4);
        //addtoDom(text);
    }
}

function handleFiles(fileobj){
    var fileblob = new Blob(fileobj);
    zip.createReader(new zip.BlobReader(fileblob), function(reader){
        reader.getEntries(function(entries){
            var footnotes = findFootnotes(entries);
            footnotes.getData(new zip.TextWriter(), function(text) {
                var tree = parsexml(text);
                var noteslist = tree.getElementsByTagName("w:footnote");
                addFootnotesToDom(noteslist);
            });
        });
    });
}
