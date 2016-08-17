# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class JdparamPipeline(object):
    def process_item(self, item, spider):
        try:
            conn = psycopg2.connect(database="postgres", user="postgres", host="127.0.0.1", port="5432")
            cur = conn.cursor()
        except Exception, e:
            print "connect error", str(e)
            return False
        try:
            cur.execute("""insert into jd_mobile_param (sub_mobile_id,bodyinfos,base_info,mobile_os,mobile_cpu,
            mobile_internet,mobile_store,mobile_screen,front_camera,rear_camera,battery_info,data_interface,mobile_feature)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""",
                        (item['sub_mobile_id'], item['bodyinfos'], item['base_info'],
                         item['mobile_os'], item['mobile_cpu'], item['mobile_internet'], item['mobile_store'],
                         item['mobile_screen'],
                         item['front_camera'], item['rear_camera'], item['battery_info'], item['data_interface'],
                         item['mobile_feature']))
            conn.commit()
            print "SUCC INSERT ONE ROWS !"
        except Exception, e:
            print e
            conn.rollback()
        finally:
            cur.close()
            conn.close()
        return item
