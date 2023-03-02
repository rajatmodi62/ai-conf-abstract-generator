import requests
from bs4 import BeautifulSoup



def generate_icml_abstract(url, txt_name):

        # url = 'https://proceedings.mlr.press/v28/'
        # txt_name = 'dummy.txt'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        # print(soup.pretify())
        texts = soup.find_all("a")


        links= []
        for text in texts:
                if '.html' in text['href']:
                        links.append(text['href'])


        # url = 'https://proceedings.mlr.press/v28/bergstra13.html'
        # print(links)
        # exit(1)
        save_data = []

        for done, url in enumerate(links):
                print("done", done+1, "/", len(links))
                try:
                        r = requests.get(url)
                        # print(url)
                        soup = BeautifulSoup(r.content, 'lxml') # If this line causes an error, run 'pip install html5lib' or install html5lib
                        # print(soup.prettify())

                        
                        texts = soup.find_all("title")
                        for text in texts:
                                try:
                                        data = str(text.getText())
                                        data = data.replace(u'\xa0', u' ')
                                        save_data.append(data.strip())
                                except:
                                        continue


                        #find authors
                        texts = soup.find_all("span",{'class':'authors'})
                        for text in texts:
                                try:
                                        data = str(text.getText())
                                        data = data.replace(u'\xa0', u' ')
                                        save_data.append(data.strip())
                                except:
                                        continue

                        #find abstract
                        texts = soup.find_all('div',{'class':'abstract'})
                        for text in texts:
                                try:
                                        data = text.getText()
                                        data = data.replace(u'\xa0', u' ')
                                        save_data.append(data.strip())
                                except:
                                        continue
                        save_data.append('*****************************')
                        with open(txt_name, 'w') as f:
                                for line in save_data:
                                        f.write(line)
                                        f.write('\n')
                        
                except:
                        continue
        import codecs
        with codecs.open(txt_name, 'w',"utf-8") as f:
                for line in save_data:
                        # line = unicode(line, "utf-8")
                        f.write(line)
                        f.write('\n')


conf = [

        ('https://proceedings.mlr.press/v162','icml22.txt'),\
        ('https://proceedings.mlr.press/v139','icml21.txt'),\
        ('https://proceedings.mlr.press/v119','icml20.txt'),\
        ('https://proceedings.mlr.press/v97','icml19.txt'),\
        ('https://proceedings.mlr.press/v80','icml18.txt'),\
        ('https://proceedings.mlr.press/v70','icml17.txt'),\
        ('https://proceedings.mlr.press/v48','icml16.txt'),\
        ('https://proceedings.mlr.press/v37','icml15.txt'),\
        ('https://proceedings.mlr.press/v32','icml14.txt'),\
        ('https://proceedings.mlr.press/v28','icml13.txt'),\
]

for item in conf:
        generate_icml_abstract(item[0],item[1])