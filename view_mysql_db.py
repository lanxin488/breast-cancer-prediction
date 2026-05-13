# -*- coding: utf-8 -*-
"""
乳腺癌预测系统 - MySQL数据库查看工具
使用方法：运行此脚本，即可查看数据库中的用户和预测记录
"""

import pymysql
import os

# MySQL配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '488656920lP@',
    'database': 'breast_cancer_db',
    'charset': 'utf8mb4'
}

def connect_db():
    """连接MySQL数据库"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ 连接数据库失败: {e}")
        return None

def show_users(conn):
    """显示所有用户"""
    print("\n" + "="*60)
    print("👥 用户列表")
    print("="*60)
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, username, email, created_at FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("  暂无用户")
        return
    
    print(f"  共 {len(users)} 个用户")
    print("-"*60)
    print("  ID | 用户名 | 邮箱 | 创建时间")
    print("-"*60)
    for user in users:
        print(f"  {user['id']:3d} | {user['username']:10s} | {user['email']:20s} | {user['created_at']}")

def show_predictions(conn):
    """显示所有预测记录"""
    print("\n" + "="*60)
    print("📊 预测记录")
    print("="*60)
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT p.id, u.username, p.result, p.confidence, p.malignant_prob, p.benign_prob, p.model_used, p.created_at
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC
    """)
    predictions = cursor.fetchall()
    
    if not predictions:
        print("  暂无预测记录")
        return
    
    print(f"  共 {len(predictions)} 条预测记录")
    print("-"*60)
    print("  ID | 用户名 | 结果 | 置信度 | 恶性概率 | 良性概率 | 使用模型 | 预测时间")
    print("-"*60)
    for pred in predictions:
        result = "🟢 良性" if pred['result'] == '良性' else "🔴 恶性"
        print(f"  {pred['id']:3d} | {pred['username']:10s} | {result} | {pred['confidence']*100:5.1f}% | {pred['malignant_prob']*100:7.1f}% | {pred['benign_prob']*100:7.1f}% | {pred['model_used']:12s} | {pred['created_at']}")

def show_stats(conn):
    """显示统计信息"""
    print("\n" + "="*60)
    print("📈 统计信息")
    print("="*60)
    
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions")
    pred_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE result = '恶性'")
    malignant_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE result = '良性'")
    benign_count = cursor.fetchone()[0]
    
    print(f"  用户总数: {user_count}")
    print(f"  预测记录总数: {pred_count}")
    print(f"  良性预测: {benign_count}")
    print(f"  恶性预测: {malignant_count}")
    if pred_count > 0:
        print(f"  恶性占比: {malignant_count/pred_count*100:.1f}%")

def main():
    """主函数"""
    print("🌟 乳腺癌预测系统 - MySQL数据库查看工具")
    print("="*60)
    
    conn = connect_db()
    if not conn:
        return
    
    try:
        show_stats(conn)
        show_users(conn)
        show_predictions(conn)
    finally:
        conn.close()
    
    print("\n" + "="*60)
    print("✅ 查看完成")
    input("\n按 Enter 键退出...")

if __name__ == '__main__':
    main()