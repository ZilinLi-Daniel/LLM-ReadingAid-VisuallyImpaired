from flask import Blueprint,request,jsonify
from utils.mysql_utils import mysql_utils
from db.preferences_sql import Preference_sql
from db.user_sql import User_sql

user_blueprint = Blueprint('user', __name__)

kind_lang_mapping_zh = {
    '经济': 'Economy',
    '房地产': 'Real estate',
    '教育':'Education',
    '科技':'Science and Technology',
    '娱乐':'Entertainment',
    '互联网':'Internet',
    '军事':'Military',
    '社会':'Social'
}

kind_lang_mapping_en = {value:key for key,value in kind_lang_mapping_zh.items()}

@user_blueprint.route('/api/user_regist', methods = ['POST'])
def register():

    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    preferences_list = data['preferences']
    lang = data['lang']

    print(email, password, preferences_list, lang)

    if email == '' or password == '':
        return jsonify({"message":"注册失败，邮箱或密码为空"})
    new_mysql = mysql_utils()
    query_user_exist_txt = User_sql.query_user_exist_sql(email)
    res = new_mysql.do_execute(query_user_exist_txt, isSingle=True)
    if res['COUNT(email)'] != 0:
        return jsonify({"message": "用户已经存在，请登录"})
    else:
        registe_user_txt = User_sql.register_user_sql(username,email,password)
        register_id = new_mysql.do_execute(registe_user_txt)


        for preferences in preferences_list:
            if lang == 'zh':
                preferences_eng = kind_lang_mapping_zh.get(preferences)
            else:
                preferences_eng = preferences
                preferences = kind_lang_mapping_en.get(preferences_eng)

            industries_add_text = Preference_sql.add_new_preference(preferences,register_id,preferences_eng)
            res = new_mysql.do_execute(industries_add_text)
    if res:
        return jsonify({"message": "True"})
    else:
        return jsonify({"message":"False"})

@user_blueprint.route('/api/login_check', methods=['POST'])
def login():

    data = request.json
    email = data['email']
    password = data['password']
    print(email,password)
    if email == '' or password == '':
        return jsonify({"message": "登录失败，邮箱或密码为空"})

    new_mysql = mysql_utils()

    query_user_exist_txt = User_sql.query_user_exist_sql(email)
    res = new_mysql.do_execute(query_user_exist_txt,isSingle=True)
    if res['COUNT(email)'] == 0:
        return jsonify({"message":"用户不存在，请完成注册"})
    else:
        validate_user_login_sql = User_sql.validate_user_login_sql(email,password)
        res = new_mysql.do_execute(validate_user_login_sql,isSingle=True)

        if res['COUNT(email)'] == 0:
            return jsonify({"message": "用户或密码错误，请重试!"})
        else:
            query_userId_txt = User_sql.query_userId_by_email(email)
            res = new_mysql.do_execute(query_userId_txt,isSingle=True)
            return jsonify({"userId": res.get('userId'), "message":"True"})