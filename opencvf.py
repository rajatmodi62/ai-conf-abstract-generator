import requests
from bs4 import BeautifulSoup

# url = 'https://openaccess.thecvf.com/CVPR2022?day=all'
# txt_name = 'cvpr22.txt'
def generate_cvf_abstract(url, txt_name,do, t):
    try:
        base_url = 'https://openaccess.thecvf.com/'
        r = requests.get(url)
        # print(url)
        soup = BeautifulSoup(r.content, 'lxml') # If this line causes an error, run 'pip install html5lib' or install html5lib
        # print(soup.prettify())
        texts = soup.find_all('a')
        links = []
        for text in texts:
            try:
                d = text['href']
                if '.html' in d:
                    links.append(base_url+d)
            except:
                continue

        # url = 'https://openaccess.thecvf.com/content_iccv_2013/html/Jia_Latent_Task_Adaptation_2013_ICCV_paper.html'

        save_data = []
        for done,url in enumerate(links):
            print("done", do+1,"/",t, done, "/", len(links),)
            r = requests.get(url)
            # print(url)
            soup = BeautifulSoup(r.content, 'lxml') # If this line causes an error, run 'pip install html5lib' or install html5lib
            # print(soup.prettify())

            texts = soup.find_all('div')
            for text in texts:
                try:
                    d = text["id"]
                except:
                    continue
                if d =='authors' or d =='papertitle' or d=='abstract':
                    data = text.getText()
                    # print(data)
                    save_data.append(data.strip())
            save_data.append('**********************************************************************')
            # break            
        # print(save_data)

        # with open(txt_name, 'w') as f:
        import codecs
        with codecs.open(txt_name, 'w',"utf-8") as f:
            for line in save_data:
                f.write(line)
                f.write('\n')
    except:
        print("continue")
    


conf = [
# ('https://openaccess.thecvf.com/WACV2023','wacv23.txt'),\
# ('https://openaccess.thecvf.com/CVPR2022?day=all','cvpr22.txt'),\
# ('https://openaccess.thecvf.com/WACV2022','wacv22.txt'),\
# ('https://openaccess.thecvf.com/ICCV2021?day=all','iccv21.txt'),\
# ('https://openaccess.thecvf.com/CVPR2021?day=all','cvpr21.txt'),\
# ('https://openaccess.thecvf.com/WACV2021','wacv21.txt'),\
# ('https://openaccess.thecvf.com/WACV2020','wacv20.txt'),\
# ('https://openaccess.thecvf.com/ICCV2017','iccv17.txt'),\
# ('https://openaccess.thecvf.com/CVPR2017','cvpr17.txt'),\
# ('https://openaccess.thecvf.com/CVPR2016','cvpr16.txt'),\
# ('https://openaccess.thecvf.com/ICCV2015','iccv15.txt'),\
# ('https://openaccess.thecvf.com/CVPR2015','cvpr15.txt'),\
# ('https://openaccess.thecvf.com/CVPR2014','cvpr14.txt'),\
# ('https://openaccess.thecvf.com/ICCV2013','iccv13.txt'),\
# ('https://openaccess.thecvf.com/CVPR2013','cvpr13.txt'),\
# ('https://openaccess.thecvf.com/CVPR2020?day=2020-06-16','cvpr20_1.txt'),\
# ('https://openaccess.thecvf.com/CVPR2020?day=2020-06-17','cvpr20_2.txt'),\
# ('https://openaccess.thecvf.com/CVPR2020?day=2020-06-18','cvpr20_3.txt'),\
# ('https://openaccess.thecvf.com/ICCV2019?day=2019-10-29','iccv19_1.txt'),\
# ('https://openaccess.thecvf.com/ICCV2019?day=2019-10-30','iccv19_2.txt'),\
# ('https://openaccess.thecvf.com/ICCV2019?day=2019-10-31','iccv19_3.txt'),\
# ('https://openaccess.thecvf.com/ICCV2019?day=2019-11-01','iccv19_4.txt'),\
# ('https://openaccess.thecvf.com/CVPR2019?day=2019-06-18','cvpr19_1.txt'),\
# ('https://openaccess.thecvf.com/CVPR2019?day=2019-06-19','cvpr19_2.txt'),\
# ('https://openaccess.thecvf.com/CVPR2019?day=2019-06-20','cvpr19_3.txt'),\
# ('https://openaccess.thecvf.com/CVPR2018?day=2018-06-19','cvpr18_1.txt'),\
# ('https://openaccess.thecvf.com/CVPR2018?day=2018-06-20','cvpr18_2.txt'),\
# ('https://openaccess.thecvf.com/CVPR2018?day=2018-06-21','cvpr18_3.txt'),\
# ('https://openaccess.thecvf.com/ICCV2023?day=all', 'iccv23.txt'),\
('https://openaccess.thecvf.com/WACV2024','wacv24.txt'),\
]



for done,item in enumerate(conf):
    generate_cvf_abstract(item[0], item[1], done, len(conf))