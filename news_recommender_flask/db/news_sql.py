class News_sql:
    def __init__(self):
        pass

    @staticmethod
    def query_category_news(userId,lang):
        '''
        根据用户的兴趣种类查询新闻
        :return: 查询新闻列表sql语句
        '''
        sql_txt = f"""
        SELECT n.*
        FROM `news` n
        WHERE
            CASE
                WHEN EXISTS (
                    SELECT 1
                    FROM `preference` p
                    WHERE p.userId = {userId}
                    AND (
                        ('{lang}' = 'zh' AND p.preferenceName IS NOT NULL) OR
                        ('{lang}' = 'en' AND p.preferenceNameEng IS NOT NULL)
                    )
                )
                THEN
                    n.news_kind IN (
                        SELECT 
                            CASE
                                WHEN '{lang}' = 'zh' THEN p.preferenceName
                                ELSE p.preferenceNameEng
                            END
                        FROM `preference` p
                        WHERE p.userId = {userId}
                    )
                ELSE 
                    CASE WHEN '{lang}' = 'zh' THEN n.news_kind = '公共' ELSE n.news_kind = 'public' END
            END = 1
        ORDER BY n.time DESC
        """
        return sql_txt

    def query_category_news_suffle(userId,lang):
        '''
        根据用户的兴趣种类查询新闻
        :return: 查询新闻列表sql语句
        '''
        sql_txt = f"""
                SELECT n.*
                FROM `news` n
                WHERE
                    CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM `preference` p
                            WHERE p.userId = {userId}
                            AND (
                                ('{lang}' = 'zh' AND p.preferenceName IS NOT NULL) OR
                                ('{lang}' = 'en' AND p.preferenceNameEng IS NOT NULL)
                            )
                        )
                        THEN
                            n.news_kind IN (
                                SELECT 
                                    CASE
                                        WHEN '{lang}' = 'zh' THEN p.preferenceName
                                        ELSE p.preferenceNameEng
                                    END
                                FROM `preference` p
                                WHERE p.userId = {userId}
                            )
                        ELSE 
                            CASE WHEN '{lang}' = 'zh' THEN n.news_kind = '公共' ELSE n.news_kind = 'public' END
                    END = 1
                ORDER BY RAND()
        """
        return sql_txt


    @staticmethod
    def query_by_id(newId):
        '''
        根据新闻id(new_id)从new_result表中获取新闻内容
        :param newId:
        :return: 查询新闻结果表sql字符串
        '''
        sql_txt = f"SELECT * FROM news WHERE newsId = {newId}"
        return sql_txt

    @staticmethod
    def query_news_exist(url):
        '''
        通过url来判断当前新闻是否存在于数据库中，避免重复插入新闻
        :param url:
        :return:
        '''
        sql_txt = f"SELECT COUNT(url) FROM news WHERE url = '{url}'"
        return sql_txt

    @staticmethod

    def insert_news_sql(title, time, content, url, category, abstract, lang):
        sql_txt = "INSERT INTO news (title, time, content, url, news_kind, abstract, lang) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = (title, time, content, url, category, abstract, lang)
        return sql_txt, params

    @staticmethod
    def query_news_by_date(currentdate,lang):
        if lang == 'zh':
            sql_txt = f"SELECT title FROM news where time = '{currentdate}' and lang = '{lang}' LIMIT 30"
        elif lang == 'en':
            sql_txt = f"SELECT title FROM news where time = '{currentdate}' and lang = '{lang}'"
        return sql_txt

    @staticmethod
    def match_newsTitle_toId(news_title,lang):
        # sql_txt = f"""
        # WITH OrderedTitles (title, ordering) AS (
        #   VALUES
        #   {newscontent_list}
        # )
        # SELECT n.newsId
        # FROM news n
        # INNER JOIN OrderedTitles ot ON n.title = ot.title
        # ORDER BY ot.ordering;
        # """
        if lang == 'zh':
            sql_txt = f"""
            select newsId,title from news where title = '{news_title}'
            """
        elif lang == 'en':
            sql_txt = f"""
            select newsId,title from news where title = "{news_title}"
            """
        return sql_txt