from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# database setup
DATABASE_URL = "sqlite:///./receipts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# receipt model
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    
    # extracted fields from OCR 
    provider = Column(String, nullable=True)       # [cite: 16]
    invoice_number = Column(String, nullable=True)  # [cite: 17]
    issue_date = Column(String, nullable=True)   # [cite: 18]
    total_amount = Column(Float, nullable=True)      # [cite: 19]
    taxes = Column(Float, nullable=True)        # [cite: 20]

    # system metadata

    file_path = Column(String)  # path to the stored image/pdf

    raw_text_ocr = Column(Text) # backup of raw OCR text

    # status management

    status = Column(String, default="In Progress")  # e.g., new, processed, error

    created_at = Column(DateTime, default=datetime.now) # initial creation timestamp

    # history

    history = relationship("HistoryStatus", back_populates="receipt")

# history model
class HistoryStatus(Base):
    __tablename__ = "history_status"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    previous_status = Column(String)
    new_status = Column(String)
    commentary = Column(Text, nullable=True) # if rejected
    timestamp = Column(DateTime, default=datetime.now)
    receipt = relationship("Receipt", back_populates="history")

# init DB

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Tables created successfully in receipts.db.")