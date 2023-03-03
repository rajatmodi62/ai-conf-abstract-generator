# importing required modules
from PyPDF2 import PdfReader
 

path= '/Users/rajat/Downloads/eccv2022.pdf'
year = '2022'
# creating a pdf reader object
reader = PdfReader(path)
 
# printing number of pages in pdf file
print(len(reader.pages))
 
# getting a specific page from the pdf file
# page = reader.pages[100]
 
# # extracting text from page
# text = page.extract_text()
count= 0

save = []
for i in range(len(reader.pages)):
    print(i,"/",len(reader.pages))
    page = reader.pages[i]
    # extracting text from page
    text = page.extract_text()
    if "Abstract" in text:
        print("Krishna")
        index = text.find('Introduction')
        save+=[str(text[:index])]
        count+=1
        save+=['************************************']
print(count)

import textwrap

my_wrap = textwrap.TextWrapper(width = 100)
final_lines = save


# print(final_lines)

save_name = 'eccv_' + year + '.txt'


# with open(save_name, 'w') as f:
import codecs
with codecs.open(save_name, 'w',"utf-8") as f:
    for line in final_lines:
        f.write(line)
        f.write('\n')