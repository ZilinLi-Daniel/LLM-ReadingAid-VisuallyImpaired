from flask import Flask
from flask_cors import *
from core.user_functions import user_blueprint
from core.news_functions import news_blueprint

app = Flask(__name__)
# 设定跨域请求
CORS(app, resources=r'/*')

app.register_blueprint(user_blueprint)
app.register_blueprint(news_blueprint)
if __name__ == '__main__':
    # get_daily_news(50)
    app.run()