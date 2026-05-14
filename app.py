from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import pickle
import os
import requests
from datetime import datetime
import json
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import time
import traceback
from knowledge_base import knowledge_base

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'breast_cancer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'
DEEPSEEK_API_KEY = 'sk-1e8e125b419b4c238a6b469f102e2c23'
COZE_API_URL = 'https://api.coze.cn/v3/chat/completions'
COZE_TOKEN = 'pat_s2dS5s3Xq7Z8J4k6Y8aQ5dP9jW2aL8eS5xW5xQ9xZ0nK5mT7tY3bK2cQ7eP6tY5'
BOT_ID = '7479247948073238536'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.now)

    predictions = db.relationship('Prediction', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    input_data = db.Column(db.JSON)
    malignant_prob = db.Column(db.Float)
    benign_prob = db.Column(db.Float)
    risk_level = db.Column(db.String(20))

class HealthProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    family_history = db.Column(db.Boolean, default=False)
    previous_conditions = db.Column(db.Text)
    lifestyle = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.now)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class BreastCancerModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
                            'smoothness_mean', 'compactness_mean', 'concavity_mean',
                            'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
                            'radius_se', 'texture_se', 'perimeter_se', 'area_se',
                            'smoothness_se', 'compactness_se', 'concavity_se',
                            'concave points_se', 'symmetry_se', 'fractal_dimension_se',
                            'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
                            'smoothness_worst', 'compactness_worst', 'concavity_worst',
                            'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst']
        self.is_trained = False
        self._load_or_train_model()

    def _load_or_train_model(self):
        try:
            with open('model.pkl', 'rb') as f:
                self.model, self.scaler = pickle.load(f)
                self.is_trained = True
        except:
            self._train_model()

    def _train_model(self):
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import load_breast_cancer
        from sklearn.model_selection import train_test_split

        data = load_breast_cancer()
        X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)

        with open('model.pkl', 'wb') as f:
            pickle.dump((self.model, self.scaler), f)
        self.is_trained = True

    def predict(self, features):
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        result = '恶性' if prediction == 0 else '良性'
        confidence = max(probabilities) * 100
        
        return {
            'result': result,
            'confidence': confidence,
            'malignant_prob': probabilities[0] * 100,
            'benign_prob': probabilities[1] * 100,
            'risk_level': '高风险' if result == '恶性' else '低风险'
        }

    def get_feature_importance(self, top_n=10):
        if not self.is_trained:
            return []
        
        importances = list(zip(self.feature_names, self.model.feature_importances_))
        importances.sort(key=lambda x: x[1], reverse=True)
        
        return importances[:top_n]

    def get_model_metrics(self):
        from sklearn.datasets import load_breast_cancer
        from sklearn.model_selection import cross_val_score

        data = load_breast_cancer()
        X_scaled = self.scaler.transform(data.data)
        scores = cross_val_score(self.model, X_scaled, data.target, cv=5)

        return {
            'accuracy': np.mean(scores),
            'accuracy_std': np.std(scores)
        }

breast_cancer_model = BreastCancerModel()

def add_system_log(user_id, action, details, ip_address=None):
    log = SystemLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address
    )
    db.session.add(log)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            add_system_log(user.id, 'login', '用户登录成功', request.remote_addr)
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册', 'error')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        add_system_log(user.id, 'register', '新用户注册', request.remote_addr)
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    add_system_log(current_user.id, 'logout', '用户退出登录', request.remote_addr)
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc()).limit(5).all()
    
    total_predictions = Prediction.query.filter_by(user_id=current_user.id).count()
    malignant_predictions = Prediction.query.filter_by(user_id=current_user.id, result='恶性').count()
    
    return render_template('dashboard.html',
                         recent_predictions=recent_predictions,
                         total_predictions=total_predictions,
                         malignant_predictions=malignant_predictions)

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        try:
            features = [float(request.form.get(feature, 0)) for feature in breast_cancer_model.feature_names]
            
            result = breast_cancer_model.predict(features)
            
            prediction = Prediction(
                user_id=current_user.id,
                result=result['result'],
                confidence=result['confidence'],
                input_data=dict(zip(breast_cancer_model.feature_names, features)),
                malignant_prob=result['malignant_prob'],
                benign_prob=result['benign_prob'],
                risk_level=result['risk_level']
            )
            db.session.add(prediction)
            db.session.commit()
            
            add_system_log(current_user.id, 'prediction', 
                         f'预测结果: {result["result"]}, 置信度: {result["confidence"]:.2f}%', 
                         request.remote_addr)
            
            return jsonify({
                'success': True,
                'result': result['result'],
                'confidence': result['confidence'],
                'malignant_prob': result['malignant_prob'],
                'benign_prob': result['benign_prob'],
                'prediction_id': prediction.id,
                'top_features': breast_cancer_model.get_feature_importance(5)
            })
            
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('predict.html')

@app.route('/api/predict', methods=['POST'])
@login_required
def api_predict():
    try:
        data = request.get_json()
        features = [float(data.get(feature, 0)) for feature in breast_cancer_model.feature_names]
        
        result = breast_cancer_model.predict(features)
        
        prediction = Prediction(
            user_id=current_user.id,
            result=result['result'],
            confidence=result['confidence'],
            input_data=dict(zip(breast_cancer_model.feature_names, features)),
            malignant_prob=result['malignant_prob'],
            benign_prob=result['benign_prob'],
            risk_level=result['risk_level']
        )
        db.session.add(prediction)
        db.session.commit()
        
        add_system_log(current_user.id, 'prediction', 
                     f'预测结果: {result["result"]}, 置信度: {result["confidence"]:.2f}%', 
                     request.remote_addr)
        
        return jsonify({
            'success': True,
            'result': result['result'],
            'confidence': result['confidence'],
            'malignant_prob': result['malignant_prob'],
            'benign_prob': result['benign_prob'],
            'prediction_id': prediction.id,
            'top_features': breast_cancer_model.get_feature_importance(5)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/prediction-report')
@login_required
def prediction_report():
    predictions = Prediction.query.filter_by(user_id=current_user.id)\
        .order_by(Prediction.created_at.desc()).all()
    
    total = len(predictions)
    benign_count = len([p for p in predictions if p.result == '良性'])
    malignant_count = len([p for p in predictions if p.result == '恶性'])
    avg_confidence = sum([p.confidence for p in predictions]) / total if total > 0 else 0
    
    return render_template('prediction_report.html', predictions=predictions,
                         total=total, benign_count=benign_count,
                         malignant_count=malignant_count, avg_confidence=round(avg_confidence, 2))

@app.route('/prediction/<int:prediction_id>')
@login_required
def prediction_detail(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    if prediction.user_id != current_user.id and not current_user.is_admin():
        flash('无权访问此预测记录', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('prediction_detail.html', prediction=prediction)

@app.route('/export-prediction/<int:prediction_id>')
@login_required
def export_prediction(prediction_id):
    prediction = Prediction.query.get_or_404(prediction_id)
    
    if prediction.user_id != current_user.id and not current_user.is_admin():
        flash('无权访问此预测记录', 'error')
        return redirect(url_for('dashboard'))
    
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph('乳腺癌预测报告', styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'预测日期: {prediction.created_at.strftime("%Y-%m-%d %H:%M:%S")}', styles['Normal']))
    story.append(Paragraph(f'预测结果: {prediction.result}', styles['Heading2']))
    story.append(Paragraph(f'置信度: {prediction.confidence:.2f}%', styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph('健康建议:', styles['Heading2']))
    story.append(Paragraph(get_health_advice(prediction), styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'prediction_report_{prediction_id}.pdf', mimetype='application/pdf')

def get_health_advice(prediction):
    advice = []
    if prediction.result == '恶性':
        advice.append('1. 立即预约乳腺专科医生进行面诊')
        advice.append('2. 准备好所有检查报告供医生参考')
        advice.append('3. 遵从医嘱进行进一步检查（如穿刺活检）')
        advice.append('4. 保持积极心态，及时治疗')
        advice.append('')
        advice.append('【专业医疗咨询渠道】')
        advice.append('• 中国抗癌协会：www.caca.org.cn')
        advice.append('• 中国乳腺癌筛查指南：www.nhc.gov.cn')
        advice.append('• 中国医学科学院肿瘤医院：www.cicams.ac.cn')
        advice.append('• 北京协和医院乳腺外科：www.pumch.ac.cn')
        advice.append('• 复旦大学附属肿瘤医院：www.shca.org.cn')
        advice.append('')
        advice.append('【温馨提示】请尽快到当地三甲医院乳腺专科就诊，遵循专业医生建议。')
    else:
        advice.append('1. 定期进行乳腺检查，建议每年一次')
        advice.append('2. 保持健康的生活方式')
        advice.append('3. 学习乳腺自我检查方法')
        advice.append('4. 如有不适，及时就医')
    return '\n'.join(advice)

@app.route('/health-profile', methods=['GET', 'POST'])
@login_required
def health_profile():
    profile = HealthProfile.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        if not profile:
            profile = HealthProfile(user_id=current_user.id)
        
        profile.age = request.form.get('age', type=int)
        profile.family_history = request.form.get('family_history') == 'on'
        profile.previous_conditions = request.form.get('previous_conditions')
        profile.lifestyle = request.form.get('lifestyle')
        profile.last_updated = datetime.now()
        
        db.session.add(profile)
        db.session.commit()
        
        add_system_log(current_user.id, 'update_profile', '更新健康档案', request.remote_addr)
        flash('健康档案已更新', 'success')
    
    return render_template('health_profile.html', profile=profile)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'password' in request.form and request.form.get('password'):
            current_user.set_password(request.form.get('password'))
        
        if 'email' in request.form:
            current_user.email = request.form.get('email')
        
        db.session.commit()
        add_system_log(current_user.id, 'update_settings', '更新个人设置', request.remote_addr)
        flash('个人信息已更新', 'success')
    
    predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    prediction_count = len(predictions)
    benign_count = len([p for p in predictions if p.result == '良性'])
    malignant_count = len([p for p in predictions if p.result == '恶性'])
    
    return render_template('profile.html', user=current_user, 
                         prediction_count=prediction_count,
                         benign_count=benign_count,
                         malignant_count=malignant_count)

@app.route('/admin-db')
@login_required
def admin_db():
    if not current_user.is_admin():
        flash('无权访问管理后台', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    logs = SystemLog.query.order_by(SystemLog.created_at.desc()).limit(50).all()
    
    return render_template('admin_db.html', users=users, logs=logs)

@app.route('/admin/promote/<int:user_id>')
@login_required
def promote_user(user_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': '无权操作'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': '不能修改自己的角色'}), 400
    
    user.role = 'admin'
    db.session.commit()
    add_system_log(current_user.id, 'promote_user', f'管理员将用户 {user.username} 升级为管理员')
    return jsonify({'success': True, 'message': f'已将 {user.username} 升级为管理员'})

@app.route('/admin/demote/<int:user_id>')
@login_required
def demote_user(user_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': '无权操作'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': '不能降级自己'}), 400
    
    user.role = 'user'
    db.session.commit()
    add_system_log(current_user.id, 'demote_user', f'管理员将用户 {user.username} 降级为普通用户')
    return jsonify({'success': True, 'message': f'已将 {user.username} 降级为普通用户'})

@app.route('/api/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    data = request.get_json()
    question = data.get('question', '')

    if not question.strip():
        return jsonify({'success': False, 'message': '请输入问题'}), 400

    answer = knowledge_base.find_answer(question)
    source = '<span class="ai-source">📚 健康知识库</span>'
    
    return jsonify({'success': True, 'answer': answer + source, 'source': 'knowledge_base'})

@app.route('/health-info')
def health_info():
    return render_template('health_info.html')

@app.route('/model-performance')
def model_performance():
    metrics = breast_cancer_model.get_model_metrics()
    feature_importance = breast_cancer_model.get_feature_importance(10)
    return render_template('model_performance.html', metrics=metrics, feature_importance=feature_importance)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/model-update-log')
def model_update_log():
    return render_template('model_update_log.html')

@app.route('/ai-chat-page')
@login_required
def ai_chat_page():
    return render_template('ai_chat.html')

@app.route('/doctor-consultation')
@login_required
def doctor_consultation():
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('doctor_consultation.html', doctors=doctors)

@app.route('/community')
@login_required
def community():
    return render_template('community.html')

@app.route('/lifestyle-intervention')
@login_required
def lifestyle_intervention():
    return render_template('lifestyle_intervention.html')

@app.route('/risk-interpretation')
@login_required
def risk_interpretation():
    return render_template('risk_interpretation.html')

def init_db():
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
        
        if not User.query.filter_by(username='testuser').first():
            testuser = User(username='testuser', email='test@example.com', role='user')
            testuser.set_password('123456')
            db.session.add(testuser)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
