from pybtex.database.input import bibtex
import collections 
parser = bibtex.Parser()
bib_data = parser.parse_file('abstract.bib')

d = collections.defaultdict(list)
for processed, paper in enumerate(bib_data.entries.keys()):
    try:
        # print(bib_data.entries[paper].fields['abstract'])
        # print(bib_data.entries[paper].fields.keys())
        conference = bib_data.entries[paper].fields['booktitle']
        title = bib_data.entries[paper].fields['title']
        abstract = bib_data.entries[paper].fields['abstract']
        d[conference].append((title, abstract))
    except:
        print("fine")

for k in d.keys():
    # if 'ACL' in k or 'NAACL' in k or 'EMNLP' in k:
    print(k)
        