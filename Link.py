import sqlite3
from random import choices
import string

class Link:
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()
        self.short_link = self.get_short_link()
    def getLinks(self):
        sql = '''SELECT * FROM links'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []
    def addLinks(self,full_link,short_link):
        try:
            self.__cur.execute("INSERT INTO links VALUES(NULL,?,?)",(full_link,short_link))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка загрузки ссылки в БД " + str(e))
            return False
        return True
    def get_short_link(self):
        fragm = string.digits + string.ascii_letters
        short_link = ''.join(choices(fragm, k=5))
        sql = "SELECT * FROM links"
        try:
            self.__cur.execute(sql)
            result = self.__cur.fetchall()
        except:
            print("Ошибка чтения из БД")
            return "Error - Ошибка чтения из БД"
        if result:
            for link in result:
                if link['short_link'] == short_link:
                    return self.get_short_link()
                else:
                    continue
        return short_link