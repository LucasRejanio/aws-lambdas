## Notifications CodePipeline

Esse Lambda é bem simples. Basicamente é uma implementação do CodeStarNotifications direto no CodePipeline. A arquitetura funciona da seguinte maneira: 

- O **CodeStarNotifications** fica monitorando o **CodePipeline** e pegando os eventos de exeção do mesmo.

- Logo depois ele envia esses eventos para um tópico **SNS**.

- O SNS por sua vez, é responsável por triggar o lambda por meio de uma **subscription**.

- E por fim o **Lambda** irá receber essa mensagem. Realizar uma tratativa. Pegar os valores de Webhook de um **ParameterStore**. Validar se existem um prefixo no nome da Pipeline. E mediante esse prefixo encaminhar a mensagem para o **canal slack** desejado.

#### Arquitetura
![Notifications Deploy](https://user-images.githubusercontent.com/52427398/119200560-8ae93500-ba63-11eb-9dfa-33fecc4666df.jpg)

## Deploying to Lambda

Inside the main folder, run:

```
sudo pip3 install requests -t ./ --upgrade \
&& sudo pip3 install pytz -t ./ --upgrade \
&& sudo zip -r lambda_function.zip . \
&& sudo rm -rf -v !("lambda_function.py"|"README.md"|"lambda_function.zip")
```

and then upload the package into Lambda console. Or in terminal run:

```
aws --profile qa --region us-east-1 lambda update-function-code --function-name notification_pipeline_service_staging --zip-file fileb://lambda_function.zip \
&& aws --profile qa --region us-east-1 lambda update-function-code --function-name notification_pipeline_lambda_staging --zip-file fileb://lambda_function.zip
```
