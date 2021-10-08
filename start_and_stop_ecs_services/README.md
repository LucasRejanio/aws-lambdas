## Deploying to Lambda

Inside the main folder, run:

```
$ zip -r function.zip lambda_function.py st*
```

and then upload the package into Lambda console. Or in terminal run:

```
$ aws lambda update-function-code --function-name start_stop_ecs_services --zip-file fileb://function.zip
```

#### Required payload to run function

```
{
  "service": "qa-02",
  "action": "start",
  "file": "start_venus"
}
```
