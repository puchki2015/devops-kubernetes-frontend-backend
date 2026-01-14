from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import qrcode
import os
from io import BytesIO
from pathlib import Path

# Loading Environment variable
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directory for storing QR codes locally
QR_CODE_DIR = "qr_codes"
os.makedirs(QR_CODE_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "QR Code Generator API is running good."}

@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Generate file name
    file_name = f"{url.split('//')[-1].replace('/', '_')}.png"
    file_path = os.path.join(QR_CODE_DIR, file_name)
    
    try:
        # Save to local file system
        img.save(file_path)
        
        # Return the local file path or URL
        local_url = f"http://localhost:8000/qr-image/{file_name}"
        return {"qr_code_url": local_url, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to serve the saved QR code images
@app.get("/qr-image/{file_name}")
async def get_qr_image(file_name: str):
    file_path = os.path.join(QR_CODE_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        raise HTTPException(status_code=404, detail="QR code not found")
