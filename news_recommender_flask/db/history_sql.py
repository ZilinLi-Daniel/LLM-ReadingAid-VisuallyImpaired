class History_sql:
    def __init__(self):
        pass

    @staticmethod
    def add_history_sql(newId, userId, viewTime):
        '''
        当用户点击新闻的时候，添加用户的浏览记录
        :param username:
        :param password:
        :param 其他信息
        :return: 注册返回的sql
        '''
        sql_txt = f"INSERT INTO history (newId,userId,viewTime) values ('{newId}','{userId}','{viewTime}')"
        return sql_txt

    @staticmethod
    def query_user_history(userId, currentTime, lang):
        '''
        以当前时间为界限，查找用户之间的历史浏览记录，并且按照降序排列
        :param userId:
        :param currentTime:
        :return:
        '''
        sql_txt = f"SELECT news.newsId, news.title, history.viewTime \
        FROM history \
        JOIN news ON history.newId = news.newsId \
        WHERE history.userId = {userId} AND history.viewTime <= '{currentTime}' and news.lang = '{lang}'\
        ORDER BY history.viewTime DESC;"
        return sql_txt
