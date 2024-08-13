# Creating the AWS Lambda Role
`AWS_PROFILE=kmonkeyjam aws cloudformation create-stack --stack-name my-lambda-role --template-body file://lambda-role-template.yaml --capabilities CAPABILITY_NAMED_IAM`

`AWS_PROFILE=kmonkeyjam aws cloudformation update-stack --stack-name my-lambda-role --template-body file://lambda-role-template.yaml --capabilities CAPABILITY_NAMED_IAM`

# Creating cloudfront to proxy to API gateway
AWS_PROFILE=kmonkeyjam aws cloudformation create-stack --stack-name cloudfront-spotify --template-body file://cloudfront-template.yaml --capabilities CAPABILITY_NAMED_IAM

# Deploying the Lambda
`poetry shell`
`poetry export -f requirements.txt --output requirements.txt`
`AWS_PROFILE=kmonkeyjam chalice deploy`

# Other notes
## Setting the OpenAI API Key locally
`export OPENAI_API_KEY=xxx`

## Shortcut to create a new lambda project
`chalice new-project mylambdaapp`

https://d27hv4mf8axlyg.cloudfront.net/

