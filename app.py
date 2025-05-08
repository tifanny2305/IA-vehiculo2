from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from ultralytics import YOLO
import shutil, os, glob

# 🚀 Crear la app
app = FastAPI()

# Habilitar CORS para todos (puedes restringir si quieres)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API de detección de daños en vehículos. Usa POST /predecir/"}

# ✅ Cargar el modelo al iniciar
model_path = "best.pt"  # Asegúrate de tener este archivo en la misma carpeta
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ El modelo no se encontró en: {model_path}")

model = YOLO(model_path)
print(f"✅ Modelo cargado desde: {model_path}")

def clasificar_deteccion(result):
    cls_idxs = result.boxes.cls.cpu().numpy().astype(int)
    class_names = [result.names[i] for i in cls_idxs]
    if "severe" in class_names:
        return "grave"
    if "moderate" in class_names:
        return "moderado"
    if "accident" in class_names:
        return "leve"
    return "sin daño"

# http://127.0.0.1:8000/predecir/
@app.post("/predecir/")
async def predecir_multiple(files: List[UploadFile] = File(...)):
    resultados = []
    for f in files:
        tmp = f"tmp_{f.filename}"
        with open(tmp, "wb") as buf:
            shutil.copyfileobj(f.file, buf)

        # Hacer la predicción
        res = model.predict(source=tmp, conf=0.3)[0]
        nivel = clasificar_deteccion(res)
        cajas = len(res.boxes)

        os.remove(tmp)
        resultados.append({
            "archivo": f.filename,
            "nivel": nivel,
            "detecciones": cajas
        })
    return {"resultados": resultados}
