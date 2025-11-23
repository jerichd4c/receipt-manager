from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
import shutil
import os
from datetime import datetime

# import database and models

from database import SessionLocal, engine, Receipt, HistoryStatus, Base
from ocr_engine import pre_process_image, extract_text, analize_receipt
from notifications import send_notification

# init app and DB

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Smart Receipt Processor")

# DB depedendency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINT 1: uploader and processor (API REST)

@app.post("/api/upload")
async def upload_receipt(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    # 1. save uploaded file
    file_name = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. execute OCR
    try:
        img = pre_process_image(file_name)
        text= extract_text(img)
        data = analize_receipt(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")

    # 3. save to DB (status = pending)
    try:
        new_receipt = Receipt(
            provider=data["provider"],
            receipt_no=data["receipt_no"],
            date=data["date"],
            total_amount=float(data["total_amount"].replace('$','').replace(',','')) if data["total_amount"] else 0.0,
            file_path=file_name,
            raw_text=text,
            status="pending"
        )
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)

        # 4. register in history
        log = HistoryStatus(receipt_id=new_receipt.id, previous_status="N/A", new_status="In Process", comment="Uploaded via API")
        db.add(log)
        db.commit()

        # 5. send notificacion by email
        # here it sends the link pointing to THIS API endpoint
        # Note: in production, use environment variables for email addresses
        send_notification("recipient@example.com", data, new_receipt.id)

        return {"message": "Receipt uploaded successfully", "id": new_receipt.id, "extracted_data": data}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving files: {str(e)}")
    
# ENDPOINT 2: webhook approval
# webhook system
@app.get("/api/approve/{id_factura}", response_class=HTMLResponse)
async def approve_receipt(id_factura: int, db: Session = Depends(get_db)):
    receipt = db.query(Receipt).filter(Receipt.id == id_factura).first()
    if not receipt:
        return HTMLResponse(content="<h1>Error: Receipt not found</h1>", status_code=404)
    
    # update status
    previous_status = receipt.status
    receipt.status = "approved"

    # log history
    log = HistoryStatus(receipt_id=id_factura, previous_status=previous_status, new_status="approved", comment="Approved via Email")
    db.add(log)
    db.commit()

    # return confirmation HTML
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1 style="color: green;">¡Receipt approved successfully!</h1>
            <p>The system has recorded your decision.</p>
        </body>
    </html>
    """

# ENDPOINT 3: webhook rejection
# webhook system
@app.get("/reject_form/{id_factura}", response_class=HTMLResponse)
async def reject_form(id_factura: int):
    return f"""
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h2 style="color: #d9534f;">Reject Receipt #{id_factura}</h2>
            <form action="/api/reject/{id_factura}" method="post" style="max-width: 400px; margin: 0 auto;">
                <p>Please provide the reason for rejection:</p>
                    <textarea name="reason" rows="4" style="width: 100%; padding: 10px;" required></textarea><br><br>
                    <button type="submit" style="background-color: #d9534f; color: white; padding: 10px 20px; border: none; cursor: pointer;">Confirm Rejection</button>
            </form>
        </body>
    </html>
    """

# ENDPOINT 4: webhook rejection processing
@app.post("/api/reject/{id_factura}", response_class=HTMLResponse)
async def process_rejection(id_factura: int, reason: str = Form(...), db: Session = Depends(get_db)):
    factura = db.query(Receipt).filter(Receipt.id == id_factura).first()
    if not factura:
        return HTMLResponse(content="<h1>Error: Receipt not found</h1>", status_code=404)
    
    # update status
    previous_status = factura.status
    factura.status = "rejected"

    #log history
    log = HistoryStatus(receipt_id=id_factura, previous_status=previous_status, new_status="rejected", comment=reason)
    db.add(log)
    db.commit()

    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1 style="color: #d9534f;">Receipt Rejected</h1>
            <p>The reason for rejection has been recorded successfully.</p>
        </body>
    </html>
    """