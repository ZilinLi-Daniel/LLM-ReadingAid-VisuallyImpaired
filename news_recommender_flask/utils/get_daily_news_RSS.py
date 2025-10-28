import feedparser
import re
import time
import requests
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup
from utils.mysql_utils import mysql_utils
from db.news_sql import News_sql

# 国内新闻RSS
domenstic_RSS_list = [
   'http://news.baidu.com/n?cmd=4&class=finannews&tn=rss',
   'http://news.baidu.com/n?cmd=1&class=housenews&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=mil&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=edunews&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=socianews&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=technnews&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=enternews&tn=rss',
   'http://news.baidu.com/n?cmd=4&class=internet&tn=rss'
]

domenstic_index_to_kind = {
    0: "经济",
    1: "房地产",
    2: "军事",
    3: "教育",
    4: "社会",
    5: "科技",
    6: "娱乐",
    7: "互联网"
}

def insert_daily_news(title,time,content,url,abstract,kind,lang):
    '''
    将处理好的新闻插入到数据库中
    :param title: 新闻标题
    :param time: 发布时间
    :param content: 新闻内容
    :param url: 新闻的网址
    :param abstract:新闻摘要
    :param kind:新闻的种类
    :param lang:新闻的语言
    :return:
    '''
    conn = mysql_utils.get_connection()
    query_user_exist_txt = News_sql.query_news_exist(url)
    res = mysql_utils.do_execute(conn, query_user_exist_txt,isSingle = True)
    if res['COUNT(url)'] != 0:
        return False
    else:
        conn = mysql_utils.get_connection()
        registe_news_txt,params = News_sql.insert_news_sql(title,time,content,url,abstract,kind,lang)
        res = mysql_utils.do_execute(conn, registe_news_txt,params)
        print(res)
        return True

def text_clean(text):
    cleaned_text = re.sub(r"（.*?）|[▲△]|责任编辑：.*$|监制.*$|执行总监：.*$", "", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    cleaned_text = re.sub(r'\[\w.*\]|\<\w.*\>','',cleaned_text)
    cleaned_text = re.sub(r'：', ':', cleaned_text)
    return cleaned_text

def crawler_news_content(url,headers):
    request = Request(url, headers=headers)
    html = urlopen(request)
    bsObj = BeautifulSoup(html, 'html.parser')
    print(bsObj)

    # Locate the parent div with class '_18p7x'
    parent_divs = bsObj.find_all('div', class_='_18p7x')
    news_content = ""

    # Iterate over each parent div to find child divs with class 'dpu8C _2kCxD'
    # and extract texts from p and span tags within these child divs
    for parent_div in parent_divs:
        child_divs = parent_div.find_all('div', class_='dpu8C _2kCxD')

        for child_div in child_divs:
            # Extract and print text from each p tag within the child div
            p_tags = child_div.find_all('p')
            for p_tag in p_tags:
                news_content += p_tag.get_text().strip()

            # Extract and print text from each span tag within the child div
            span_tags = child_div.find_all('span')
            for span_tag in span_tags:
                news_content += span_tag.get_text().strip()
    return news_content

def get_RSS_news(rss_url, headers, category,lang):
    """
    国内新闻的获取
    :param rss_url:
    :param headers:
    :param category:
    :param lang:
    :return:
    """
    feed = feedparser.parse(rss_url)
    for post in feed.entries:
        # 获取新闻，时间，内容
        # print(post)
        title = post.title
        origin_time = post.published
        format_time = origin_time.strip("‘’").split("T")[0]
        url = post.link
        summary = post.summary
        summary = text_clean(summary)
        # 对获取到的内容进行清洗
        content = crawler_news_content(url,headers)
        content = text_clean(content)
        if content and content.strip():
            insert_daily_news(title,format_time,content,url,category,summary,lang)
            time.sleep(5)
        else:
            with open("crawler_fail_url.txt", "a+") as file:
                file.write(url + "\n")



def get_daily_news():
    # 国内数据crawler 使用的headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Cookie': "BIDUPSID=318DC5A6862EE6D6AFF7046477BD5557; PSTM=1710468044; BAIDUID=318DC5A6862EE6D698DC42500AE533AA:FG=1; H_WISE_SIDS_BFESS=40008_39661_40207_40211_40217_40079_40365_40352_40298_40380_40369_40402_40415; H_PS_PSSID=40008_40211_40079_40365_40352_40298_40380_40369_40415_40461_40457_40317_39661_40506_40488_40510_40513; BAIDUID_BFESS=318DC5A6862EE6D698DC42500AE533AA:FG=1; BDRCVFR[Zh1eoDf3ZW3]=mk3SLVN4HKm; delPer=0; PSINO=7; BA_HECTOR=8g2h20a081a42l040kal85ags600ra1ivvsu71t; ZFY=WvFgNGBVMEwqIUulmtHpIIFT:AAJxYznxqJTGYs:AGzGE:C; H_WISE_SIDS=40008_40211_40079_40365_40352_40298_40380_40369_40415_40461_40457_40317_39661_40506_40488_40510_40513; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; ZD_ENTRY=baidu; ab_sr=1.0.1_ZjZhN2Q1Y2YxNmQwMTJhYTQxZTk0MmIxNjdkMTM2MmQ5ZDg2OWJlNGQxYTUwMTllYWNhN2NmMjRmMzcwMzVhZDNlYmRlNGM1MDFjYWM2OTExZDM2MTc0ODNlYzQwYmNhZTk4OGNmYWVmZDRmNWQ0MWJkMzRlZWM0OWUzNGUyNzc0NTg2OTY0YzNiNzY2OTg4MDk4ZjQ2MDZjMTg1YzZiYw=="
    }
    # 通过RSS获取国内新闻数据
    for index,rss_url in enumerate(domenstic_RSS_list):
        category = domenstic_index_to_kind.get(index)
        get_RSS_news(rss_url,headers,category,"zh")

if __name__ == "__main__":
    get_daily_news()