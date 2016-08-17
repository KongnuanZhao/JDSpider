import psycopg2
import ConfigParser
import os
import sys

insertBrand = "insert into jd_mobile_brand(name,url,link) values(%s,%s,%s)"
selectBrand = "select * from jd_mobile_brand"
insertModel = "insert into jd_mobile_model(brand_id,name,url,price) values(%s,%s,%s,%s)"
selectModel = "select * from jd_mobile_model"
selectSubModel = "select * from jd_sub_model where id not in (select sub_mobile_id from jd_mobile_param)"


def getConn():
    conn = psycopg2.connect(database="postgres", user="postgres", host="127.0.0.1", port="5432")
    # conn = psycopg2.connect(database="lotuseed_apk", user="lotuseed_apk", host="192.168.0.64", port="1922")
    return conn


def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


def file_path(dirname, filename):
    curPath = cur_file_dir()
    filePath = (curPath + "/../%s/%s") % (dirname, filename)
    return filePath


def insert(dict_list, sql_name):
    conn = getConn()
    cur = conn.cursor()
    cur.executemany(sql_name, dict_list)
    conn.commit()
    print "success"
    cur.close()
    conn.close()


def update(dict_list, sql_name):
    conn = getConn()
    cur = conn.cursor()
    cur.executemany(sql_name, dict_list)
    conn.commit()
    cur.close()
    conn.close()


def select_brand(sql_name):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(sql_name)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def select(sql_name):
    conn = getConn()
    cur = conn.cursor()
    cur.execute(sql_name)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# if __name__=='__main__':
#     result=select_brand("brand_url")
#     for tag in result:
#         print tag
