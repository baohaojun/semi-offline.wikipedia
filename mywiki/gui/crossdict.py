import os
import sys
import struct
import unicodedata
import inspect

crossdict_dict = open(os.path.expanduser("~/src/ahd/ahd.dz"))
index = open(os.path.expanduser("~/src/ahd/ahd.idx"))
ii = open(os.path.expanduser("~/src/ahd/ahd.ii"))

mTotalEntries = os.stat(os.path.expanduser("~/src/ahd/ahd.ii")).st_size / 4

def getEntryEndPos(idx):
    pos0 = getByte0Pos(idx)
    index.seek(pos0 + 1)
    nDefs = ord(index.read(1))
    return pos0 + 1 + nDefs * 8

def getByte0Pos(idx):
    ii.seek(idx * 4)
    ret = struct.unpack("!I", ii.read(4))[0]
    return ret - 1
    
def getWordInternal(idx):
    if idx < 0 or idx >= mTotalEntries:
        return ""

    wordStart = 0
    if idx != 0:
        wordStart = getEntryEndPos(idx - 1) + 1

    wordEndPlus1 = getByte0Pos(idx)
    if wordEndPlus1 <= wordStart:
        return ""

    index.seek(wordStart)
    word = index.read(wordEndPlus1 - wordStart)
    return word

def getNormalWord(word):
    return unicodedata.normalize(
        'NFKD', word.decode('utf-8')
    ).encode('ascii','ignore')

def getWordIdxInternal(word):

    return binarySearchHelper(getNormalWord(word), word, 0, mTotalEntries)

def compareToIgnoreCase(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()
    if w1 == w2:
        return 0
    elif w1 < w2:
        return -1
    else:
        return 1

def tryToFindExactMatch(normalWord, word, mid):
    while True:
        mid = mid - 1
        if mid < 0 or compareToIgnoreCase(normalWord, getNormalWord(getWord(mid))) != 0:
            break
            
    while True:
        mid = mid + 1
        if (word == (getWord(mid))) :
            return mid
            
        if compareToIgnoreCase(normalWord, getNormalWord(getWord(mid))) != 0:
            break
    
    return mid - 1

def binarySearchHelper(normalWord, word, min, maxP1):
    if (min + 1 >= maxP1):
        return min

        
    mid = (min + maxP1) / 2
    midWord = getWord(mid)
    midWordNormal = getNormalWord(midWord)

    compRes = compareToIgnoreCase(normalWord, midWordNormal)
    if (compRes == 0):
        if (word == midWord):
            return mid
        else:
            return tryToFindExactMatch(normalWord, word, mid)

    elif ( compRes <= 0):
        return binarySearchHelper(normalWord, word, min, mid);
    else :
        return binarySearchHelper(normalWord, word, mid + 1, maxP1);


def getWord(idx):
    return getWordInternal(idx)

def getStartEnds(idx):
    start_ends = []
    
    pos0 = getByte0Pos(idx)
    index.seek(pos0 + 1)
    nDefs = ord(index.read(1))

    for i in range(0, nDefs):
        start = struct.unpack("!I", index.read(4))
        end = struct.unpack("!I", index.read(4))
        start_ends.append((start[0], end[0]))

    return start_ends;

html_head = "<html> <head> <link rel='stylesheet' href='dict.css' type='text/css'> <script src='jquery.js'></script> <script src='rangy-core.js'></script> <script src='rangy-serializer.js'></script> <script src='android.selection.js'></script> </head> <body>"

html_tail = "</body></html>"
def getExplanation(word):
    wordIdx = getWordIdxInternal(word)
    start_ends = getStartEnds(wordIdx)
    defs = []

    entries = 10
    minIdx = max(wordIdx - entries / 2, 0)
    maxIdx = min(wordIdx + entries / 2 + 1, mTotalEntries)

    table = []
    for i in range(minIdx, maxIdx):
        word = getWord(i)
        table.append("<tr><td><a href='%s'>%s</a></tr></td>" % (word, word if i != wordIdx else ("<span style='color: red'>%s</span>" % word)))

    table_str = "<div style='float: left; margin-right: 2ex'><table>" + ''.join(table) + "</table></div>"

    if start_ends:
        for p in start_ends:
            (start, end) = p
            crossdict_dict.seek(start);
            str = crossdict_dict.read(end - start)
            defs.append(str)
        return html_head + table_str + '<div>' +  ''.join(defs) + '</div>' + html_tail

    return ""

def getExplanations(word):
    start_ends = getStartEnds(getWordIdxInternal(word))
    defs = []
    
    if start_ends:
        for p in start_ends:
            (start, end) = p
            crossdict_dict.seek(start)
            str = crossdict_dict.read(end - start)
            defs.append(str)
        return defs
    return []

def uniq_ahd():
    
    newDict = open(os.path.expanduser("~/src/ahd/ahd.dz2"), "w")
    newIdx = open(os.path.expanduser("~/src/ahd/ahd.idx2"), "w")
    newIi = open(os.path.expanduser("~/src/ahd/ahd.ii2"), "w")

    
    for i in range(0, mTotalEntries):
        word = getWord(i)
        defs_map = {}
        defs = getExplanations(word)
        uniq_defs = []
        for d in range(0, len(defs)):
            defs[d] = ''.join(defs[d].split("\r"))
            if not defs[d] in defs_map:
                defs_map[defs[d]] = 1
                uniq_defs.append(defs[d])
            else:
                print "%s:%d: word %s has dups" % (inspect.stack()[0][1], inspect.stack()[0][2], word)

        newIdx.write(word)
        newIdx.write(chr(0))
        
        newIi.write(struct.pack("!I", newIdx.tell()))
        newIdx.write(chr(len(uniq_defs)))

        for d in uniq_defs:
            newIdx.write(struct.pack("!I", newDict.tell()))
            newDict.write(d)
            newIdx.write(struct.pack("!I", newDict.tell()))
            

if __name__ == '__main__':
    # uniq_ahd()
    print getExplanation(sys.argv[1])

