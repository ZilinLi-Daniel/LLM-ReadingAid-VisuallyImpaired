# 获取每日国际新闻
import feedparser
import re
import time
import json
import configparser

from utils.NewsAgent import NewsAgent
from selenium import webdriver
from utils.mysql_utils import mysql_utils
from utils.parse_utils import parse_text
from db.news_sql import News_sql
from utils.prompt import Category_PROMPT
from datetime import datetime

config = configparser.ConfigParser()
config.read('../config/config.ini')
# 用于统计
news_kind_count = {
    "Economy":6,
    "Real estate":1,
    "Military":4,
    "Education":5,
    "Social":5,
    "Technology":5,
    "Entertainment":5,
    "Internet":3,
    "Public":5
}

#对应的新闻RSS
intel_RSS_list = [
    'https://feeds.bbci.co.uk/news/business/rss.xml', # 经济
    'https://feeds.bbci.co.uk/news/politics/rss.xml', #政治
    'https://feeds.bbci.co.uk/news/health/rss.xml', # 健康
    'https://feeds.bbci.co.uk/news/education/rss.xml', #教育
    'https://feeds.bbci.co.uk/news/science_and_environment/rss.xml', # 科学环境
    'https://feeds.bbci.co.uk/news/technology/rss.xml', # 科技
    'https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml', #娱乐
    'https://feeds.bbci.co.uk/news/world/rss.xml',#世界新聞
    'https://feeds.bbci.co.uk/news/rss.xml',
    'https://feeds.bbci.co.uk/news/world/europe/rss.xml',
    'https://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
    'https://feeds.bbci.co.uk/news/world/africa/rss.xml',
    'https://feeds.bbci.co.uk/news/world/asia/rss.xml',
    'https://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
    'https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
    'https://feeds.bbci.co.uk/news/england/rss.xml',
    'https://feeds.bbci.co.uk/news/northern_ireland/rss.xml',
    'https://feeds.bbci.co.uk/news/scotland/rss.xml',
    'https://feeds.bbci.co.uk/news/wales/rss.xml'
]

def insert_daily_news(title,time,content,url,category,abstract,lang):
    '''
    将处理好的新闻插入到news_base的数据库表中
    :param title: 新闻标题
    :param time: 新闻发布时间
    :param content: 新闻内容
    :param url: 新闻的url
    :param kind: 新闻的种类
    :return: 处理结果
    '''
    conn = mysql_utils.get_connection()
    query_news_exist_txt = News_sql.query_news_exist(url)
    res = mysql_utils.do_execute(conn, query_news_exist_txt, isSingle=True)
    if res['COUNT(url)'] != 0:
        return None
    else:
        # 插入到news_base的数据库
        insert_query, params = News_sql.insert_news_sql(title, time, content, url, category, abstract, lang)
        news_id = mysql_utils.do_execute(conn, insert_query, params)
        return news_id


def set_news_kind(content):
    '''
    analysize the news category
    :param content:
    :return:
    '''
    messages = [{"role": "system", "content": Category_PROMPT}]
    news_agent = NewsAgent(api_key=config.get(section='llm', option='api'),
                           base_url=config.get(section='llm', option='base_url'),
                           model=config.get(section='llm', option='model'),
                           messages=messages)

    parse_news = news_agent.continue_conversation(user_input="Let's begin:[News]:" + content)
    print("大语言模型分析种类的结果：\n", parse_news)
    result = parse_text(parse_news)
    kind = result.get('Category')
    if '\n' in kind:
        kind = kind.replace('\n', '')
    return kind


# 获取新闻内容
def crawler_news_content(url):
    '''
    通过爬虫获取对应的新闻内容
    :param url:
    :param headers:
    :return:  获取到的新闻文本
    '''

    driver = webdriver.Chrome()

    try:
        # Open the URL
        driver.get(url)

        # Wait for the page to fully load
        time.sleep(10)

        # Find the script tag containing the JSON data
        try:
            script_tag = driver.find_element("id", "__NEXT_DATA__").get_attribute('innerHTML')
        except Exception:
            script_tag = None

        if script_tag:
            # Parse the JSON data
            json_data = json.loads(script_tag)

            # Navigate through the JSON structure to extract the desired content
            tag = url.split('/')[-1]
            contents_key = f'@"news","{tag}",'
            contents = json_data['props']['pageProps']['page'][contents_key]['contents']
            final_text = ''
            for item in contents:
                if item['type'] == 'text':
                    for block in item['model']['blocks']:
                        if block['type'] == 'paragraph':
                            final_text += block['model']['text']

            return final_text
        else:
            return None
    except Exception:
        return None
    finally:
        # Close the driver
        driver.close()
        time.sleep(5)

def format_time(origin_time):
    date_obj = datetime.strptime(origin_time, '%a, %d %b %Y %H:%M:%S GMT')

    # Format the date as "Fri, 29 Mar 2024"
    formatted_day = date_obj.strftime('%Y.%m.%d')
    return formatted_day

def text_clean(text):
    '''
    对新闻的摘要和文本内容进行清洗
    :param text:
    :return:
    '''
    cleaned_text = re.sub(r"\s+", " ", text).strip()
    cleaned_text = re.sub(r'\[\w.*\]|\<\w.*\>','',cleaned_text)
    cleaned_text = re.sub(r'：', ':', cleaned_text)
    return cleaned_text

def get_RSS_news(rss_url):
    '''
    通过rss的地址，获取新闻内容
    :param rss_url: 不通种类的新闻rss
    :param headers: 对网页请求的rss头
    :return: 插入基本数据库的基本信息
    '''
    execute_get_daily_news = any(count < 5 for count in news_kind_count.values())
    print(execute_get_daily_news)
    if execute_get_daily_news:
        feed = feedparser.parse(rss_url)
        for post in feed.entries:
            # 获取新闻，时间，内容, 摘要, 新闻链接
            title = post.title
            origin_time = post.published
            time = format_time(origin_time)
            url = post.link
            # 判断数据库是否包含这条新闻，如果有，后面的就不用做了：
            conn = mysql_utils.get_connection()
            query_news_exist_txt = News_sql.query_news_exist(url)
            res = mysql_utils.do_execute(conn, query_news_exist_txt, isSingle=True)
            if res['COUNT(url)'] != 0:
                continue
            # 如果数据库不包含这条新闻，则继续处理
            summary = post.summary
            summary = text_clean(str(summary))
            # 对获取到的内容进行清洗
            content = crawler_news_content(url)
            content = text_clean(str(content))

            # 通过大语言模型对该条新闻的种类进行判断
            category = set_news_kind(content)

            if content and content.strip() and category:
                # 将获取到的新闻信息插入到基本信息表(base_news)
                if news_kind_count.get(category) < 5:
                    news_kind_count[category] += 1
                    insert_daily_news(title, time, content, url, category, summary, "en")
            else:
                # 将处理失败的新闻写入到记录的文件中
                with open("crawler_fail_url.txt", "a+") as file:
                    file.write(url + "\n")
                continue


def get_internal_daily_news():
    for rss_url in intel_RSS_list:
        print(rss_url)
        get_RSS_news(rss_url)


if __name__ == "__main__":
    get_internal_daily_news()