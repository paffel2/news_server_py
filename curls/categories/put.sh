curl -X 'PUT' \
  'http://localhost:8000/api/categories/' \
  -H 'token: e51be516-d096-44f9-86fb-7c8e068ee52d' \
  -d '{
  "id": 4,
  "category_name": "paraolympic games",
  "parent_category": 1
}'