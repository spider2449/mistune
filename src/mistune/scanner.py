import sys
from sre_compile import compile as sre_compile
from sre_parse import Pattern, SubPattern, parse
from sre_constants import BRANCH, SUBPATTERN

is_py2 = sys.version_info[0] == 2

if is_py2:
    def _create_subpatterns(s, lexicon):
        p = []
        for phrase, _ in lexicon:
            p.append(SubPattern(s, [
                (SUBPATTERN, (len(p) + 1, parse(phrase, s.flags))),
            ]))
        s.groups = len(p) + 1
        return p

else:
    def _create_subpatterns(s, lexicon):
        p = []
        for phrase, _ in lexicon:
            gid = s.opengroup()
            p.append(SubPattern(s, [
                (SUBPATTERN, (gid, 0, 0, parse(phrase, s.flags))),
            ]))
            s.closegroup(gid, p[-1])
        return p


class Scanner(object):
    def __init__(self, lexicon, hole_type, flags=0):
        self.lexicon = lexicon
        self.hole_type = hole_type
        s = Pattern()
        s.flags = flags

        p = _create_subpatterns(s, lexicon)
        p = SubPattern(s, [(BRANCH, (None, p))])
        self._scanner = sre_compile(p).scanner

    def scan(self, string):
        sc = self._scanner(string)

        pos = 0
        for match in iter(sc.search, None):
            _, method = self.lexicon[match.lastindex - 1]
            hole = string[pos:match.start()]
            if hole:
                yield self.hole_type, hole

            yield method(match)
            pos = match.end()

        hole = string[pos:]
        if hole:
            yield self.hole_type, hole
