import os
import pandas as pd
import numpy as np
import joblib

from error_logs import configure_logger
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

logger = configure_logger()


def model_training(df: pd.DataFrame):
    """
    Trains multiple regression models and evaluates their performance.
    Returns the best model based on R² score.
    """
    try:
        logger.info("==> Starting Model Training...")

        # Split features and target
        X = df.drop(columns=['exam_score'])
        y = df['exam_score']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Feature Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Models to train
        models = {
            'Linear': LinearRegression(),
            'Ridge': Ridge(),
            'Lasso': Lasso(),
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
            'XGBoost': XGBRegressor(objective='reg:squarederror', n_estimators=100, random_state=42)
        }

        # Training and evaluation
        results = {}
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)

            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            results[name] = {
                'model': model,
                'r2': r2,
                'mae': mae,
                'rmse': rmse
            }

        # Select the best model based on R² score
        best_model_name = max(results, key=lambda x: results[x]['r2'])
        best_model_info = results[best_model_name]

        # Log the results
        summary = (
            f"\n{'='*30}\n"
            f"MODEL TRAINING REPORT\n"
            f"{'='*30}\n"
            f"Best Model:       {best_model_name}\n"
            f"R² Score:         {best_model_info['r2']:.4f}\n"
            f"Mean Absolute Error: {best_model_info['mae']:.4f}\n"
            f"Root Mean Squared Error: {best_model_info['rmse']:.4f}\n"
            f"{'='*30}"
        )
        logger.info(summary)
        logger.info("==> Model Training completed successfully.\n\n")

        # Save the best model and scaler
        model_path = os.path.join('models', 'best_model.pkl')
        scaler_path = os.path.join('models', 'scaler.pkl')
        os.makedirs('models', exist_ok=True)
        joblib.dump(best_model_info['model'], model_path)
        joblib.dump(scaler, scaler_path)
        logger.info(f"Best model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")

        # Return the best model and scaler
        return best_model_info['model'], scaler, best_model_info
    

    except Exception as e:
        logger.error(f"Error during model training: {e}")
        return None, None