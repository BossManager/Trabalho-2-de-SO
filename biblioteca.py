from menus import *

def detectarDeadlock(): #pronto
	#SIMULACAO
	shadow_rp = list(map(list,registrosPedidos)) #copia lista de pedidos em aberto pelos alunos
	shadow_qe = list(qtdExemplares) #copia lista de exemplares disponiveis
	shadow_r = list(map(list,registros)) #copia lista de exemplares alugados por cada aluno
	#Tenta percorrer até a lista ficar vazia
	while shadow_rp:
		achou = False # Flag para sinalizar se algum aluno foi atendido durante alguma iteração do loop
		for k,i in enumerate(shadow_rp):
			#verifica se o pedido do aluno 'k' pode ser atendido
			if sum([1 for y,p in enumerate(i) if p<=shadow_qe[y]])==len(shadow_qe):
				#aluno libera os livros, os valores são adicionados a lista de exemplares disponiveis
				shadow_qe = [l1+l2 for l1,l2 in zip(shadow_r[k],shadow_qe)] 
				#deleta pedido de livros do aluno 'k'
				del shadow_rp[k]
				# sinaliza que um aluno foi atendido
				achou = True
		# nenhum aluno atendido == 'DEADLOCK'
		if not achou:
			return True #deadlock detectado
	return False #deadlock não detectado

def atenderAluno():#pronto
	# Checar se algum pedido pode ser atendido pelos livros devolvidos pelo aluno atual
	for m,i in enumerate(registrosPedidos):
		#cada objeto 'i' é uma lista [e1,e2,e3,..,en] dos exemplares que o aluno 'm'tem de cada livro
		# variavel para contar quantos pedidos de livros foram atendidos para o aluno 'm'
		cont = sum([1 for k,j in enumerate(i) if qtdExemplares[k]>=j])
		#checa se a quantidade de exemplares atendidos é igual a quantidade de livros
		if cont == qtdLivros and sum(i)!=0:
			# entrega os livros para o aluno 'm'
			# e retira os livros entregue para o aluno 'm' da lista de exemplares disponiveis
			for k,j in enumerate(i):
				registros[m][k] += j
				qtdExemplares[k] -= j
			# zera o registro de pedidos do aluno 'm'
			registrosPedidos[m] = [0 for i in range(qtdLivros)]
			print('Livros entregues ao aluno ',m,'.')
	print()

##################################
# FUNÇÕES ALUNO                  #
##################################
def acao_Pedido(): #pronto
	print('Pedido de livro:')
	id_aluno = int(input('Id do aluno: '))
	if not id_aluno in range(qtdAlunos):
		print('Aluno não cadastrado no sistema')
		return
	id_livro = int(input('Id do livro: '))
	if not id_livro in range(len(qtdExemplares)):
		print('Livro não cadastrado no sistema')
		return
	qtExemplares = int(input('Qtd de exemplares: ')) #exemplares que o aluno quer do livro 'id_livro'
	#verifica se o aluno esta em estado de espera
	if sum(registrosPedidos[id_aluno]) == 0:
		#verifica se tem exemplares suficiente do livro 'id_livro'
		if qtExemplares <= qtdExemplares[id_livro]:
			#coloca os exemplares do livro 'id_livro' no registro dos alunos
			registros[id_aluno][id_livro] += qtExemplares 
			#atualiza a quantidade de exemplares do livro 'id_livro' 
			qtdExemplares[id_livro] -= qtExemplares 
			print('Pedido realizado com sucesso!')
		else:
			#Registra o pedido de exemplares do aluno 
			registrosPedidos[id_aluno][id_livro] += qtExemplares
			#se deadlock for detectado,o pedido é cancelado	
			if detectarDeadlock():
				registrosPedidos[id_aluno][id_livro] -= qtExemplares
				print('Alerta: Exemplares não disponíveis. Seu pedido não pode ser realizado por dependencia circular.')
			else:
				print('Alerta: Exemplares não disponíveis. Aluno ',id_aluno,' em estado de espera.')
	else:
		print('Ação bloqueada.Aluno em estado de espera!!!')
	print()
def acao_Liberar(): #pronto
	print('Pedido de livro:')
	id_aluno = int(input('Id do aluno: '))
	if not id_aluno in range(qtdAlunos):
		print('Aluno não cadastrado no sistema')
		return
	#verifica se o aluno esta em estado de espera
	if sum(registrosPedidos[id_aluno]) == 0:
		#devolve todos os exemplares que o aluno 'id_aluno' pegou
		for k,i in enumerate(registros[id_aluno]):
			qtdExemplares[k] += i
		#zera a lista de exemplares do aluno 'id_aluno'
		registros[id_aluno] = [0 for l in range(qtdAlunos)]
		print('Livros devolvidos com sucesso!')
		#tenta atender o pedido em espera de algum aluno
		atenderAluno()
	else:
		print('Ação bloqueada.Aluno em estado de espera!!!')
	print()


##################################
# FUNÇÕES ADMIN                  #
##################################
def acao_Numero_Exemplares_T():#pronto
	print('Lista de livros:')
	#printa a quantidade de livros e de exemplares disponiveis
	for k,i in enumerate(qtdExemplares):
		print('Livro ',k,': ',qtdExemplaresOriginal[k],' (',i,' disponíveis)')
	print()

def acao_Numero_Exemplares_A():#pronto
	#mostra a quantidade e os exemplares pegos por cada aluno
	for k,i in enumerate(registros):
		print('Aluno ',k,': ',end='')
		if sum(i)==0:
			print('nenhum livro')
		else:
			results = []
			#formata a saida para cada aluno que tem exemplares
			for m,j in enumerate(i):
				if j>0:
					results.append(str(j)+' exemplares do livro \"'+str(m)+'\"')
			print(' e '.join(results))
	print()

def acao_Alunos_Espera():#pronto
	print('Alunos em espera:')
	# checa se algum aluna está esperando exemplares serem liberados
	if sum([sum(registrosPedidos[k]) for k in range(qtdAlunos)]) == 0:
		print('Nenhum aluno em espera')
	else:
		#formata a saida para cada aluno
		for k,i in enumerate(registrosPedidos):
			results = []
			if sum(i)>0:
				for m,j in enumerate(i):
					if j>0:
						results.append(str(j)+' exemplares do livro \"'+str(m)+'\"')
				print('Aluno ',k,': Esperando ',' e '.join(results))
	print()



#########################################################################
## Author: Daniel Nogueira de Oliveira, matricula 385386               ##
## Version: 0.3(final)                                                 ##
## status: 100%                                                        ##
#########################################################################

if __name__ == '__main__':
	registros = [] # quantos estao alugados
	qtdExemplares = [] #quantos ainda tem
	registrosPedidos = [] # quantos foram pedidos
	opc = 1
	print("Setup Inicial")
	qtdLivros = int(input("Qtd de livros: "))
	for i in range(qtdLivros):
		qtdExemplares.append(int(input("Qtd de exemplares do livro "+str(i)+": ")))
	# copia da quantidade original de exemplares de cada livro
	qtdExemplaresOriginal = qtdExemplares.copy()
	qtdAlunos = int(input("Qtd de alunos: "))
	#inicia matrizes de registros
	registros = [[0 for i in range(qtdLivros)] for j in range(qtdAlunos)]
	registrosPedidos = [[0 for i in range(qtdLivros)] for j in range(qtdAlunos)]

	while opc==1 or opc==2:
		menu_Usuario()
		opc = int(input('Opcao: '))
		if opc == 1:
			menu_Aluno()
			opc2 = int(input('Opcao: '))
			if opc2 == 1:
				acao_Pedido()
			elif opc2 == 2:
				acao_Liberar()
			else:
				print('Opção invalida.')
		elif opc == 2:
			menu_Admin()
			opc2 = int(input('Opcao: '))
			if opc2 == 1:
				acao_Numero_Exemplares_T()
			elif opc2 == 2:
				acao_Numero_Exemplares_A()
			elif opc2 == 3:
				acao_Alunos_Espera()
			else:
				print('Opção invalida.')
		else:
			print('Opção invalida.')
		

