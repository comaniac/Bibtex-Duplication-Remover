from pybtex.database import parse_file
import argparse
import os
import sys
import copy

# Process arguments

parser = argparse.ArgumentParser(description='Bibtex Duplicated Remover')
parser.add_argument('--out', action='store', 
        default='out.bib',
        help='The merged bib file')
parser.add_argument('primary_bib', action='store', 
        help='The primary bibtex file')
parser.add_argument('secondary_bib', action='store', 
        help='The secondary bibtex file')
args = parser.parse_args()

if not os.path.exists(args.primary_bib):
    print 'Cannot open the primary bibtex'
    sys.exit(1)
if not os.path.exists(args.secondary_bib):
    print 'Cannot open the secondary bibtex'
    sys.exit(1)
   
prim_bib = parse_file(args.primary_bib)
sec_bib = parse_file(args.secondary_bib)


# Functions

def processTitle(s):
    if s[0] == '{':
        s = s[1:-1]
    return s
   
# Build a dict for the primary
bib = {}
for k in prim_bib.entries.keys():
    title = processTitle(prim_bib.entries[k].fields['title'])
    bib[title] = (k, prim_bib.entries[k])

for k in sec_bib.entries.keys():
    title = processTitle(sec_bib.entries[k].fields['title'])
    if title in bib:
        if k == bib[title][0]:
            msg = 'ignore'
        else:
            msg = 'map to {0}'.format(bib[title][0])
        print 'Found duplication {0}, {1}'.format(k, msg)
    else:
        if k in prim_bib.entries.keys():
            print ('ERROR: The same key {0} for two different citations.'.format(k))
            print ('You need to manually resolve the conflict for {0} in the primary and {1} in the secondary'
                    .format(prim_bib.entries[k].fields['title'], title))
            sys.exit(1)
        new_entry = copy.deepcopy(sec_bib.entries[k])
        prim_bib.entries[k] = new_entry

with open(args.out, 'w') as f:
    f.write(prim_bib.to_string('bibtex').encode('utf-8'))

print 'Done'
