
import pickle
import xgboost as xgb
import os

model_path = 'xgboost_model.pkl'

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f"Model loaded successfully: {type(model)}")
    
    if hasattr(model, 'feature_names_in_'):
        print("Feature names:", model.feature_names_in_)
    elif hasattr(model, 'get_booster'):
        print("Feature names from booster:", model.get_booster().feature_names)
    else:
        print("Could not find feature names directly.")
        
except Exception as e:
    print(f"Error loading model: {e}")
