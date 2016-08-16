# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class JdspiderPipeline(object):
    def process_item(self, item, spider):
        try:
            conn = psycopg2.connect(database="postgres", user="postgres", host="127.0.0.1", port="5432")
            cur = conn.cursor()
        except Exception, e:
            print "connect error", str(e)
            return False
        try:
            cur.execute("""insert into jd_sub_model (brand_id,model_id,name,url,price)
                values(%s,%s,%s,%s,%s);""", (item['brand_id'], item['model_id'], item['name'],
                                             item['url'], item['price']))
            conn.commit()
            print "SUCC INSERT ONE ROWS !"
        except Exception, e:
            print e
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return item
