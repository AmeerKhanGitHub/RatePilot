from sqlalchemy import create_engine, Column, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use DATABASE_URL from environment variables for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")  # Default to in-memory SQLite for testing
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ForwardCurve(Base):
    __tablename__ = 'forward_curve'
    reset_date = Column(String, primary_key=True)
    one_month_sofr = Column(Float)

# Create tables
Base.metadata.create_all(engine)
