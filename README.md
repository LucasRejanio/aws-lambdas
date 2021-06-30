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

```sh
- apt update && apt install zip -y && apt install curl -y && apt install jq -y
- curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
- aws configure set aws_access_key_id ${AWS_STAGING_ACCESS_KEY_ID} --profile qa
- aws configure set aws_secret_access_key ${AWS_STAGING_SECRET_ACCESS_KEY_ID} --profile qa
- aws --profile qa --region us-east-1 lambda update-function-code --function-name qa_01_user_store_builder_from_source --zip-file fileb://user_store_builder_from_source/v1/function.zip
- aws --profile qa --region us-east-1 lambda publish-version --function-name qa_01_user_store_builder_from_source > version.json
- export VERSION_NUMBER=$(cat version.json | jq .Version | sed -e 's/\"//g')
- aws --profile qa --region us-east-1 lambda update-alias --function-name qa_01_user_store_builder_from_source --name v1 --function-version $VERSION_NUMBER
```
