import mysql.connector
from mysql.connector import Error

db_config = {
    'user': 'ec2-user',
    'password': 'Shakai.Group08',
    'host': 'ec2-54-196-139-143.compute-1.amazonaws.com',  
    'database': 'failure_story_db'
}

connection = None
cursor = None

try:
    # 连接到数据库
    connection = mysql.connector.connect(**db_config)
    
    # 创建游标
    cursor = connection.cursor()
    
    # 执行查询
    query = "SELECT * FROM Post"
    cursor.execute(query)
    
    # 获取查询结果
    results = cursor.fetchall()
    
    # 处理查询结果
    for row in results:
        print(row)

except Error as err:
    print(f"Error: {err}")
finally:
    # 关闭游标和连接
    if cursor is not None:
        cursor.close()
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")