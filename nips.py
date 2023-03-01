import requests
from bs4 import BeautifulSoup

years = [str(i) for i in range(1987,2023)]

for year in years:
        
    URL = 'https://papers.nips.cc/paper/'+year
    r = requests.get(URL)
    print(URL)
    soup = BeautifulSoup(r.content, 'lxml') # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())

    texts = soup.find_all('a')

    links = []
    for text in texts:
        # print(type(text))
        # print(text['href'])
        if 'html' in text['href']:
            links.append(text['href'])

    links = sorted(links)

    save = []
    for done, link in enumerate(links):
        print("done", done+1, "/", len(links))
        url = 'https://papers.nips.cc/'+link
        
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        # print(soup)
        # exit(1)
        texts = soup.find_all('h4')
        for text in texts:
            save+=[text.getText()] #paper title
            break
        print(save)
        
        texts = soup.find_all('p')
        data = []
        for text in texts:
            # print(text.getText())
            data.append(text.getText())
        print("author", data[1])
        print("tetx", data[3])
        save+=[data[1]]
        save+=[]
        save+=[data[3]]
        save+=['************************************']
        # break
        


            
    import textwrap

    my_wrap = textwrap.TextWrapper(width = 100)
    final_lines = save


    print(final_lines)

    save_name = 'nips_' + year + '.txt'


    # with open(save_name, 'w') as f:
    import codecs
    with codecs.open(save_name, 'w',"utf-8") as f:
        for line in final_lines:
            f.write(line)
            f.write('\n')
