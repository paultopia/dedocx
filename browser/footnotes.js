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

function escapeRegExp(string){
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); 
}

function findCitation(fntext, sctext){
    var rs1 = "(?:\n|\.\s*|see|See),?\s?(?:generally|e\.g\.)?.*?"
    var rs3 = ".*?\(.*?\d\d\d\d\|forthcoming)"
    var rstring = rs1 + escapeRegExp(sctext) + rs3;
    var regex = new RegExp(rstring);
    return fntext.match(regex);
}

function extractFromFootnote(footnote){
    var smallcaps = Array.from(footnote.getElementsByTagName("w:smallCaps"));
    var smallcapsTexts = null;
    var footnoteText = footnote.textContent;
    if (smallcaps.length !== 0){
        smallcapsTexts = smallcaps.map(x => smallcapsText(x));
        for (let sc of smallcapsTexts){
            console.log(findCitation(footnoteText, sc));
        }
    }
    return {"text": footnoteText, "smallcaps": smallcapsTexts};
}

function addFootnotesToDom(fnlist){
    for (let footnote of fnlist){
        let text = JSON.stringify(extractFromFootnote(footnote), undefined, 4);
        let newParagraph = document.createElement('p');
        newParagraph.textContent = text;
        document.getElementsByTagName("body")[0].appendChild(newParagraph);
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
                var tenthnote = noteslist[10];
                console.log(tenthnote.textContent);
                var smallcaps = tree.getElementsByTagName("w:smallCaps");
                console.log(smallcapsText(smallcaps[0]));
                console.log(noteslist.length);
                console.log(getScNodes(noteslist).length);
                addFootnotesToDom(noteslist);
                console.log(noteslist[5]); 
            });
        });
    });
}
