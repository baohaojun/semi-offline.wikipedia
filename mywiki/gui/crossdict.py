import re
import os
import sys
import struct
import unicodedata
import inspect
from OrderedSet import OrderedSet

def getNormalWord(word):
    return unicodedata.normalize(
        'NFKD', word.decode('utf-8')
    ).encode('ascii','ignore')



def ncasecmp(a, b):
    return cmp(getNormalWord(a).lower(), getNormalWord(b).lower())

def compareToIgnoreCase(w1, w2):
    w1 = w1.lower()
    w2 = w2.lower()
    if w1 == w2:
        return 0
    elif w1 < w2:
        return -1
    else:
        return 1

class CrossDict:
    def __init__(self, dict_name, derived_name = None):
        self.crossdict_dict = open(os.path.expanduser("~/src/ahd/%s.dz" % dict_name))
        self.index = open(os.path.expanduser("~/src/ahd/%s.idx" % dict_name))
        self.ii = open(os.path.expanduser("~/src/ahd/%s.ii" % dict_name))
        self.mTotalEntries = os.stat(os.path.expanduser("~/src/ahd/%s.ii" % dict_name)).st_size / 4
        if derived_name:
            self.derived_dict = CrossDict(derived_name)
        else:
            self.derived_dict = None

    def getEntryEndPos(self, idx):
        pos0 = self.getByte0Pos(idx)
        self.index.seek(pos0 + 1)
        nDefs = ord(self.index.read(1))
        return pos0 + 1 + nDefs * 8

    def getByte0Pos(self, idx):
        self.ii.seek(idx * 4)
        ret = struct.unpack("!I", self.ii.read(4))[0]
        return ret - 1

    def getWordInternal(self, idx):
        if idx < 0 or idx >= self.mTotalEntries:
            return ""

        wordStart = 0
        if idx != 0:
            wordStart = self.getEntryEndPos(idx - 1) + 1

        wordEndPlus1 = self.getByte0Pos(idx)
        if wordEndPlus1 <= wordStart:
            return ""

        self.index.seek(wordStart)
        word = self.index.read(wordEndPlus1 - wordStart)
        return word

    def getWordIdxInternal(self, word):
        return self.binarySearchHelper(getNormalWord(word), word, 0, self.mTotalEntries)


    def tryToFindExactMatch(self, normalWord, word, mid):
        while True:
            mid = mid - 1
            if mid < 0 or compareToIgnoreCase(normalWord, getNormalWord(self.getWord(mid))) != 0:
                break

        while True:
            mid = mid + 1
            if (word == (self.getWord(mid))) :
                return mid

            if compareToIgnoreCase(normalWord, getNormalWord(self.getWord(mid))) != 0:
                break

        return mid - 1

    def binarySearchHelper(self, normalWord, word, min, maxP1):
        if (min + 1 >= maxP1):
            return min

        mid = (min + maxP1) / 2
        midWord = self.getWord(mid)

        midWordNormal = getNormalWord(midWord)

        compRes = compareToIgnoreCase(normalWord, midWordNormal)
        if (compRes == 0):
            if (word == midWord):
                return mid
            else:
                return self.tryToFindExactMatch(normalWord, word, mid)

        elif ( compRes <= 0):
            return self.binarySearchHelper(normalWord, word, min, mid);
        else :
            return self.binarySearchHelper(normalWord, word, mid + 1, maxP1);


    def getWord(self, idx):
        return self.getWordInternal(idx)

    def getStartEnds(self, idx):
        start_ends = []

        pos0 = self.getByte0Pos(idx)
        self.index.seek(pos0 + 1)
        nDefs = ord(self.index.read(1))

        for i in range(0, nDefs):
            start = struct.unpack("!I", self.index.read(4))
            end = struct.unpack("!I", self.index.read(4))
            start_ends.append((start[0], end[0]))

        return start_ends;

    def getExplanation(self, word):
        html_head = "<html> <head> <link rel='stylesheet' href='dict.css' type='text/css'> <script src='jquery.js'></script> <script src='rangy-core.js'></script> <script src='rangy-serializer.js'></script> <script src='android.selection.js'></script> </head> <body>"

        html_tail = "</body></html>"

        word = word.strip()
        wordIdx = self.getWordIdxInternal(word)
        wordX = self.getWord(wordIdx)

        if (getNormalWord(word).lower() != getNormalWord(wordX).lower()) and self.derived_dict:
            derivedIdx = self.derived_dict.getWordIdxInternal(word)
            derivedWordX = self.derived_dict.getWord(derivedIdx)

            if (getNormalWord(word).lower() == getNormalWord(derivedWordX).lower()):
                words = self.derived_dict.getExplanations(word)
                if len(words) > 1:
                    return html_head + ("%s" % words) + html_tail
                else:
                    wordIdx = self.getWordIdxInternal(words[0])
        start_ends = self.getStartEnds(wordIdx)
        defs = []

        n_entries = 10
        minIdx = max(wordIdx - n_entries / 2, 0)
        maxIdx = min(wordIdx + n_entries / 2 + 1, self.mTotalEntries)

        table = []
        for i in range(minIdx, maxIdx):
            word = self.getWord(i)
            table.append("<tr><td><a href='%s'>%s</a></td></tr>" % (word, word if i != wordIdx else ("<span style='color: red'>%s</span>" % word)))

        table_str = "<table>" + ''.join(table) + "</table>"

        if start_ends:
            for p in start_ends:
                (start, end) = p
                self.crossdict_dict.seek(start);
                str = self.crossdict_dict.read(end - start)
                defs.append(str.replace('ALIGN="center" WIDTH="100%"', ''))
            return html_head + '<table><tr><td class="topAlign left-panel">' + table_str + '</td><td class="topAlign"><div>' +  ''.join(defs) + '</div></td></tr></table>' + html_tail

        return ""

    def getExplanations(self, word):
        start_ends = self.getStartEnds(self.getWordIdxInternal(word))
        defs = []

        if start_ends:
            for p in start_ends:
                (start, end) = p
                self.crossdict_dict.seek(start)
                str = self.crossdict_dict.read(end - start)
                defs.append(str)
            return defs
        return []

    def write_dict(self, entries, entry_defs, newDict, newIdx, newIi):
        def_start_end_map = {}
        for word in entries:
            norm_low_word = getNormalWord(word).lower()
            uniq_defs = entry_defs[norm_low_word]
            if len(uniq_defs) > 255:
                print "%s:%d: word is %s, uniq_defs is %s" % (inspect.stack()[0][1], inspect.stack()[0][2], word, uniq_defs)
                continue

            newIdx.write(word)
            newIdx.write(chr(0))
            newIi.write(struct.pack("!I", newIdx.tell()))
            newIdx.write(chr(len(uniq_defs)))

            start = end = 0
            for d in uniq_defs:
                if d in def_start_end_map:
                    (start, end) = def_start_end_map[d]
                else:
                    start = newDict.tell()
                    newDict.write(d)
                    end = newDict.tell()
                    def_start_end_map[d] = (start, end)
                newIdx.write(struct.pack("!I", start))
                newIdx.write(struct.pack("!I", end))


    def uniq_ahd(self):

        newDict = open(os.path.expanduser("~/src/ahd/ahd.dz2"), "w")
        newIdx = open(os.path.expanduser("~/src/ahd/ahd.idx2"), "w")
        newIi = open(os.path.expanduser("~/src/ahd/ahd.ii2"), "w")

        derived_word_map = {}
        ordered_word_defs = OrderedSet()
        word_defs = {}
        entries = OrderedSet()
        derived_entries = OrderedSet()
        nl_entry_defs = {}
        for i in range(0, self.mTotalEntries):
            word = self.getWord(i)

            if i % 1000 == 0:
                print "%s:%d: word is %s" % (inspect.stack()[0][1], inspect.stack()[0][2], word)

            norm_low_word = getNormalWord(word).lower()
            entries.add(word)
            if norm_low_word not in nl_entry_defs:
                nl_entry_defs[norm_low_word] = OrderedSet()
            defs_map = {}
            defs = self.getExplanations(word)
            uniq_defs = []
            for d in range(0, len(defs)):
                defs[d] = ''.join(defs[d].split("\r"))
                if not defs[d] in defs_map:
                    defs_map[defs[d]] = 1
                    uniq_defs.append(defs[d])
                else:
                    print "%s:%d: word %s has dups" % (inspect.stack()[0][1], inspect.stack()[0][2], word)

            for d in uniq_defs:
                nl_entry_defs[norm_low_word].add(d)
                d = ''.join(d.split('&#183;'))
                d = ''.join(d.split('<FONT FACE="Minion New">&#57375;</FONT>'))
                d = ''.join(d.split('<FONT FACE="Minion New">&#8242;</FONT>'))
                for derived_word in re.findall(r'<FONT SIZE="-1" FACE="arial,sans-serif">(?:<I>)?(?:<FONT COLOR="#229966">)?(?:<I>)?(.*?)(?:</I>)?</FONT>', d):
                    if derived_word != word and \
                    '&' not in derived_word and \
                    '<' not in derived_word and \
                    len(derived_word) > 1 and \
                    derived_word != ', ':
                        derived_word = getNormalWord(derived_word).lower()
                        if derived_word not in derived_word_map:
                            derived_word_map[derived_word] = OrderedSet()
                        derived_word_map[derived_word].add(word)
                        derived_entries.add(derived_word)

        self.write_dict(entries, nl_entry_defs, newDict, newIdx, newIi)
        newDict = open(os.path.expanduser("~/src/ahd/derive.dz"), "w")
        newIdx = open(os.path.expanduser("~/src/ahd/derive.idx"), "w")
        newIi = open(os.path.expanduser("~/src/ahd/derive.ii"), "w")
        derived_entries -= entries


        derived_entries=list(derived_entries)
        derived_entries.sort(cmp=ncasecmp)
        self.write_dict(derived_entries, derived_word_map, newDict, newIdx, newIi)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Uasge: crossdict.py cmd"
        exit()
        
    elif sys.argv[1] == "uniq":
        cd = CrossDict('ahd')
        cd.uniq_ahd()
    elif sys.argv[1] == "list":
        dd = CrossDict('derive')
        for i in range(0, dd.mTotalEntries):
            word = dd.getWord(i)
            print "%s: %s" % (dd.getWord(i), dd.getExplanations(word))
    elif sys.argv[1] == "look":
        cd = CrossDict('ahd')
        print cd.getExplanation(sys.argv[2])
    # for x in range(0, 1000):
         # print self.getWordInternal(x)

