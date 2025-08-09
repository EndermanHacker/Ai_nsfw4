from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from fastapi import HTTPException

app = FastAPI()

# إعداد مجلد القوالب
templates = Jinja2Templates(directory="templates")

class ImageResponse(BaseModel):
    image_url: str
    nsfw_detected: bool

def fake_image_generator(prompt: str) -> str:
    return f"https://fakeimages.com/generated/{prompt.replace(' ', '_')}.png"

def fake_nsfw_detector(image_url: str) -> bool:
    return "nsfw" in image_url.lower()

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, "result": None, "error": None})

@app.post("/", response_class=HTMLResponse)
def generate_image(request: Request, prompt: str = Form(...), nsfw_filter: Optional[bool] = Form(True)):
    image_url = fake_image_generator(prompt)
    nsfw_detected = fake_nsfw_detector(image_url)

    if nsfw_detected and nsfw_filter:
        error = "تم اكتشاف محتوى NSFW. التوليد مرفوض بسبب تفعيل الفلتر."
        return templates.TemplateResponse("form.html", {"request": request, "result": None, "error": error})

    result = image_url
    return templates.TemplateResponse("form.html", {"request": request, "result": result, "error": None})

