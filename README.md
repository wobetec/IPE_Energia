# Inicializando o programa na máquina física
## Instalação e clonagem do repositório
Primeiramente, verifique se sua máquina possui a linguagem de programação Python e o sistema de controle de versões GIT instalados em sua versão mais recente.
Agora, devemos clonar o github em questão, a partir do comando:
      
	git clone https://github.com/wobetec/IPE_Energia

Em caso afirmativo, crie um ambiente virtual, ou "venv", a partir do seguinte comando:
        
	python -m venv env
  
Logo após, devemos ativar o venv, da seguinte forma:
        
	./env/Script/activate
## Instalações necessárias e inicialização do aplicativo
Devemos entrar na pasta que possui o arquivo "requirements.txt" e, após isso, executar o seguinte comando via terminal:
        
	pip -r install requirements.txt
  
Após o passo acima, basta executar o seguinte comando:
        
	flask run
  
Após isso, o site deverá estar rodando localmente em sua máquina.

## Para utilizar o aplicativo sem o banco de dados clonado do github:
Execute o seguinte comando para reiniciar o banco de dados do zero:
        
	python cmd.py migrate
  
Após estar com a base de dados limpa, aplique o seguinte comando:
        
	flask run
  
Assim, na tela de login, utilize o comando de exemplo a seguir:
        
	http:/localhost:5000/register/esdras/senha
  
Assim, você terá um login e senha do seguinte modo:
        
	login: esdras
        
	senha: senha (a que foi atribuída na url)
  
Daí em diante, basta continuar utilizando normalmente o site, porém cadastrando todas as concessionárias e tarifas necessárias para utilizar nas OMs que posteriormente serão cadastradas.
  
        
