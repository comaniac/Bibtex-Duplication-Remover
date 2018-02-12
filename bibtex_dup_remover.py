from pybtex.database import parse_file, BibliographyData
import argparse
import os
import sys
import copy

# Process arguments

parser = argparse.ArgumentParser(description='Bibtex Duplicated Remover')
parser.add_argument('--out', action='store', 
        default='out.bib',
        help='The merged bib file')
parser.add_argument('--patch-only', action='store_true', 
        default=False,
        help='Only write the new entries from the to-be-merged file')
parser.add_argument('--verbose', action='store_true', 
        default=False,
        help='Print out details')
parser.add_argument('--another-bib', action='store', 
        default=None,
        help='The bibtex file to be merged')
parser.add_argument('primary_bib', action='store', 
        help='The source bibtex file')
args = parser.parse_args()

single_mode = False

if not os.path.exists(args.primary_bib):
    print 'Cannot open the source bibtex file'
    sys.exit(1)
else:
    print 'Reading the source bibtex file'
    prim_bib = parse_file(args.primary_bib)

if not args.another_bib is None:
    if not os.path.exists(args.another_bib):
        print 'Cannot open the to-be-merged bibtex file'
        sys.exit(1)
    else:
        print 'Reading the to-be-merged bib file'
        sec_bib = parse_file(args.another_bib)
else:
    print 'Running single mode'
    single_mode = True

new_bib = BibliographyData(entries=[])

# Functions

def processTitle(s):
    if s[0] == '{':
        s = s[1:-1]
    return s.lower()
   
# Build a dict for the primary and check the duplication
print 'Checking the duplication of the source bibtex file'
bib = {}
for k in prim_bib.entries.keys():
    title = processTitle(prim_bib.entries[k].fields['title'])
    if title in bib:
        print ('Found duplication {0} with two keys {1} and {2} '
                .format(title, k, bib[title][0]) +
                'inside primary bib')
    else:
        bib[title] = (k, prim_bib.entries[k])
        if not args.patch_only:
            new_bib.entries[k] = copy.deepcopy(prim_bib.entries[k])
       
if single_mode:
    print 'Finished'
    sys.exit(0)

# Scan the second bib and check the duplication
print 'Merging another bibtex file'
for k in sec_bib.entries.keys():
    title = processTitle(sec_bib.entries[k].fields['title'])
    if title in bib:
        # Find duplication
        # FIXME We current identify the duplication using the title only,
        # but maybe this is not sufficient
        if k == bib[title][0]: # Same key, don't merge
            msg = 'ignore'
        else: # Different key, only adopt the one in primary
            msg = 'map to {0}'.format(bib[title][0])
        print 'Found duplication {0}, {1}'.format(k, msg)
    else:
        if k in prim_bib.entries.keys():
            # The to-be-merged bibtex has the same key as the primary bibtex
            # but with different title
            print ('ERROR: The same key {0} for two different citations.'
                    .format(k))
            print ('You need to manually resolve the conflict for {0} '
                    .format(prim_bib.entries[k].fields['title']) +
                    'in the primary and {0} in the secondary'.format(title))
            sys.exit(1)
        if args.verbose:
            print 'New entry: {0}'.format(title)
        new_bib.entries[k] = copy.deepcopy(sec_bib.entries[k])  

new_bib.to_file(args.out, 'bibtex')

print 'Finished'

