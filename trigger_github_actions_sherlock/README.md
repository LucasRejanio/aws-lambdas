## Deploying to Lambda

Inside the main folder, run:

```
$ pip3 install requests -t ./ --upgrade
$ zip -r lambda_function.zip .
$ rm -rf -v !("lambda_function.py"|"README.md"|"lambda_function.zip")
```

and then upload the package into Lambda console. Or in terminal run:

```
$ aws --profile qa --region us-east-1 lambda update-function-code --function-name trigger_github_actions_sherlock --zip-file fileb://lambda_function.zip
```
