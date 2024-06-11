import openreview
import jsonlines

c = openreview.Client(baseurl='https://api2.openreview.net')
notes = c.get_all_notes(content={'venueid':'ICLR.cc/2024/Conference'} )
txt_name = 'iclr24.txt'
all_iclr = []
# notes = c.get_all_notes(invitation=f'ICLR.cc/2024/Conference/-/Submission')
# print(len(notes))
save_data = []
total = 0


keyword_list = [
        'action recognition',\
        'action localization',\
        'video captioning',\
        'video question answering',\
        'video text retrieval',\
        'text video retrieval',\
        'video generation',\
        'video prediction',\
        'video synthesis',\
        
]


for note in notes:
    note = note.to_json()
    authors = note['content']['authors']['value']
    authors = ','.join(authors)
    title = note['content']['title']['value']
    abstract = note['content']['abstract']['value']
    save_data.append(authors)
    save_data.append(title)
    save_data.append(abstract)
    save_data.append('**********************************************************************')
    # print(authors)
    # print(title)
    print(abstract)
    total+=1
print(total)
import codecs
with codecs.open(txt_name, 'w',"utf-8") as f:
    for line in save_data:
        f.write(line)
        f.write('\n')