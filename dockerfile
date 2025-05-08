# Usa la imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# 👉 INSTALA las dependencias del sistema necesarias (para OpenCV y más)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos necesarios
COPY requirements.txt .
COPY app.py .
COPY best.pt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para arrancar la API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
