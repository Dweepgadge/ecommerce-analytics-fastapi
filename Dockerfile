# 1. Base Image: Ek halka-phulka Python Linux environment
FROM python:3.11-slim

# 2. Container ke andar working directory set karo
WORKDIR /app

# 3. Pehle requirements.txt copy karo (Docker Caching ke liye)
COPY requirements.txt .

# 4. Saare packages install karo
RUN pip install --no-cache-dir -r requirements.txt

# 5. Apna saara project code container me copy karo
COPY . .

# 6. Container ka port 8000 open karo
EXPOSE 8000

# 7. Server start karne ki command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
