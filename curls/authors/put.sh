curl -X 'PUT' \
  'http://localhost:8000/api/authors/2/' \
  -H 'token: e51be516-d096-44f9-86fb-7c8e068ee52d' \
  -d '{
  "bio": "finance journalis"
}'