from openai import OpenAI
from utils.mysql_utils import mysql_utils
from utils.prompt import News_Recommendation_Prompt,News_Recommendation_Prompt_Chinese
from utils.parse_utils import parse_response_news
from db.news_sql import News_sql
from db.history_sql import History_sql
from datetime import datetime,timedelta

def llm_recommend_news(parse_prompt,user_input):
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

def query_newsId_by_title(news_content_list,recommend_news_list,lang):
    # 将新闻的标题和新闻id进行绑定，并用于点击的时候获取id显示详情
    new_mysql = mysql_utils()
    for item in news_content_list:
        match_newsId_by_title = News_sql.match_newsTitle_toId(item,lang)
        res = new_mysql.do_execute(match_newsId_by_title,isSingle=True)
        if res:
            recommend_news_list.append(res)
    return recommend_news_list

def get_recommend_news_list(userId,lang):
    recommend_news_list = []
    histroy_news = []
    candiate_news = []

    # 获取当前的时间，用于增加用户的历史浏览记录
    current_date_str = datetime.now().strftime("%Y-%m-%d")

    query_histroy_txt = History_sql.query_user_history(userId, current_date_str,lang)
    new_mysql = mysql_utils()
    history_news_title = new_mysql.do_execute(query_histroy_txt)

    if len(history_news_title) != 0:
        # 如果不是新用户，则获取历史浏览记录
        for history in history_news_title:
            histroy_news.append(history.get('title'))

        # 获取今天的candiate 新闻.重复获取候选新闻,保证不为空

        while True:
            query_news_date_txt = News_sql.query_news_by_date(current_date_str,lang)
            daily_news_title = new_mysql.do_execute(query_news_date_txt)
            if daily_news_title:
                break  # 如果查询结果不为空，则退出循环

            # 更新日期为前一天
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
            current_date -= timedelta(days=1)
            current_date_str = current_date.strftime("%Y-%m-%d")

        # 抽取获取到的数据的标题
        for item_news in daily_news_title:
            candiate_news.append(item_news.get('title'))

        # 过滤掉重复新闻
        histroy_news = list(set(histroy_news))
        # 从候选新闻中删除掉之前看过的历史新闻：
        candiate_news = list(set(candiate_news) - set(histroy_news))

        # 将获取到的历史记录和候选的信息送入到大模型
        parse_prompt = ''
        if lang == 'zh':
            user_input = News_Recommendation_Prompt_Chinese.format(histroy_news, candiate_news)
        else:
            user_input = News_Recommendation_Prompt.format(histroy_news, candiate_news)

        response = llm_recommend_news(parse_prompt, user_input)

        # 对大语言模型生成的结果进行分析
        recommend_content = parse_response_news(response)
        recommend_news_list = query_newsId_by_title(recommend_content, recommend_news_list,lang)
        # 返回结果
    else:
        query_txt = News_sql.query_category_news_suffle(userId,lang)
        recommend_news_list = new_mysql.do_execute(query_txt)

    return recommend_news_list