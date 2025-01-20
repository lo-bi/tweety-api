import os
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from tweety import TwitterAsync
from tweety.filters import SearchFilters

app = FastAPI()

# Function to check the API key
def verify_api_key(x_api_key: str = Header(...)):
    expected_api_key = os.getenv("API_KEY")
    if x_api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Define the request body model
class SearchQuery(BaseModel):
    query: str

@app.get("/")
async def root(api_key: str = Depends(verify_api_key)):
    return {"message": "OK"}

@app.post("/searchRecentPosts")
async def search_recent_posts(search: SearchQuery, api_key: str = Depends(verify_api_key)):
    username = os.getenv("TWITTER_USERNAME")
    password = os.getenv("TWITTER_PASSWORD")

    if not username or not password:
        raise HTTPException(status_code=500, detail="Twitter username or password not set in environment variables")

    # Initialize Twitter client and sign in
    twitter_client = TwitterAsync("session")
    await twitter_client.sign_in(username, password)

    # Ensure the user is authenticated
    user_info = twitter_client.me
    if not user_info:
        raise HTTPException(status_code=403, detail="Twitter authentication failed")

    # Search for tweets based on the query
    tweets = await twitter_client.search(search.query, filter_=SearchFilters.Latest())

    # Format the tweets for the response
    tweet_data = [{"tweet": tweet} for tweet in tweets]

    return {"tweets": tweet_data}
