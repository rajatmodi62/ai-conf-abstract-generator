import openreview
# from __future__ import print_function
# c = openreview.Client(baseurl='https://openreview.net')
# import openreview
import tools
client = openreview.Client(baseurl='https://api.openreview.net', username='rajatmodi@knights.ucf.edu', password='Bash@1995')
notes = openreview.tools.iterget_notes(client, invitation='ICLR.cc/2019/Conference/-/Blind_Submission')
print("hello")
for note in notes:
    print(note.content['title'])