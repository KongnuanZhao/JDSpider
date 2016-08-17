爬取思路，先爬取所有手机品牌，然后爬取手机品牌下的型号，再爬取某个型号下的具体机型，最后爬取具体机型的具体参数
爬取品牌和型号逻辑比较简单，执行test目录下的`jd_brand.py`和`jd_model`爬取入库
然后执行 `scrapy crawl jd_spider`爬取具体机型
最后 `cd jdparam`爬取具体机型对应的参数 `scrapy crawl jd_param`

建表
create table jd_mobile_brand(
id serial PRIMARY KEY,
name varchar(128),
url text,
input_date date DEFAULT CURRENT_DATE,
link text
)

create table jd_mobile_model(
id serial PRIMARY KEY,
brand_id int REFERENCES jd_mobile_brand(id),
name text,
url text,
price text,
input_date date DEFAULT CURRENT_DATE
)

create table jd_sub_model(
id serial PRIMARY KEY,
brand_id int REFERENCES jd_mobile_brand(id),
model_id int REFERENCES jd_mobile_model(id),
name text,
url text,
price text,
input_date date DEFAULT CURRENT_DATE
)

参数表字段说明：
  主体 bodyinfos
 基本信息 base_info
 操作系统 mobile_os
 主芯片  mobile_cpu
 网络支持 mobile_internet 网络
 存储 mobile_store
 屏幕 mobile_screen 显示
 前置摄像头 front_camera
 后置摄像头 rear_camera 摄像功能
 电池信息 battery_info
 数据接口 data_interface 传输功能
 手机特性 mobile_feature 其他

create table jd_mobile_param(
id serial PRIMARY KEY,
sub_mobile_id int REFERENCES jd_sub_model(id),
bodyinfos text,
base_info text,
mobile_os text,
mobile_cpu text,
mobile_internet text,
mobile_store text,
mobile_screen text,
front_camera text,
rear_camera text,
battery_info text,
data_interface text,
mobile_feature text,
input_date date DEFAULT CURRENT_DATE
)