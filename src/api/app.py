import pandas as pd
import joblib
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Definir la estructura de los datos de entrada (Data Contract)
class Transaction(BaseModel):
    type: str  # TRANSFER o CASH_OUT
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float
    step: int

# 2. Inicializar la App
app = FastAPI(title="Fraud Detection System API", version="1.0")

# --- SOLUCIÓN DE RUTAS (ROBUSTO) ---
# Encontrar dónde está este archivo app.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta exacta al modelo (independiente de la terminal)
# Subimos dos niveles (../../) para llegar a la raíz y entrar a models
model_path = os.path.join(current_dir, "../../models/xgb_fraud_detector.joblib")
columns_path = os.path.join(current_dir, "../../models/model_columns.joblib")

print(f"📂 Buscando modelo en: {model_path}")

try:
    model = joblib.load(model_path)
    model_columns = joblib.load(columns_path)
    print("✅ Modelo cargado exitosamente.")
except Exception as e:
    print(f"❌ Error fatal cargando el modelo: {e}")
    # No detenemos la app, pero avisamos del error
    model = None

# 3. Endpoint de Predicción
@app.post("/predict")
def predict_fraud(tx: Transaction):
    if model is None:
        raise HTTPException(status_code=500, detail="Model could not be loaded")

    # A. Validar tipo de transacción
    if tx.type not in ['TRANSFER', 'CASH_OUT']:
        return {"risk_score": 0.0, "is_fraud": False, "reason": "Transaction type ignored"}

    # B. Feature Engineering "On-the-fly"
    input_data = {
        'amount': tx.amount,
        'old_balance_orig': tx.oldbalanceOrg,
        'new_balance_orig': tx.newbalanceOrig,
        'old_balance_dest': tx.oldbalanceDest,
        'new_balance_dest': tx.newbalanceDest,
        'hour_of_day': tx.step % 24,
        'type': 0 if tx.type == 'TRANSFER' else 1,
        'error_balance_orig': tx.newbalanceOrig + tx.amount - tx.oldbalanceOrg,
        'error_balance_dest': tx.oldbalanceDest + tx.amount - tx.newbalanceDest
    }
    
    # Crear DataFrame y asegurar el orden de columnas
    df = pd.DataFrame([input_data])
    # Aseguramos que las columnas estén en el mismo orden que el entrenamiento
    try:
        df = df[model_columns] 
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing columns: {e}")

    # C. Predicción
    probability = model.predict_proba(df)[0][1] # Probabilidad de clase 1
    is_fraud = probability > 0.5

    return {
        "risk_score": float(probability),
        "is_fraud": bool(is_fraud),
        "alert": "⚠️ HIGH RISK" if is_fraud else "✅ OK"
    }

# 4. Endpoint de Salud
@app.get("/health")
def health_check():
    return {"status": "active", "model_loaded": model is not None}
