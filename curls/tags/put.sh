curl -X 'PUT' \
  'http://localhost:8000/api/tags/' \
  -H 'token: 60a6d12e-24de-4738-8930-ecd4a67bfad9' \
  -d '{
  "id": 7,
  "tag_name": "new name for tag"
}'