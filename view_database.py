# -*- coding: utf-8 -*-
"""
乳腺癌预测系统 - 数据库查看工具
使用方法：运行此脚本，即可查看数据库中的用户和预测记录
"""

import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'breast_cancer.db')

def connect_db():
    """连接数据库"""
    if not os.path.exists(DB_PATH):
        print(f"❌ 数据库文件不存在: {DB_PATH}")
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ 连接数据库失败: {e}")
        return None

def show_users(conn):
    """显示所有用户"""
    print("\n" + "="*60)
    print("👥 用户列表")
    print("="*60)
    
    cursor = conn.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("  暂无用户")
        return
    
    print(f"  共 {len(users)} 个用户")
    print("-"*60)
    print("  ID | 用户名 | 邮箱")
    print("-"*60)
    for user in users:
        print(f"  {user['id']:3d} | {user['username']:10s} | {user['email']}")

def show_predictions(conn):
    """显示所有预测记录"""
    print("\n" + "="*60)
    print("📊 预测记录")
    print("="*60)
    
    cursor = conn.execute("""
        SELECT p.id, u.username, p.result, p.confidence, p.malignant_prob, p.created_at
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
    print("  ID | 用户名 | 结果 | 置信度 | 恶性概率 | 预测时间")
    print("-"*60)
    for pred in predictions:
        result = "🟢 良性" if pred['result'] == '良性' else "🔴 恶性"
        print(f"  {pred['id']:3d} | {pred['username']:10s} | {result} | {pred['confidence']*100:5.1f}% | {pred['malignant_prob']*100:7.1f}% | {pred['created_at']}")

def show_stats(conn):
    """显示统计信息"""
    print("\n" + "="*60)
    print("📈 统计信息")
    print("="*60)
    
    # 用户统计
    cursor = conn.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    # 预测统计
    cursor = conn.execute("SELECT COUNT(*) FROM predictions")
    pred_count = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM predictions WHERE result = '恶性'")
    malignant_count = cursor.fetchone()[0]
    
    cursor = conn.execute("SELECT COUNT(*) FROM predictions WHERE result = '良性'")
    benign_count = cursor.fetchone()[0]
    
    print(f"  用户总数: {user_count}")
    print(f"  预测记录总数: {pred_count}")
    print(f"  良性预测: {benign_count}")
    print(f"  恶性预测: {malignant_count}")
    if pred_count > 0:
        print(f"  恶性占比: {malignant_count/pred_count*100:.1f}%")

def main():
    """主函数"""
    print("🌟 乳腺癌预测系统 - 数据库查看工具")
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
