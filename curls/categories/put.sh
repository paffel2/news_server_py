curl -X 'PUT' \
  'http://localhost:8000/api/categories/2/' \
  -H 'token: e51be516-d096-44f9-86fb-7c8e068ee52d' \
  -d '{
  "category_name": "paraolympic games",
  "parent_category": 1
}'