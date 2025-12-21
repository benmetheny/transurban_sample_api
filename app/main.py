from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from PIL import Image
import io

from app.rate_limiter import rate_limiter
from app.image_analyzer import is_image_grayscale

app = FastAPI(title="Transurban Sample API")

app.state.limiter = rate_limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(
        status_code=429,
        detail="Rate limit exceeded. Max 1 request every 2 seconds."
    )

@app.post("/analyze-image")
@rate_limiter.limit("1/2seconds")
async def analyze_image(request: Request, file: UploadFile = File(...)):
    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPG images are supported.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        width, height = image.size
        grayscale = is_image_grayscale(image)

        return {
            "is_grayscale": grayscale,
            "width": width,
            "height": height
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process image.")
