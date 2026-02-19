import xgboost as xgb
import optuna
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

def objective(trial, X, y):
    """
    Função objetivo para a Otimização Bayesiana (Optuna).
    """
    params = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'booster': 'gbtree',
        'random_state': 42,
        
        # Espaço de busca (Hiperparâmetros avançados)
        'scale_pos_weight': trial.suggest_float('scale_pos_weight', 10.0, 150.0),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'lambda': trial.suggest_float('lambda', 1e-3, 10.0, log=True),
        'alpha': trial.suggest_float('alpha', 1e-3, 10.0, log=True)
    }

    # Validação Cruzada Estratificada interna
    kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    auc_scores = []
    
    for train_idx, val_idx in kf.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        # early_stopping impede o modelo de treinar mais do que o necessário
        model = xgb.XGBClassifier(**params, n_estimators=500, early_stopping_rounds=30)
        model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
        
        preds = model.predict_proba(X_val)[:, 1]
        auc_scores.append(roc_auc_score(y_val, preds))
    
    return np.mean(auc_scores)

def train_final_model(X, y, n_trials=15):
    print("🚀 A iniciar Otimização Bayesiana com Optuna...")
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X, y), n_trials=n_trials)
    
    print(f"✅ Melhores parâmetros encontrados: {study.best_params}")
    
    # Treina o modelo com a melhor configuração encontrada
    best_params = study.best_params
    best_params['random_state'] = 42
    final_model = xgb.XGBClassifier(**best_params, n_estimators=500)
    final_model.fit(X, y)
    
    return final_model