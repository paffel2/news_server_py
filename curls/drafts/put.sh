curl -X 'PUT' \
  'http://localhost:8000/api/drafts/' \
  -H 'token: e693e4ae-30c7-474e-bbc4-d7e08d2790e5' \
  -F 'id=3' \
  -F 'category=1' \
  -F 'tags=4' \
  -F 'text=new text' \
  -F 'title=new title'