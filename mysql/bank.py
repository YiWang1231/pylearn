import pymysql
import sys


class TransferMoney (object):
    def __init__(self, conn):
        self.conn = conn

    def transfer(self, source_acctid, target_acctid, money):
        try:
            self.check(source_acctid)
            self.check(target_acctid)
            self.has_money(source_acctid, money)
            self.reduce_money(source_acctid, money)
            self.add_money(target_acctid, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def check(self, acctid):
        cursor = self.conn.cursor()
        try:
            sql = 'select*from bank where acctid=%s'%acctid
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账号%s不存在"%acctid)
        finally:
            cursor.close()


    def has_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'select*from bank where acctid=%s and money>%s'%(acctid, money)
            cursor.execute(sql)
            if len(rs) != 1:
                raise Exception("账号%s余额不足"%acctid)
        finally:
            cursor.close()
    def reduce_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update bank where money=money-%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            if cursor.rowconut != 1:
                raise Exception("账号%s转账失败"%acctid)
        finally:
            cursor.close()

    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = 'update bank where money=money+%s where acctid=%s'%(money, acctid)
            cursor.execute(sql)
            if cursor.rowconut != 1:
                raise Exception("账号%s收款失败"%acctid)
        finally:
            cursor.close()


if __name__ == "__main__":
    source_acctid = sys.argv[1]
    target_acctid = sys.argv[2]
    money = sys.argv[3]
    conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wangyi", db='user', charset='utf8')
    tr_money = TransferMoney(conn)
    try:
        tr_money = TransferMoney.transfer(source_acctid, target_acctid, money)
    except Exception as e:
        print("问题是：%s" + str(e))
