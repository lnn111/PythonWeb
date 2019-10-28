import requests
from bs4 import BeautifulSoup
from home import db, Article


# 洪洋文章
def getHyArtical():
    r = requests.get("https://blog.csdn.net/lmj623565791/article/list/1")
    if r.status_code == 200:
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "lxml")
        head = soup.find('head')
        # print(head.find('title').text)
        list = soup.find('div', class_='article-list')
        lists = list.find_all('div', class_='article-item-box csdn-tracking-statistics')
        for item in lists[:2]:
            a_tag = item.find('a')
            title = a_tag.text
            link = a_tag['href']
            p_tag = item.find('p', class_='content')
            content = p_tag.find('a').text
            div_tag = item.find('div', class_='info-box d-flex align-content-center')
            time = div_tag.find('span', class_='date').text
            read_num_tag = div_tag.find('span', class_='num')
            read_num = read_num_tag.text
            comm_num = read_num_tag.find_next('span', class_='num').text
            article = Article(title, content, link, time, read_num, comm_num)
            db.session.add(article)
        try:
            db.session.commit()
        except BaseException as e:
            print("出错%s" % str(e))
        else:
            print("完成。。。")


def getKyleduo():
    url = "https://blog.kyleduo.com/"
    r = requests.get(url)
    if (r.status_code == 200):
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        articals = soup.find_all('article', class_='post post-type-normal')
        for artical in articals[:2]:
            a_tag = artical.find('a', class_='post-title-link')
            title = a_tag.text
            link = url + a_tag['href']
            ar = Article(title, "", link, "", "", "")
            db.session.add(ar)
        saveToDB()

def getArticles(url):
    r = requests.get(url)
    if (r.status_code == 200):
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        return soup

def getWeishu():
    url="http://weishu.me/archives/"
    soup=getArticles(url)
    lists=soup.find_all('article',class_='post post-type-normal')
    for item in lists[:2]:
        a_tag=item.find('a',class_='post-title-link')
        title=a_tag.text
        link="http://weishu.me"+a_tag['href']
        article=Article(title,"",link,"","","")
        db.session.add(article)
    saveToDB()



def saveToDB():
    try:
        db.session.commit()
    except BaseException as e:
        print("操作数据库出错：%s" % str(e))
    else:
        print("操作数据库成功")


if __name__ == '__main__':
    getKyleduo()
