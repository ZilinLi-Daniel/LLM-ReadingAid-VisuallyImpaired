class User_sql:
    def __init__(self):
        pass

    @staticmethod
    def query_user_exist_sql(email):
        '''
        根据用户提交的用户名查询数据库是否存在该用户
        :param username:
        :return: 用户查询sql
        '''
        sql_txt = f"SELECT COUNT(email) FROM user WHERE email = '{email}'"
        return sql_txt

    @staticmethod
    def validate_user_login_sql(email, password):
        sql_txt = f"SELECT COUNT(email) FROM user WHERE email = '{email}' and password = '{password}'"
        return sql_txt

    @staticmethod
    def register_user_sql(username, email, password):
        '''
        根据用户提交的用户名和密码和其他信息完成用户注册
        :param username:
        :param password:
        :param 其他信息
        :return: 注册返回的sql
        '''
        sql_txt = f"INSERT INTO user (username,email,password) values ('{username}','{email}','{password}')"
        return sql_txt

    @staticmethod
    def query_userId_by_email(email):
        '''
        根据邮箱来获取用户id，然后进一步的获取偏好
        :param email:
        :return:
        '''
        sql_txt = f"SELECT userId FROM user where email = '{email}'"
        return sql_txt

