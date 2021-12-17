## About Lambda
This lambda does an export in a cvs file of the comments from the last 7 days.

### Routine
- Every Monday at 08h am.

## Deploying to Lambda

Inside the main folder, run:

```
pip3 install requests -t ./ --upgrade \
&& pip3 install psycopg2-binary -t ./ --upgrade \
&& pip3 install pandas -t ./ --upgrade \
&& pip3 install pytz -t ./ --upgrade \
&& zip -r lambda_function.zip . \
&& rm -rf -v !("lambda_function.py"|"README.md"|"lambda_function.zip")
```

and then upload the package into Lambda console. Or in terminal run:

```
$ aws --region us-east-1 lambda update-function-code --function-name export_ghost_comments --zip-file fileb://lambda_function.zip
```
