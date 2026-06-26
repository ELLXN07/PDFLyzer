from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
from io import BytesIO
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"]
)

client = Groq(
api_key=os.getenv("GROQ_API_KEY")
)

app.mount(
"/static",
StaticFiles(directory="static"),
name="static"
)

@app.get("/")
async def home():
    return FileResponse(
    "static/index.html"
    )

@app.post("/analyze-pdf")
async def analyze_pdf(
file: UploadFile = File(...)
):


    contents = await file.read()

    pdf = PdfReader(
        BytesIO(contents)
    )

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    print("TEXT LENGTH:", len(text))

    if not text.strip():

        return {
            "analysis":
            "No text found in PDF."
        }

    text = text[:3000]

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",

                "content":
                """
                Analyze this PDF.

                Give:
                1. Short Summary
                2. Important Points
                3. Main Concepts
                """
            },

            {
                "role": "user",
                "content": text
            }
        ]
    )

    return {

        "analysis":

        response
        .choices[0]
        .message
        .content
    }