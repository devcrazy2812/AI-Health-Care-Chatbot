import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def main():
    data_path = os.path.join('..', 'data', 'heart-disease.csv')
    print(f"Loading data from {data_path}...")
    
    # Load dataset
    df = pd.read_csv(data_path)
    
    # Simple EDA
    print(f"Dataset shape: {df.shape}")
    
    # Features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize & train the model
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # Predictions and evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    output_dir = os.path.join('..', 'backend', 'ml_models')
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'rf_heart_disease.joblib')
    
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully at {model_path}")

if __name__ == '__main__':
    main()
