import pymysql

#MySQL -h localhost -u root -pwangyi
conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wangyi", db='user', charset='utf8')
#datebase, charset = utf8防止乱码
cursor = conn.cursor()
# 获取example下面的table user
# sql = 'select*from user'
# cursor.execute(sql)
# print(cursor.rowcount)
# r1 = cursor.fetchone()
# rm = cursor.fetchmany(3)
# rl = cursor.fetchall()
# print(r1)
# print(rm)
# print(rl)
# sql1 = 'select*from user'
# cursor.execute(sql1)
# ra = cursor.fetchall()
# for i in ra:
#     print('userid=%s,username=%s' % i) #自动匹配每一列
sql_insert = 'insert into user values(11, "name11")'
sql_update = 'update user set username="name9" where userid=9'
sql_delete = 'delete from user where userd<3'
try:
    cursor.execute(sql_insert)
    print(cursor.rowcount)
    cursor.execute(sql_update)
    print(cursor.rowcount)
    cursor.execute(sql_delete)
    print(cursor.rowcount)
    sql_show = 'select*from user'
    print(cursor.execute(sql_show))
    conn.commit() #使得操作生效
except Exception as e:
    print(e)
    conn.rollback()
conn.close()
cursor.close()
