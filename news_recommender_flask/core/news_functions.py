from flask import Blueprint,request,jsonify
from utils.mysql_utils import mysql_utils
from db.news_sql import News_sql
from db.history_sql import History_sql
from datetime import datetime
from utils.recommend_news_list import get_recommend_news_list
from utils.summary_news import get_news_summary

news_blueprint = Blueprint('news', __name__)

@news_blueprint.route('/api/category_news_list', methods=['GET'])
def public_news_display():

    userId = request.args.get('user_id')
    lang = request.args.get('lang')

    new_mysql = mysql_utils()
    query_txt = News_sql.query_category_news(userId,lang)

    res = new_mysql.do_execute(query_txt)
    return jsonify({"display_news_list": res})

@news_blueprint.route('/api/news_detail', methods=['GET'])
def news_detail_display():
    id = request.args.get('new_id')
    userId = request.args.get('user_id')
    print(id,userId)
    new_mysql = mysql_utils()
    query_txt = News_sql.query_by_id(int(id))
    news_detail = new_mysql.do_execute(query_txt,isSingle=True)

    current_date_str = datetime.now().strftime("%Y-%m-%d")
    current_date_str


    histroy_add_txt = History_sql.add_history_sql(id,userId,current_date_str)
    new_mysql.do_execute(histroy_add_txt,isSingle=True)

    return jsonify({"news_detail":news_detail})

@news_blueprint.route('/api/recommend_news_list', methods=['GET'])
def news_recommendation_list():
    userId = request.args.get('user_id')
    lang = request.args.get('lang')
    recommend_news_list = get_recommend_news_list(userId,lang)
    if recommend_news_list:
        return jsonify({"news_recommend_list": recommend_news_list})
    else:
        return jsonify({"error": "No recommend content!"})


@news_blueprint.route('/api/news_summary', methods = ['GET'])
def news_summary():
    userId = request.args.get('user_id')
    lang = request.args.get('lang')
    newsId = request.args.get('news_id')

    if (newsId and userId and lang):
        news_summary = get_news_summary(userId, lang, newsId)

    if news_summary:
        return jsonify({"news_summary": news_summary})
    else:
        return jsonify({"error": "No summary content!"})