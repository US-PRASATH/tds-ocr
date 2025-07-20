from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # OCR to extract text
        text = pytesseract.image_to_string(image)
        print("Extracted:", text)

        # Find and evaluate multiplication expression
        import re
        match = re.search(r"(\d+)\s*\*\s*(\d+)", text.replace("x", "*"))
        if not match:
            return JSONResponse(status_code=400, content={"error": "Multiplication not found"})

        num1, num2 = int(match.group(1)), int(match.group(2))
        result = num1 * num2

        return {"answer": result, "email": "23f1002057@ds.study.iitm.ac.in"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
