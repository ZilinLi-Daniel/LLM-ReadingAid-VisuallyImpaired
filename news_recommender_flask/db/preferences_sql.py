'''
对用户偏爱的新闻类别的相关操作
Table_name: preference
'''

class Preference_sql:
    def __init__(self):
        pass

    @staticmethod
    def query_all_preference():
        '''
        查询偏好表的所有偏好
        :return: 查询行业列表sql语句
        '''
        sql_txt = "SELECT * FROM  preference"
        return sql_txt

    @staticmethod
    def add_new_preference(prference_name,user_id,prference_name_Eng):
        '''
        当用户注册的时候，添加用户感兴趣的新闻种类记录
        :return: 查询新闻结果表sql字符串
        '''
        sql_txt = f"INSERT INTO preference (preferenceName, userId, preferenceNameEng) values ('{prference_name}','{user_id}','{prference_name_Eng}')"
        return sql_txt