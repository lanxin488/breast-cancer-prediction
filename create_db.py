# 创建 MySQL 数据库
import MySQLdb

try:
    # 先连接到 MySQL（不指定数据库）
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        password='488656920lP@'
    )
    
    cursor = conn.cursor()
    
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS breast_cancer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("✅ 数据库创建成功！")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ 错误: {e}")