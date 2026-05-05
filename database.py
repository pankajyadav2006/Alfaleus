from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Use environment variable for database path, default to local directory
DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./opportunities.db")

engine = create_engine(
    DB_PATH, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    type = Column(String)  # Grant, Conference, Accelerator, Competition, Fellowship, Other
    organizer = Column(String)
    location = Column(String)
    deadline = Column(String)
    source_link = Column(String, unique=True, index=True)
    source_name = Column(String)
    description = Column(Text)
    funding_range = Column(String)
    startup_stage = Column(String)
    remote_or_onsite = Column(String)
    tags = Column(String)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    keyword_matched = Column(String)

# Create indices for full-text search simulation
Index('idx_title_desc', Opportunity.title, Opportunity.description)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
