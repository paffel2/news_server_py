curl -X 'POST' \
  'http://localhost:8000/api/news/1/commentaries/' \
  -H 'token: e693e4ae-30c7-474e-bbc4-d7e08d2790e5' \
  -d '{
  "text": "new comment"
}'