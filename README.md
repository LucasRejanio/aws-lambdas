<img alt="AWS" src="https://img.shields.io/badge/AWS%20-%23FF9900.svg?&style=for-the-badge&logo=amazon-aws&logoColor=white"/> <img alt="Python" src="https://img.shields.io/badge/python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white"/>

# aws-lambdas
Esse repositorio tem como objetivo guardar algumas soluções utilizando Lambda dentro da aws.

- https://aws.amazon.com/pt/lambda/


### Exemple Deploying to Lambda

Inside the main folder, run:

- Install dependencies and zip the code:

```sh
$ pip3 install requests -t ./ --upgrade
$ pip3 install pytz -t ./ --upgrade
$ zip -r lambda_function.zip .
$ rm -rf -v !("lambda_function.py"|"README.md"|"lambda_function.zip")
```

- then upload the package into Lambda console. Or in terminal run:

```sh
$ aws --profile prod --region us-east-1 lambda update-function-code --function-name NOME_LAMBDA --zip-file fileb://lambda_function.zip
```
