## Deploying to Lambda

Inside the main folder, run:

```
$ pip3 install requests -t ./ --upgrade
$ pip3 install pytz -t ./ --upgrade
$ zip -r lambda_function.zip .
$ rm -rf -v !("lambda_function.py"|"README.md"|"lambda_function.zip")
```

and then upload the package into Lambda console. Or in terminal run:

```
$ aws --profile qa --region us-east-1 lambda update-function-code --function-name notification_pipeline_service_staging --zip-file fileb://lambda_function.zip
```

#### Required payload to run function

```
{
  "service": "qa-02",
  "action": "start",
  "file": "start_venus"
}
```
