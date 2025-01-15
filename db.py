import mysql.connector
import hashlib
import datetime

# 數據庫連接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': '',
    'password': '',
    'database': 'CHART'
}

def fetch_data_from_mysql(query):
    """
    從 MySQL 獲取數據，並將 datetime 類型轉換為字符串。
    """
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        # 將 datetime 轉換為字符串
        for row in results:
            if 'updated_at' in row and isinstance(row['updated_at'], datetime.datetime):
                row['updated_at'] = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
        return results
    finally:
        cursor.close()
        connection.close()

def hash_data(data):
    """
    生成數據的哈希值。
    """
    return hashlib.sha256(str(data).encode('utf-8')).hexdigest()
