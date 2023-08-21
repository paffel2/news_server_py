curl -X 'POST' \
  'http://localhost:8000/api/authors/' \
  -H 'token: e51be516-d096-44f9-86fb-7c8e068ee52d' \
  -d '{
  "id": 3,
  "bio": "description"
}'