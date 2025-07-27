#!/bin/bash

API_URL="http://127.0.0.1:8000/api"

USERNAME="admin"
PASSWORD="Juniorboy58*"

echo "Logging in to get JWT tokens..."

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/token/" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USERNAME\", \"password\":\"$PASSWORD\"}")

# Separate body and status code
HTTP_BODY=$(echo "$LOGIN_RESPONSE" | head -n -1)
HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)

echo "HTTP Status: $HTTP_CODE"
echo "Response Body: $HTTP_BODY"

if [ "$HTTP_CODE" != "200" ]; then
  echo "Login failed."
  exit 1
fi

ACCESS_TOKEN=$(echo "$HTTP_BODY" | grep -oP '(?<="access":")[^"]+')

if [ -z "$ACCESS_TOKEN" ]; then
  echo "Failed to extract access token."
  exit 1
fi

echo "Access token acquired: ${ACCESS_TOKEN:0:30}..."

AUTH_HEADER="Authorization: Bearer $ACCESS_TOKEN"

echo "Getting current user info..."

USER_RESPONSE=$(curl -s -X GET "$API_URL/users/me/" -H "$AUTH_HEADER")

echo "User info response: $USER_RESPONSE"

USER_ID=$(echo "$USER_RESPONSE" | grep -oP '(?<="id":)[0-9]+')

if [ -z "$USER_ID" ]; then
  echo "Failed to get user ID."
  exit 1
fi

echo "Current user ID: $USER_ID"

echo "Creating a new conversation with yourself..."

CREATE_PAYLOAD="{\"participants\": [$USER_ID]}"

CREATE_RESPONSE=$(curl -s -X POST "$API_URL/conversations/" \
  -H "Content-Type: application/json" \
  -H "$AUTH_HEADER" \
  -d "$CREATE_PAYLOAD")

echo "Create conversation response:"
echo "$CREATE_RESPONSE"

echo "Fetching all conversations for current user..."

CONV_RESPONSE=$(curl -s -X GET "$API_URL/conversations/" -H "$AUTH_HEADER")

echo "$CONV_RESPONSE"

