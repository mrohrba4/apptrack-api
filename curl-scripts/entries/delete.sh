#!/bin/bash

curl "http://localhost:8000/entries/${ID}/" \
  --include \
  --request DELETE \
  --header "Authorization: Token ${TOKEN}"

echo
