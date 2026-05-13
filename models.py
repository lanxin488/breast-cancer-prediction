from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import numpy as np
import joblib
import os

db = SQLAlchemy()
login_manager = LoginManager()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    health_records = db.relationship('HealthRecord', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin' or self.role == 'doctor'

    def is_doctor(self):
        return self.role == 'doctor'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class Prediction(db.Model):
    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    radius_mean = db.Column(db.Float, nullable=False)
    texture_mean = db.Column(db.Float, nullable=False)
    perimeter_mean = db.Column(db.Float, nullable=False)
    area_mean = db.Column(db.Float, nullable=False)
    smoothness_mean = db.Column(db.Float, nullable=False)
    compactness_mean = db.Column(db.Float, nullable=False)
    concavity_mean = db.Column(db.Float, nullable=False)
    concave_points_mean = db.Column(db.Float, nullable=False)
    symmetry_mean = db.Column(db.Float, nullable=False)
    fractal_dimension_mean = db.Column(db.Float, nullable=False)
    radius_se = db.Column(db.Float, nullable=False)
    texture_se = db.Column(db.Float, nullable=False)
    perimeter_se = db.Column(db.Float, nullable=False)
    area_se = db.Column(db.Float, nullable=False)
    smoothness_se = db.Column(db.Float, nullable=False)
    compactness_se = db.Column(db.Float, nullable=False)
    concavity_se = db.Column(db.Float, nullable=False)
    concave_points_se = db.Column(db.Float, nullable=False)
    symmetry_se = db.Column(db.Float, nullable=False)
    fractal_dimension_se = db.Column(db.Float, nullable=False)
    radius_worst = db.Column(db.Float, nullable=False)
    texture_worst = db.Column(db.Float, nullable=False)
    perimeter_worst = db.Column(db.Float, nullable=False)
    area_worst = db.Column(db.Float, nullable=False)
    smoothness_worst = db.Column(db.Float, nullable=False)
    compactness_worst = db.Column(db.Float, nullable=False)
    concavity_worst = db.Column(db.Float, nullable=False)
    concave_points_worst = db.Column(db.Float, nullable=False)
    symmetry_worst = db.Column(db.Float, nullable=False)
    fractal_dimension_worst = db.Column(db.Float, nullable=False)
    
    image_path = db.Column(db.String(255))
    result = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    malignant_prob = db.Column(db.Float, nullable=False)
    benign_prob = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(50), nullable=False, default='Random Forest')
    report_generated = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'radius_mean': self.radius_mean,
            'texture_mean': self.texture_mean,
            'perimeter_mean': self.perimeter_mean,
            'area_mean': self.area_mean,
            'smoothness_mean': self.smoothness_mean,
            'result': self.result,
            'confidence': self.confidence,
            'malignant_prob': self.malignant_prob,
            'benign_prob': self.benign_prob,
            'model_used': self.model_used,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class HealthRecord(db.Model):
    __tablename__ = 'health_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer)
    bmi = db.Column(db.Float)
    family_history = db.Column(db.Boolean, default=False)
    menarche_age = db.Column(db.Integer)
    menopause_age = db.Column(db.Integer)
    breast_feeding = db.Column(db.Boolean)
    hormone_therapy = db.Column(db.Boolean)
    previous_cancer = db.Column(db.Boolean)
    screening_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'age': self.age,
            'bmi': self.bmi,
            'family_history': self.family_history,
            'menarche_age': self.menarche_age,
            'menopause_age': self.menopause_age,
            'breast_feeding': self.breast_feeding,
            'hormone_therapy': self.hormone_therapy,
            'previous_cancer': self.previous_cancer,
            'screening_history': self.screening_history,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }


class SystemLog(db.Model):
    __tablename__ = 'system_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }


class BreastCancerModel:
    def __init__(self):
        self.rf_model = None
        self.lr_model = None
        self.scaler = None
        self.feature_names = None
        self.feature_importances = None
        self.model_metrics = None
        
        self._load_or_create_models()

    def _load_or_create_models(self):
        base_path = os.path.dirname(__file__)
        rf_path = os.path.join(base_path, 'rf_model.pkl')
        lr_path = os.path.join(base_path, 'lr_model.pkl')
        scaler_path = os.path.join(base_path, 'scaler.pkl')
        metrics_path = os.path.join(base_path, 'model_metrics.pkl')

        if (os.path.exists(rf_path) and os.path.exists(lr_path) and 
            os.path.exists(scaler_path) and os.path.exists(metrics_path)):
            self.rf_model = joblib.load(rf_path)
            self.lr_model = joblib.load(lr_path)
            self.scaler = joblib.load(scaler_path)
            self.model_metrics = joblib.load(metrics_path)
            self.feature_names = [
                'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
                'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
                'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
                'compactness_se', 'concavity_se', 'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
                'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
                'compactness_worst', 'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
            ]
            if hasattr(self.rf_model, 'feature_importances_'):
                self.feature_importances = self.rf_model.feature_importances_
        else:
            self._create_and_save_models(rf_path, lr_path, scaler_path, metrics_path)

    def _create_and_save_models(self, rf_path, lr_path, scaler_path, metrics_path):
        from sklearn.datasets import load_breast_cancer
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

        data = load_breast_cancer()
        X, y = data.data, data.target
        self.feature_names = data.feature_names.tolist()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.rf_model.fit(X_train_scaled, y_train)
        
        self.lr_model = LogisticRegression(random_state=42, max_iter=1000)
        self.lr_model.fit(X_train_scaled, y_train)

        self.feature_importances = self.rf_model.feature_importances_

        rf_pred = self.rf_model.predict(X_test_scaled)
        rf_prob = self.rf_model.predict_proba(X_test_scaled)
        
        lr_pred = self.lr_model.predict(X_test_scaled)
        lr_prob = self.lr_model.predict_proba(X_test_scaled)

        self.model_metrics = {
            'Random Forest': {
                'accuracy': accuracy_score(y_test, rf_pred),
                'precision': precision_score(y_test, rf_pred),
                'recall': recall_score(y_test, rf_pred),
                'f1': f1_score(y_test, rf_pred),
                'roc_auc': roc_auc_score(y_test, rf_prob[:, 1]),
                'confusion_matrix': confusion_matrix(y_test, rf_pred).tolist()
            },
            'Logistic Regression': {
                'accuracy': accuracy_score(y_test, lr_pred),
                'precision': precision_score(y_test, lr_pred),
                'recall': recall_score(y_test, lr_pred),
                'f1': f1_score(y_test, lr_pred),
                'roc_auc': roc_auc_score(y_test, lr_prob[:, 1]),
                'confusion_matrix': confusion_matrix(y_test, lr_pred).tolist()
            }
        }

        joblib.dump(self.rf_model, rf_path)
        joblib.dump(self.lr_model, lr_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.model_metrics, metrics_path)

    def predict(self, features, model_type='Random Forest'):
        features_scaled = self.scaler.transform([features])
        
        if model_type == 'Logistic Regression':
            model = self.lr_model
        else:
            model = self.rf_model
        
        prediction = model.predict(features_scaled)
        probabilities = model.predict_proba(features_scaled)
        
        malignant_prob = probabilities[0][0]
        benign_prob = probabilities[0][1]
        confidence = float(np.max(probabilities))
        result = '恶性' if prediction[0] == 0 else '良性'
        
        return result, confidence, malignant_prob, benign_prob

    def get_feature_importance(self, top_n=5):
        if self.feature_importances is None:
            return []
        
        indices = np.argsort(self.feature_importances)[::-1]
        top_features = []
        
        for i in range(min(top_n, len(self.feature_names))):
            top_features.append({
                'name': self.feature_names[indices[i]],
                'importance': float(self.feature_importances[indices[i]])
            })
        
        return top_features

    def get_model_metrics(self):
        return self.model_metrics


breast_cancer_model = BreastCancerModel()