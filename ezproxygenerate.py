from __future__ import print_function
import sys,os,re,ssl

domain = "ezproxy.library.uwa.edu.au"
pattern = re.compile(r'"http:\/\/ezproxy\.library\.uwa\.edu\.au\/login\?url=http:\/\/([^"\/]+)')

def f7(seq):
    '''http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order'''
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x) or x == domain)]

def print_preamble(fpo, database):
    print("// ==UserScript==", file=fpo)
    print("// @name UWA Auto EzProxy Redirector", file=fpo)
    print("// @namespace jtanx.plugins", file=fpo)
    print("// @description Automatically redirect to the proxified equivalent as provided by the University of Western Australia.", file=fpo)
    print("// @run-at document-start", file=fpo)
    print("// @grant none", file=fpo)
    print("// ", file=fpo)
    
    domains = []
    for line in open(database):
        m = re.search(pattern, line)
        if m:
            domains.append(m.group(1).replace("www.","").replace("*.",""))
    
    domains = f7(domains)
    for d in domains:
        print("// @match http://*.%s/*" % d, file=fpo)
        print("// @match https://*.%s/*" % d, file=fpo)
            
    print("// ==/UserScript==", file=fpo)
    print(file=fpo)
    

def main(f=None, out=sys.stdout):
    if type(out) is str:
        out = open(out, "w")
    print_preamble(out, f)
    print(r'window.location.replace(window.location.href.replace(/(https?:\/\/)([^\/]+)(.*)/i, "$1$2.%s$3"))' % domain, file=out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s database.html")
    else:
        main(*sys.argv[1:])