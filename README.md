# Creating the AWS Lambda Role
`AWS_PROFILE=kmonkeyjam aws cloudformation create-stack --stack-name my-lambda-role --template-body file://lambda-role-template.yaml --capabilities CAPABILITY_NAMED_IAM`

`AWS_PROFILE=kmonkeyjam aws cloudformation update-stack --stack-name my-lambda-role --template-body file://lambda-role-template.yaml --capabilities CAPABILITY_NAMED_IAM`

# Deploying the Lambda
`poetry shell`
`AWS_PROFILE=kmonkeyjam chalice deploy`

# Setting the OpenAI API Key
`export OPENAI_API_KEY=xxx`


# Other notes
## Shortcut to create a new lambda project
`chalice new-project mylambdaapp`