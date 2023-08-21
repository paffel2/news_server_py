curl -X 'POST' \
  'http://localhost:8000/api/categories/' \
  -H 'token: e51be516-d096-44f9-86fb-7c8e068ee52d' \
  -d '{
  "category_name": "olympic games",
  "parent_category": 1
}'