import os
import joblib
import pandas as pd
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Initialize FastAPI app
app = FastAPI(title="Academic Performance Predictor")

# Setup folder paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Load ML Artifacts
MODEL_PATH = "./models/best_model.pkl"
SCALER_PATH = "./models/scaler.pkl"

def load_artifacts():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    return None, None

model, scaler = load_artifacts()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the main input form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    study_hours: float = Form(...),
    social_media: float = Form(...),
    netflix: float = Form(...),
    attendance: float = Form(...),
    sleep: float = Form(...),
    exercise: float = Form(...),
    mental_health: float = Form(...)
):
    if model is None or scaler is None:
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "error": "Model files not found!"
        })

    # Prepare data
    input_data = pd.DataFrame([{
        'study_hours_per_day': study_hours,
        'social_media_hours': social_media,
        'netflix_hours': netflix,
        'attendance_percentage': attendance,
        'sleep_hours': sleep,
        'exercise_frequency': exercise,
        'mental_health_rating': mental_health
    }])

    # Scale and Predict
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    final_score = round(max(0, min(100, prediction)), 2)

    # REMOVED: generate_student_advice call
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": final_score
        # coaching_advice is gone!
    })



# To run the app, use the command:
# uvicorn src.web.api:app --reload