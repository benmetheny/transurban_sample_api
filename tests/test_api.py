from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io

client = TestClient(app)

def create_image(color=True):
    img = Image.new("RGB", (100, 50), color="red" if color else "gray")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf

def test_color_image():
    response = client.post(
        "/analyze-image",
        files={"file": ("test.jpg", create_image(color=True), "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()["is_grayscale"] is False

def test_grayscale_image():
    response = client.post(
        "/analyze-image",
        files={"file": ("test.jpg", create_image(color=False), "image/jpeg")}
    )
    assert response.status_code == 200
    assert response.json()["is_grayscale"] is True

def test_invalid_file_type():
    response = client.post(
        "/analyze-image",
        files={"file": ("plain-text.txt", b"plain-text", "text/plain")}
    )
    assert response.status_code == 400
