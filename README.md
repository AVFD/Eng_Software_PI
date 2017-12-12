# Projeto fechadura eletrônica

### Colocar servidor online Frontend
Após clonar o projeto, (git clone https://github.com/AVFD/Eng_Software_PI.git), para subir o servidor do front end faça:

* Ferramentas necessárias: npm, nodejs, angular/cli
  + Instalando npm: sudo apt install npm
  + Instalando nodejs (para versão utilizada 6.x): curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
  sudo apt install nodejs
  + Instalando angular e typescript: sudo npm install -g typescript, sudo npm install -g @angular/cli
  
Agora basta realizar os seguintes procedimentos:

* Entre na pasta /frontend
* Digite ng serve
* Após a compilação ficar chegar ao 100%, abra o navegador em localhost:4200. Caso queira outra porta especifique com o comando:
* ng serve -p numeroPorta.

### Colocar servidor online Backend

Para segunrança, primeiro deve-se criar um abimente virutal.

Neste caso, iremos utilizar o miniconda.

Para baixar o miniconda, acesse o link a seguir:
  https://conda.io/miniconda.html

Para criar um novo ambiente virtual, digite no terminal:
    # conda create -n nome\_do\_ambiente python=3

Para iniciar um ambiente virtual já criado, digite no terminal:
    # source activate nome\_do\_ambiente

No ambiente criado, instale as bibliotecas baseada no arquivo "requeriments.txt" que está acompanhado.
Para isso, digite:
 #### pip install -r requeriments.txt


Configurando os parâmetros do banco de dados:
Antes de executar o back-end, é necessário configurar o arquivo de configuração.
Na pasta "backend" abra o arquivo "config.py". Mude o valor da variável "SQLALCHEMY_DATABASE_URI" para o valor adequado que represente seu banco de dados.

Depois, vá até o arquivo "run.py" que encontra-se na mesma pasta. Altere os parâmetros do "app.run" para valores adequados a sua conexão com o banco de dados.

Feito isso, pode-se rodar o server. Para roda-lo, dentro da pasta "back-end", digite:
  #### python3 run.py
