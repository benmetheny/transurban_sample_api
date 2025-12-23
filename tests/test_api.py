import time
from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

wait_time = 2.1

def create_image(color=True):
    img = Image.new("RGB", (100, 50), color="red" if color else "gray")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_color_image():
    response = post_with_retry(
        "/analyze-image",
        {"file": ("test.jpg", create_image(color=True), "image/jpeg")}
    )

    assert response.status_code == 200
    assert response.json()["is_grayscale"] is False

def test_grayscale_image():
    response = post_with_retry(
        "/analyze-image",
        {"file": ("test.jpg", create_image(color=False), "image/jpeg")}
    )

    assert response.status_code == 200
    assert response.json()["is_grayscale"] is True

def test_invalid_file_type():
    response = post_with_retry(
        "/analyze-image",
        {"file": ("plain-text.txt", b"plain-text", "text/plain")}
    )

    assert response.status_code == 400

def test_rate_limit():
    status_code = 0
    for _ in range(5):
        response = client.post(
            "/analyze-image",
            files={"file": ("plain-text.txt", b"plain-text", "text/plain")}
        )
        if response.status_code == 429:
            status_code = response.status_code
            break
    
    assert status_code == 429

def post_with_retry(path, body):
    response = client.post(path, files=body)
    if(response.status_code == 429):
        time.sleep(wait_time)
        response = client.post(path, files=body)
    return response

