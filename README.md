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

- Deploy with version

```sh
- apt update && apt install zip -y && apt install curl -y && apt install jq -y
- curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install
- aws configure set aws_access_key_id ${AWS_STAGING_ACCESS_KEY_ID} --profile qa
- aws configure set aws_secret_access_key ${AWS_STAGING_SECRET_ACCESS_KEY_ID} --profile qa
- aws --profile qa --region us-east-1 lambda update-function-code --function-name $LAMBDA_NAME --zip-file fileb://function.zip
- aws --profile qa --region us-east-1 lambda publish-version --function-name $LAMBDA_NAME > version.json
- export VERSION_NUMBER=$(cat version.json | jq .Version | sed -e 's/\"//g')
- aws --profile qa --region us-east-1 lambda update-alias --function-name $LAMBDA_NAME --name v1 --function-version $VERSION_NUMBER
```

<!-- import os
import json
import jinja2

class FileLoader:
    @staticmethod
    def file_dir_compose(file_dir):
        staging_environments = ["qa", "next"]
        if os.environ['PULUMI_STACK'] == "qa-devs":
            folder = os.environ['PULUMI_STACK']
        elif any(env in str(os.environ['PULUMI_STACK']) for env in staging_environments):
            folder = "qa"
        else:
            folder = os.environ['PULUMI_STACK']

        return f"{file_dir}{folder}/"

    @staticmethod
    def start_from_json(file_dir, name, separator_enabled):
        with open(f"{FileLoader.file_dir_compose(file_dir) + name}.json", 'r') as file:
            if separator_enabled:
                data = json.loads(file.read())
                return json.dumps(data, separators=(",", ":"))

            data = file.read()
            return json.loads(data)

    @staticmethod
    def start_from_template(file_dir, envs, template_file, separator_enabled, file_type):
        file_path = f"{FileLoader.file_dir_compose(file_dir)}templates/"
        if file_type == "JSON":
            creater = jinja2.Environment(loader=jinja2.FileSystemLoader(file_path)).get_template(f"{template_file}.json")
            file = creater.render(environs=envs)
            if separator_enabled:
                data = json.loads(file)
                return json.dumps(data, separators=(",", ":"))

            return json.loads(file)
        if file_type == "YML":
            creater = jinja2.Environment(loader=jinja2.FileSystemLoader(file_path)).get_template(f"{template_file}.yml")
            file = creater.render(environs=envs)
            return file

        raise Exception("Sorry, only support JSON or YML") -->
