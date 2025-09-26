#!/bin/bash

# Script to generate avatar upload URL for a user

USER_ID=68cdf1d70740197a824e74bd  # Change this to the desired user ID

curl -X POST \
  http://127.0.0.1:3000/users/$USER_ID/avatar