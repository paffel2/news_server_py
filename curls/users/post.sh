curl -X 'POST' \
  'http://localhost:8000/api/users/' \
  -d '{
  "username": "login",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com"
}'