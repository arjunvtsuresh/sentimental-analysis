from fastapi import FastAPI, Depends, HTTPException
from graphene import ObjectType, String, Schema
from starlette_graphene3 import GraphQLApp
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import os

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

# Authentication function
def verify_api_key(api_key: str):
    if api_key != os.getenv("API_KEY", "mysecretkey"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True

# GraphQL Schema
class Query(ObjectType):
    sentiment = String(text=String(required=True), api_key=String(required=True))

    def resolve_sentiment(self, info, text, api_key):
        verify_api_key(api_key)  # Check API key
        result = sentiment_analyzer(text)[0]
        return result['label']

schema = Schema(query=Query)

# FastAPI app setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


app.add_route("/graphql", GraphQLApp(schema=schema))

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API - Use /graphql endpoint"}
