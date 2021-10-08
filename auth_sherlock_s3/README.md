## Deploying to Lambda

Inside the main folder, run:

```
$ zip -r lambda_function.zip index.js
```

and then upload the package into Lambda console. Or in terminal run:

```
$ aws --profile prod --region us-east-1 lambda update-function-code --function-name auth_enjuca_s3 --zip-file fileb://lambda_function.zip
```

and then deploy a new package to Lambda@Edge using the AWS Lambda console.
