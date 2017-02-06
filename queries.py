GET_ALL_RESTAURANTS = 'SELECT * FROM restaurants;'
INSERT_INTERESTED = 'INSERT INTO interested ({keys}) values ({values});'
GET_ALL_RELEVANT_MATCHES = """
SELECT res.rest_name, res.rest_image, res.users
FROM
    (SELECT r.name as rest_name, r.image as rest_image, json_agg(user_data.*) as users, array_length(array_agg(user_data.user_id), 1) as length
    FROM
          (
        SELECT p.*, i.going, i.restaurant_name
        FROM interested as i
        INNER JOIN people as p ON i.user_id = p.user_id
          ) as user_data
    INNER JOIN restaurants as r ON r.name = user_data.restaurant_name
    GROUP BY r.name,r.image) as res
ORDER BY res.length DESC
"""
LOGIN = 'INSERT INTO people ({keys}) values ({values});'
GET_ALL_GOING = """
SELECT res.rest_name, res.users
FROM
    (SELECT r.name as rest_name, r.image as rest_image, json_agg(user_data.name) as users, array_length(array_agg(user_data.user_id), 1) as length
    FROM
          (
        SELECT p.*, i.going, i.restaurant_name
        FROM interested as i
        INNER JOIN people as p ON i.user_id = p.user_id where i.going=true
          ) as user_data
    INNER JOIN restaurants as r ON r.name = user_data.restaurant_name
    GROUP BY r.name,r.image) as res
ORDER BY res.length DESCs"""