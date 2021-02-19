#!/bin/bash

curl "http://localhost:8000/entries/${ID}/" \
  --include \
  --request GET \
  --header "Authorization: Token ${TOKEN}"

echo
