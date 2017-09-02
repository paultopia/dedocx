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
    var demanding = "see,?\\s?(?:generally|e\\.g\\.)?.*?";
    var lessDemanding = "(?:see|\\n\\s?|\\.\\s*),?\\s?(?:generally|e\\.g\\.)?.*?";
    var forgiving =  "(?:see|\\n\\s?|\\.\\s*|^),?\\s?(?:generally|e\\.g\\.)?.*?";
    var rs2 = _.escapeRegExp(sctext);
    var rs3 = ".*?\\(.*?(?:\\d\\d\\d\\d|forthcoming)\\)";
    for (let rs1 of [demanding, lessDemanding, forgiving]){
        let rstring = rs1 + rs2 + rs3;
        let regex = new RegExp(rstring, "i");
        let match = fntext.match(regex);
        if (match){
            return match[0];
        }
    }
}

function extractCitesFromFootnote(footnote){
    var smallcaps = Array.from(footnote.getElementsByTagName("w:smallCaps"));
    var smallcapsTexts = null;
    var cites = [];
    var footnoteText = footnote.textContent;
    if (smallcaps.length !== 0){
        smallcapsTexts = smallcaps.map(x => smallcapsText(x));
        for (let sc of smallcapsTexts){
            cites.push(findCitation(footnoteText, sc));
        }
    }
    return _.uniq(cites);
}

function addCitesToDom(fnlist){
    var cites = [];
    for (let footnote of fnlist){
        cites = cites.concat(extractCitesFromFootnote(footnote));
    }
    for (let cite of cites){
        addtoDom(cite);
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
                addCitesToDom(noteslist);
            });
        });
    });
}
