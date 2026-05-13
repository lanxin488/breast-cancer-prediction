"""数据库迁移脚本 - 添加新列"""
import MySQLdb
from app import app, db

def migrate_database():
    """添加缺失的列到现有表"""
    try:
        # 连接到数据库
        conn = MySQLdb.connect(
            host='localhost',
            user='root',
            password='488656920lP@',
            db='breast_cancer_db',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        print("🔧 开始数据库迁移...")
        
        # 检查并添加 role 列到 users 表
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
            print("✅ 添加 role 列成功")
        except MySQLdb.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("ℹ️ role 列已存在，跳过")
            else:
                raise
        
        # 检查并添加 created_at 列到 users 表
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
            print("✅ 添加 created_at 列成功")
        except MySQLdb.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("ℹ️ created_at 列已存在，跳过")
            else:
                raise
        
        # 创建 health_records 表
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS health_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    age INT,
                    bmi FLOAT,
                    family_history VARCHAR(10),
                    symptoms TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✅ 创建 health_records 表成功")
        except Exception as e:
            print(f"⚠️ health_records 表可能已存在: {e}")
        
        # 创建 system_logs 表
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(50) NOT NULL,
                    details TEXT,
                    ip_address VARCHAR(50),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            print("✅ 创建 system_logs 表成功")
        except Exception as e:
            print(f"⚠️ system_logs 表可能已存在: {e}")
        
        # 为现有用户设置默认角色
        cursor.execute("UPDATE users SET role = 'user' WHERE role IS NULL OR role = ''")
        # 为 admin 用户设置管理员角色
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
        
        conn.commit()
        print("🎉 数据库迁移完成！")
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
