爬取思路，先爬取所有手机品牌，然后爬取手机品牌下的型号，再爬取某个型号下的具体机型，最后爬取具体机型的具体参数

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