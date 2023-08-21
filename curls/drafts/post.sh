curl -X 'POST' \
  'http://localhost:8000/api/drafts/' \
  -H 'token: e693e4ae-30c7-474e-bbc4-d7e08d2790e5' \
  -F 'category=2' \
  -F 'tags=4' \
  -F 'text=somethin text in news' \
  -F 'title=sport title'