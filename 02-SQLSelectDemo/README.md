### 记录一次复杂查询

### 第一步 创建数据

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer
import pymysql
from sqlalchemy import Column, BigInteger, String, DateTime
from Util import get_now_time, json_data, get_user_data

# 相关配置
app = Flask(__name__)

# 创建组件对象
db = SQLAlchemy(app)
pymysql.install_as_MySQLdb()
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://******:******@**.**.***.***:****/dev"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True


# 数据库 - models
class UserLiveRecord(db.Model):
    """
        用户观看记录表
    """
    __tablename__ = 'user_live_record'

    id = Column(BigInteger, primary_key=True)
    company_type = Column(Integer)
    live_video_id = Column(BigInteger)
    pm = Column(Integer)
    openid = Column(String(200, 'utf8mb4_general_ci'))
    user_id = Column(String(200, 'utf8mb4_general_ci'))
    user_name = Column(String(200, 'utf8mb4_general_ci'))
    terminal_type = Column(String(200, 'utf8mb4_general_ci'))
    ip = Column(String(200, 'utf8mb4_general_ci'))
    ts_in = Column(String(200, 'utf8mb4_general_ci'))
    ts_out = Column(String(200, 'utf8mb4_general_ci'))
    user_type = Column(Integer)
    online = Column(Integer)
    create_time = Column(DateTime)

    def save(self):
        self.create_time = get_now_time()


"""
数据库 - 表 - 创建语句
CREATE TABLE `user_live_record` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `company_type` int(11) DEFAULT NULL COMMENT '1-上海昶晁 2-四川钱坤 3-上海仕祁 4-上海岙舟 5-福州',
  `live_video_id` bigint(20) DEFAULT NULL COMMENT 'live_video的主键',
  `pm` int(11) DEFAULT NULL,
  `openid` varchar(200) DEFAULT NULL COMMENT 'openid',
  `user_id` varchar(200) DEFAULT NULL COMMENT '用户id',
  `user_name` varchar(200) DEFAULT NULL COMMENT '用户名',
  `terminal_type` varchar(200) DEFAULT NULL COMMENT '类型 PC wap',
  `ip` varchar(200) DEFAULT NULL COMMENT 'ip',
  `ts_in` varchar(200) DEFAULT NULL COMMENT '进入时间',
  `ts_out` varchar(200) DEFAULT NULL COMMENT '离开时间',
  `user_type` tinyint(4) DEFAULT '0' COMMENT '0代表用户以学生身份进入, 1表示用户以老师身份进入',
  `online` int(11) DEFAULT '0' COMMENT '用户在线时长, ts_in与ts_out的差值, 以秒为单位',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='客户观看记录表';
"""


def create_data():
    """
    创建数据
    :return:
    """
    conten_list = json_data.get("content")

    for conten in conten_list:
        user_id = conten.get("user_id")
        user_name = conten.get("user_name")
        ip = conten.get("ip")
        user_type = conten.get("user_type")
        ts_in = conten.get("ts_in")
        ts_out = conten.get("ts_out")
        online = conten.get("online")

        pm, terminal_type, openid = get_user_data(user_id)
        user_live_record = UserLiveRecord()
        user_live_record.live_video_id = 453
        user_live_record.pm = pm
        user_live_record.openid = openid if openid else user_id
        user_live_record.user_id = user_id
        user_live_record.user_name = user_name
        user_live_record.terminal_type = terminal_type if terminal_type else 'pc'
        user_live_record.ip = ip
        user_live_record.ts_in = ts_in
        user_live_record.ts_out = ts_out
        user_live_record.user_type = user_type
        user_live_record.online = online
        user_live_record.company_type = 9

        user_live_record.save()
        db.session.add(user_live_record)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    create_data()

```



### 第二步 查询

> 查询某一时间段内的用户观看时长统计、微信账户数(UV)、用户登录次数(PV)

![image-20220622100420262](https://picture-typora-bucket.oss-cn-shanghai.aliyuncs.com/typora/image-20220622100420262.png)

#### 情况一

```mysql
-- sql：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.company_type = 9 
	AND user_live_record.user_type = 0 
	AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) <= '开始时间' 
	AND ( str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) BETWEEN '开始时间' AND '结束时间' )


-- 示例：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.company_type = 9 
	AND user_live_record.user_type = 0 
	AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) <= '2022-06-21 19:30:00' 
	AND ( str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00' )
```

#### 情况二

```mysql
-- sql：
SELECT
	* 
FROM
	user_live_record 
WHERE
		user_live_record.user_type = 0 
		AND user_live_record.company_type = 9 
		AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) <= '开始时间' AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) >= '结束时间' 
	
	
-- 示例：
SELECT
	* 
FROM
	user_live_record 
WHERE
		user_live_record.user_type = 0 
		AND user_live_record.company_type = 9 
		AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) <= '2022-06-21 19:30:00' AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) >= '2022-06-21 19:40:00' 
	
```

#### 情况三

```mysql
-- sql：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.user_type = 0 
	AND user_live_record.company_type = 9 
	AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) >= '开始时间' 
	AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) <= '结束时间'
	
	
-- 示例：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.user_type = 0 
	AND user_live_record.company_type = 9 
	AND str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) >= '2022-06-21 19:30:00' 
	AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) <= '2022-06-21 19:40:00'
```

#### 情况四

```mysql
-- sql：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.user_type = 0 
	AND user_live_record.company_type = 9 
	AND ( str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) BETWEEN '开始时间' AND '结束时间' ) 
	AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) >= '结束时间'
	
	
-- 示例：
SELECT
	* 
FROM
	user_live_record 
WHERE
	user_live_record.user_type = 0 
	AND user_live_record.company_type = 9 
	AND ( str_to_date( user_live_record.ts_in, '%Y-%m-%d %k:%i:%s' ) BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00' ) 
	AND str_to_date( user_live_record.ts_out, '%Y-%m-%d %k:%i:%s' ) >= '2022-06-21 19:40:00'
```

### 第三步 查询汇总

```mysql
-- sql：
SELECT *
FROM user_live_record
WHERE user_live_record.company_type = 9
    AND user_live_record.user_type = 0
    AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间'
    AND
      (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间' AND
            str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '开始时间'
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '结束时间'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND
            (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'
    )
    
-- 示例：
SELECT *
FROM user_live_record
WHERE user_live_record.company_type = 9
    AND user_live_record.user_type = 0
    AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00'
    AND
      (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00' AND
            str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:30:00'
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:40:00'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND
            (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'
    )
```

### 第四步 计算时间差

#### ![image-20220623130256987](https://picture-typora-bucket.oss-cn-shanghai.aliyuncs.com/typora/image-20220623130256987.png)

```mysql
-- sql：
SELECT *,
       IF
           (
               (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间' AND
                str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '结束时间'),
               timestampdiff(
                   SECOND, '开始时间',
                           str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s')),
               IF
                   (
                       (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '结束时间' AND
                        str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '开始时间'),
                       timestampdiff(
                           SECOND, str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s'),
                                   str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s')),
                       IF
                           (
                                   str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '开始时间',
                                   timestampdiff(SECOND, str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s'),
                                                         '结束时间'),
                                   timestampdiff(SECOND, '开始时间', '结束时间')))) AS ONLINE
FROM user_live_record
WHERE user_live_record.company_type = 9
    AND user_live_record.user_type = 0
    AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间'
    AND
      (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间' AND
            str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '开始时间'
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '结束时间'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND
            (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'
    )


-- 示例：
SELECT *,
       IF
           (
               (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00' AND
                str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:40:00'),
               timestampdiff(
                   SECOND, '2022-06-21 19:30:00',
                           str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s')),
               IF
                   (
                       (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:40:00' AND
                        str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:30:00'),
                       timestampdiff(
                           SECOND, str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s'),
                                   str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s')),
                       IF
                           (
                                   str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:30:00',
                                   timestampdiff(SECOND, str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s'),
                                                         '2022-06-21 19:40:00'),
                                   timestampdiff(SECOND, '2022-06-21 19:30:00', '2022-06-21 19:40:00')))) AS ONLINE
FROM user_live_record
WHERE user_live_record.company_type = 9
    AND user_live_record.user_type = 0
    AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00'
    AND
      (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00' AND
            str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:30:00'
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:40:00'
    )
   OR (
            user_live_record.user_type = 0
        AND user_live_record.company_type = 9
        AND
            (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')
        AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'
    )
```

