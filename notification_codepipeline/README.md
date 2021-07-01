## Notifications CodePipeline

Esse Lambda é bem simples. Basicamente é uma implementação do CodeStarNotifications direto no CodePipeline. A arquitetura funciona da seguinte maneira: 

- O **CodeStarNotifications** fica monitorando o **CodePipeline** e pegando os eventos de exeção do mesmo.

- Logo depois ele envia esses eventos para um tópico **SNS**.

- O SNS por sua vez, é responsável por triggar o lambda por meio de uma **subscription**.

- E por fim o **Lambda** irá receber essa mensagem. Realizar uma tratativa. Pegar os valores de Webhook de um **ParameterStore**. Validar se existem um prefixo no nome da Pipeline. E mediante esse prefixo encaminhar a mensagem para o **canal slack** desejado.

#### Arquitetura
![Notifications Deploy](https://user-images.githubusercontent.com/52427398/119200560-8ae93500-ba63-11eb-9dfa-33fecc4666df.jpg)

![New Model of Pulumi](https://user-images.githubusercontent.com/52427398/124122308-55653d80-da4c-11eb-817c-20151b878c07.jpg)

![New model CI (Website)](https://user-images.githubusercontent.com/52427398/124122379-66ae4a00-da4c-11eb-80db-5ee0d556654b.jpg)


