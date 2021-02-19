#!/bin/bash
curl "http://localhost:8000/entries/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "entry": {
      "company": "'"${COMPANY}"'",
      "position": "'"${POS}"'",
      "link": "'"${LINK}"'",
      "date_applied": "'"${DA}"'",
      "status": "'"${STATUS}"'",
      "notes": "'"${NOTES}"'"
    }
  }'

echo
