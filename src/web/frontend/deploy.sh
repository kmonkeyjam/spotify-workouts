#!/bin/bash
# Build the React app
npm run build

# Deploy to S3
AWS_PROFILE=kmonkeyjam aws s3 sync build/ s3://spotify-workouts-web --delete

