from openai import OpenAI
from utils.mysql_utils import mysql_utils
from utils.prompt import News_summary_prompt,News_summary_prompt_zh
from utils.parse_utils import parse_response_summary
from db.news_sql import News_sql
from db.history_sql import History_sql
from datetime import datetime,timedelta


def llm_summary_news(parse_prompt,user_input):
    client = OpenAI(api_key='sk-SqklZhtBglH1iuhN0fF466F38bD7420f9cE1C2C05c29165c',
                    base_url = 'https://hb.rcouyi.com/v1')

    response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[
        {"role": "system", "content": parse_prompt},
        {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content


def get_news_summary(userId, lang, newsId):

    # 获取新闻
    try:
        news_sql = News_sql.query_by_id(newsId)
        new_mysql = mysql_utils()
        res = new_mysql.do_execute(news_sql, isSingle=True)
        news_content = res.get("content")
    except Exception as e:
        print("some error!",e)

    # 获取用户的历史记录
    histroy_news = []
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    query_histroy_txt = History_sql.query_user_history(userId, current_date_str, lang)
    history_news_title = new_mysql.do_execute(query_histroy_txt)
    if len(history_news_title) != 0:
        # 如果不是新用户，则获取历史浏览记录
        for history in history_news_title:
            histroy_news.append(history.get('title'))

    # 对历史记录新闻标题进行去重
    histroy_news = list(set(histroy_news))
    # 使用用户的历史记录和新闻原文拼接prompt
    if lang == 'en':
        user_input = News_summary_prompt.format(histroy_news, news_content)
    else:
        user_input = News_summary_prompt_zh.format(histroy_news,news_content)
    try:
        response = llm_summary_news("",user_input)
        response_summary = parse_response_summary(response)
        return response_summary
    except Exception as e:
        print("some error!",e)
