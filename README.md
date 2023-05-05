# CINtofome

Projeto da Disciplina Infraestrutura de Comunicações - 2022.2

Universidade Federal de Pernambuco - UFPE

Centro de Intromática - CIN

Grupo:

      Hiago Rafael Nunes e Silva
      
      Júlia Albuquerque Machado
      
      Ítallo Antônio dos Santos 
      
## Instruções para rodar o projeto
Python 3.10.6

### Arquivo de leitura

O client envia o arquivo *testFile.txt* da pasta *client*, portanto ele é necessário para que o programa execute

Caso deseje testar com outro arquivo, basta adicioná-lo à pasta *client* e alterar a variável *fileName* em *client.py* para que receba o nome do novo arquivo

### Para excutar o server:

*dentro do diretório server*

```
python3 server.py
```
**Execute o server antes do client**

### Para excutar o client:

*dentro do diretório client*

```
python3 client.py
```
### Simulação de perdas

Em *server.py*, existe uma variável de nome *simularPerda* que recebe uma quantidade de perdas que serão simuladas sequencialmente.

Caso o valor dessa variável seja menor ou igual a 0, nenhuma perda será simulada.

### Arquivos e funcionamento do projeto

Quando em execução, o client irá enviar o arquivo com o nome especificado na variável *fileName* (como dito antes, esse arquivo deve existir no diretório *client*).

Ao iniciar o recebimento, o server irá criar um novo arquivo em seu diretório com o mesmo nome e mesmo conteúdo do enviado pelo client

Finalizada a recepção dos dados enviados pelo client, o server irá devolver os dados para o client, que por sua vez, irá criar um novo arquivo, desta vez com o prefixo *responseFile-*, e escrever os dados recebidos.

Ao final da execução de ambos, a pasta server terá uma cópia de mesmo nome e conteúdo do arquivo enviado pelo client, enquanto que a pasta client terá o arquivo original mais o arquivo resposta com prefixo citado no parágrafo acima

Tanto o arquivo cópia na pasta *server* quanto o arquivo resposta na pasta *client* podem ser apagados para melhor visualização da execução dos programas