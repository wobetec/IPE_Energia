# Inicializando o programa na máquina física


### Instalação e clonagem do repositório
  &emsp;&emsp;Primeiramente, verifique se sua máquina possui a linguagem de programação PYTHON e o sistema de controle de versões GIT instalados em sua versão mais recente.
  <br></br>
  &emsp;&emsp;Agora, devemos clonar o github em questão, a partir do comando:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;git clone <url-do-repositório>
  <br></br>
  &emsp;&emsp;Em caso afirmativo, crie um ambiente virtual, ou "venv", a partir do seguinte comando:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;python -m venv env
  <br></br>
  &emsp;&emsp;Logo após, devemos ativar o venv, da seguinte forma:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;./env/Script/activate

### Instalações necessárias e inicialização do aplicativo
  &emsp;&emsp;Devemos entrar na pasta que possui o arquivo "requirements.txt" e, após isso, executar o seguinte comando via terminal:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;pip -r install requirements.txt
  <br></br>
  &emsp;&emsp;Após o passo acima, basta executar o seguinte comando:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;flask run
  <br></br>
  &emsp;&emsp;Após isso, o site deverá estar rodando localmente em sua máquina.

## Para utilizar o aplicativo sem o banco de dados clonado do github:
  &emsp;&emsp;Execute o seguinte comando para reiniciar o banco de dados do zero:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;python cmd.py migrate
  <br></br>
  &emsp;&emsp;Após estar com a base de dados limpa, aplique o seguinte comando:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;flask run
  <br></br>
  &emsp;&emsp;Assim, na tela de login, utilize o comando de exemplo a seguir:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;http://127.0.0.1:5000/register/esdras/senha
  <br></br>
  &emsp;&emsp;Assim, você terá um login e senha do seguinte modo:
        <br></br>
        &emsp;&emsp;&emsp;&emsp;login: esdras
        <br></br>
        &emsp;&emsp;&emsp;&emsp;senha: senha (a que foi atribuída na url)
  <br></br>
  &emsp;&emsp;Daí em diante, basta continuar utilizando normalmente o site, porém cadastrando todas as concessionárias e tarifas necessárias para utilizar nas OMs posteriormente cadastradas.
  
        
