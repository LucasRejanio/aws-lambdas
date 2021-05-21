## Notifications CodePipeline

Esse Lambda é bem simples. Basicamente é uma implementação do CodeStarNotifications direto no CodePipeline. A arquitetura funciona da seguinte maneira: 

- O **CodeStarNotifications** fica monitorando o **CodePipeline** e pegando os eventos de exeção do mesmo.

- Logo depois ele envia esses eventos para um tópico **SNS**.

- O SNS por sua vez, é responsável por triggar o lambda por meio de uma **subscription**.

- E por fim o **Lambda** irá receber essa mensagem. Realizar uma tratativa. Pegar os valores de Webhook de um **ParameterStore**. Validar se existem um prefixo no nome da Pipeline. E mediante esse prefixo encaminhar a mensagem para o **canal slack** desejado.

#### Arquitetura
![Notifications Deploy](https://user-images.githubusercontent.com/52427398/119199098-de0db880-ba60-11eb-92cd-138767424154.jpg)
