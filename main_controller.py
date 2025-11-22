from ocr_engine import pre_process_image, extract_text, analize_receipt
from database import SessionLocal, Receipt, HistoryStatus, create_tables

def preprocess_new_receipt(file_path):
    """Pre-process a new receipt image and extract structured data."""
    # Step 1: Pre-process the image with IA
    print(f"Pre-processing image: {file_path}...")
    img = pre_process_image(file_path)
    ocr_text = extract_text(img)
    data = analize_receipt(ocr_text)

    # Step 2: Store in DB
    db = SessionLocal()
    try: 

        # create new object with extracted data
        new_receipt = Receipt(
            provider=data["provider"],
            invoice_number=data["invoice_number"],
            issue_date=data["issue_date"],
            # convert to float, removing $ and commas
            total_amount=float(data["total_amount"].replace('$','').replace(',','')) if data["total_amount"] else 0.0,
            file_path=file_path,
            raw_text_ocr=ocr_text,
            status="In Progress" # initial status
        )

        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)

        # log initial status in history
        log_entry = HistoryStatus(
            receipt_id=new_receipt.id,
            previous_status="N/A",
            new_status="In Progress",
            commentary="Receipt created and processing started."
        )
        db.add(log_entry)
        db.commit()

        print(f"✅ Receipt saved with ID: {new_receipt.id} | Status: {new_receipt.status}")
        return new_receipt.id
    
    except Exception as e:
        print(f"❌ Error saving receipt: {e}")
        db.rollback()
    finally:
        db.close()

# test block

if __name__ == "__main__":
    # make sure DB tables exist
    create_tables()

    # test with a sample image
    preprocess_new_receipt("sample_invoice.jpg")
