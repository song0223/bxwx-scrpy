import mysql.connector
from bxwxcj import settings
import datetime

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, host=MYSQL_HOSTS, database=MYSQL_DB)
cur = cnx.cursor(buffered=True)##初始化MySQL的操作游标

class Sql:
    @classmethod##@classmethod这个是一个修饰符；作用是我们不需要初始化类就可以直接调用类中的函数使用
    def insert_xs(cls, title, author, image, is_ending, type, bxwx_id, introduction, bxwx_url):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO books(`bxwx_id`, \
               `bxwx_url`, `title`, `author`, `type`, image, `introduction`, `is_ending`, `read_count`, `created_at`, `updated_at`) \
               VALUES ('%s', '%s', '%s', '%s', '%d', '%s' , '%s', '%d', '%d', '%s', '%s')" % \
              (bxwx_id, bxwx_url, title, author, type, image, introduction, is_ending, 0, now_time, now_time)

        cur.execute(sql)##执行sql语句
        cnx.commit()##提交到数据库执行

    @classmethod
    def select_xs_id(cls, bxwx_id):
        sql = 'SELECT EXISTS(SELECT 1 FROM books WHERE bxwx_id=%(bxwx_id)s)'
        value = {
            'bxwx_id': bxwx_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

    @classmethod
    def insert_zj_content(cls, book_id, bxwx_id, bxwx_url, title, content, sort):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO book_chapter(`book_id`, `bxwx_id`, `bxwx_url`, `title`, `content`, `sort`, `created_at`, `updated_at`) VALUES (%(book_id)s, %(bxwx_id)s,%(bxwx_url)s, %(title)s, %(content)s, %(sort)s, %(created_at)s, %(updated_at)s)'
        value = {
            'book_id': book_id,
            'bxwx_id': bxwx_id,
            'bxwx_url': bxwx_url,
            'title': title,
            'content': content,
            'sort': sort,
            'created_at': now_time,
            'updated_at': now_time,
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_zj_id(cls, bxwx_id):
        sql = 'SELECT EXISTS(SELECT 1 FROM book_chapter WHERE bxwx_id=%(bxwx_id)s)'
        value = {
            'bxwx_id': bxwx_id
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]

