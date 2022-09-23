-- 情况一
-- sql：
SELECT *
FROM user_live_record
WHERE user_live_record.company_type = 9
  AND user_live_record.user_type = 0
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间'
  AND (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')


-- 示例：
SELECT *
FROM user_live_record
WHERE user_live_record.company_type = 9
  AND user_live_record.user_type = 0
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00'
  AND (str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')



-- 情况二
-- sql：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '开始时间'
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'


-- 示例：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:30:00'
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'



-- 情况三
-- sql：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '开始时间'
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '结束时间'


-- 示例：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:30:00'
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') <= '2022-06-21 19:40:00'



-- 情况四
-- sql：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '开始时间' AND '结束时间')
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '结束时间'


-- 示例：
SELECT *
FROM user_live_record
WHERE user_live_record.user_type = 0
  AND user_live_record.company_type = 9
  AND (str_to_date(user_live_record.ts_in, '%Y-%m-%d %k:%i:%s') BETWEEN '2022-06-21 19:30:00' AND '2022-06-21 19:40:00')
  AND str_to_date(user_live_record.ts_out, '%Y-%m-%d %k:%i:%s') >= '2022-06-21 19:40:00'



-- 查询汇总：
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



-- 计算时间差
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