from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import json
import tempfile

from streamlit_financial_report_v7_7 import (
    generate_full_html,
    convert_html_to_pdf,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Financial Statement Analyzer API Running"
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        # Read uploaded JSON file
        content = await file.read()

        # Convert JSON text into Python object
        data = json.loads(content.decode("utf-8"))

        # Generate HTML report
        html_content = generate_full_html(data)

        # Generate PDF report
        pdf_bytes = convert_html_to_pdf(html_content)

        # Save temporary PDF
        temp_pdf = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        temp_pdf.write(pdf_bytes)
        temp_pdf.close()

        return JSONResponse({
            "success": True,
            "html": html_content,
            "pdf_path": temp_pdf.name,
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
            },
        )