import joblib
import pandas as pd

# ------------------------------------------
# Prediction Function
# ------------------------------------------
def make_prediction():
    try:
        # Load the artifacts
        model = joblib.load('models/best_model.pkl')
        scaler = joblib.load('models/scaler.pkl')

        print("\n" + "="*30)
        print("STUDENT SCORE PREDICTOR")
        print("="*30)
        
        """
        Get user input (Make sure order matches your 7 selected features!)
        The order must be exactly: study_hours, social_media, netflix, 
        attendance, sleep, exercise, mental_health
        """

        #Define inputs in a dictionary
        inputs = {
            'study_hours_per_day': float(input("Study Hours/Day(0-16): ")),
            'social_media_hours': float(input("Social Media Hours(0-12): ")),
            'netflix_hours': float(input("Netflix Hours(0-12): ")),
            'attendance_percentage': float(input("Attendance %(1-100): ")),
            'sleep_hours': float(input("Sleep Hours(1-12): ")),
            'exercise_frequency': float(input("Exercise (1-5): ")),
            'mental_health_rating': float(input("Mental Health (1-10): "))
        }
        # Convert to DataFrame
        input_df = pd.DataFrame([inputs])
        # Ensure correct column order
        expected_columns = [
            'study_hours_per_day', 'social_media_hours', 'netflix_hours', 
            'attendance_percentage', 'sleep_hours', 'exercise_frequency', 
            'mental_health_rating'
        ]
        input_df = input_df[expected_columns]
        # Scale the data (Crucial!)
        user_data_scaled = scaler.transform(input_df)
        # Predict
        prediction = model.predict(user_data_scaled)[0]
        # Clip the result between 0 and 100
        prediction = max(0, min(100, prediction))

        # Display the result
        print("\n" + "-"*30)
        print(f"RESULT: Estimated Exam Score: {prediction:.2f}%")
        if prediction >= 50:
            print("Status: PASS! Congratulations on your predicted success!")
        else:
            print("your selected values indicate you might need to work harder to pass. Keep pushing!")
        print("-"*30)

    except FileNotFoundError:
        print("Error: Model or Scaler not found. Run training first!")
    except Exception as e:
        print(f"Error: {e}")

# ------------------------------------------
# Run Prediction
# ------------------------------------------
if __name__ == "__main__":
    make_prediction()


# Run: python -m src.step.f_predict