from fastapi import FastAPI, Depends, HTTPException
import strawberry
from strawberry.fastapi import GraphQLRouter
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database Setup
DATABASE_URL = "sqlite:///./sentiment.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Sentiment Analysis Table
class SentimentAnalysis(Base):
    __tablename__ = "sentiment_results"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    prediction = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Authentication function
def verify_api_key(api_key: str):
    if api_key != os.getenv("API_KEY", "mysecretkey"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True

# Define GraphQL Schema with Strawberry
@strawberry.type
class Query:
    @strawberry.field
    def sentiment(self, text: str, api_key: str) -> str:
        verify_api_key(api_key)  # Check API key
        result = sentiment_analyzer(text)[0]
        prediction = result['label']

        # Save to database
        db: Session = next(get_db())
        db_entry = SentimentAnalysis(text=text, prediction=prediction)
        db.add(db_entry)
        db.commit()

        return prediction

schema = strawberry.Schema(query=Query)

# FastAPI app setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GraphQL Route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API - Use /graphql endpoint"}

# New Endpoint: Fetch stored results
@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    results = db.query(SentimentAnalysis).all()
    return results
