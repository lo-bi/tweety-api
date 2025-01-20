# tweety-api
API for tweety https://github.com/mahrtayyab/tweety
It only support the search of recent tweets based on a query

Don't forget to change the env var `API_KEY`, `TWITTER_USERNAME` and `TWITTER_PASSWORD` when running the container

```
git clone https://github.com/lo-bi/tweety-api.git
cd tweety-api
docker build -t tweety-api:latest .
docker run -d -p 8000:8000 -e API_KEY=mysecureapikey -e TWITTER_USERNAME=username -e TWITTER_PASSWORD=password tweety-api:latest
```

Then run the following command to do a query in X recent posts
```
curl -X POST "http://127.0.0.1:8000/searchRecentPosts" \
-H "Content-Type: application/json" \
-H "x-api-key: APIKEY" \
-d '{"query": "cats"}'
```