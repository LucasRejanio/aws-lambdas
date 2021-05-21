# Start and stop ec2 AWS
Essa documentação tem como objetivo realizar o processo de automatização de Start e Stop de instancia ec2(Amazon Web Services) utilizando Lambda aplicado com Python. 

## Overview 
- [ ] Criar política
- [ ] Criar função vinculada a política
- [ ] Criar funções lambda para start e stop
- [ ] Configurar o CloudWatch para start e stop

## Criando uma política personalizada
A primeira coisa a se fazer é criar uma política personalizada, para essa tarefa vamos acessar o console da aws e vamos procurar o servço **Acess Menagement (IAM)** - Politicas (Policies).

  #### Passos:
  - Create policy
  - Opção de JSON 
  - Copiar e colar o json abaixo 
 
  #### Create policy
  
  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "ec2:Start*",
          "ec2:Stop*"
        ],
        "Resource": "*"
      }
    ]
  }
  ```
  
## Criando uma função 
Ainda na parte de **Acess Menagement (IAM)** vamos acessar a parte de Funções (Roles). 

  #### Passos
  - Create role
  - Caso de uso: Lambda  
  - Selecionar nossa politica 
  - Atribuir nome para função

É importante lembra que depois que a função estiver criada, vamos acessar a parte de permissões e anexar a política **AmazonEC2FullAccess**

## Criando função lambda
Para criar uma função lambda iremos acessar o console na parte **lambda**

  #### Informações básicas de criação
  - Para Nome da função , insira um nome que o identifique como a função usada para interromper suas instâncias EC2. Por exemplo, "StartEC2Instances"
  - Para Runtime , escolha Python 3.7 
  - Em Permissões , expanda e selecione a opção de usar uma função existente
  - Selecione a função criada anteriormente
 
  Observação: para região , substitua "us-west-1" pela região AWS em que estão suas instâncias. <br />
  Substitua os IDs de instância EC2 de exemplo pelos IDs das instâncias específicas que você deseja parar e iniciar.
  
  #### Função de Start
  
  ```python
  import boto3
  region = 'us-west-1'
  instances = ['i-12345cb6de4f78g9h']
  ec2 = boto3.client('ec2', region_name=region)

  def lambda_handler(event, context):
      ec2.start_instances(InstanceIds=instances)
      print('started your instances: ' + str(instances))
  ```
  
  Logo depois da criação defina o tempo limite para 10 segundos em configurações básicas.
  
  #### Realize novamente o processo para criar dessa vez a funcão para Stop
  
  #### Função de Stop
  
  ```python
  import boto3
  region = 'us-west-1'
  instances = ['i-12345cb6de4f78g9h']
  ec2 = boto3.client('ec2', region_name=region)

  def lambda_handler(event, context):
      ec2.stop_instances(InstanceIds=instances)
      print('stopped your instances: ' + str(instances))
   ```
    
## Crie regras que acionem suas funções Lambda
Para realizar essa etapa iremos acessar o console novamente ir no serviço de **CloudWatch**  
  
  #### Informações básicas de criação
  - No painel de navegação esquerdo, em Events , escolha Rules 
  - Escolha create rule
  - Em event source , schedule
  - Cron expression 
  - Em target, adicione um target
  - Target deve ser a função Lambda (Nesse caso a função de Start)
  
  #### Detalhes
  Na parte de cron devemos no atendar em alguns detalhes, por exemplo, como estamos no Brasil sempre iremos nos basear no fuso horário. Nesse caso, sempre iremos configurar
  com tês horas de atraso. 
  
  #### Exemplo de cron: 
  Nesse exemplo, quero que realize o Start da ec2 de segunda a sexta, sempre as 10h da manhã. 
  
  ```
  00 13 ? * MON-FRI * 
  ```
  #### Realize novamente o processo para criar dessa vez a regra cron para a função de Stop
  
  #### Informações básicas de criação
  - No painel de navegação esquerdo, em Events , escolha Rules 
  - Escolha create rule
  - Em event source , schedule
  - Cron expression 
  - Em target, adicione um target
  - Target deve ser a função Lambda (Nesse caso a função de Stop)
  
  #### Exemplo de cron: 
  Nesse exemplo, quero que realize o Stop da ec2 de segunda a sexta, sempre as 18h da noite.
  
  ```
  00 21 ? * MON-FRI * 
  ```
## Conclusão

- [x] Criar política
- [x] Criar função vinculada a política
- [x] Criar funções lambda para start e stop
- [x] Configurar o CloudWatch para start e stop
  
