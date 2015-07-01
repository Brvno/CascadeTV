# CascadeTV
Sistema de stream em cascata

~~~~~ DNS Algorithm ~~~~~~~~~
	Consistência e Replicação
	
se DNS is master
	Abrir conexão da porta do DNS
	-- Thread Replicas--
		Esperar requisicao das replicas
		Se recebeu requisião
			Adiciona na lista de replicas
			Envia lista de dns para todos

	-- Thread Consistentcia --
		Envia dados para as outras replicas

	-- Thread Funcionalidade -- 
		Papel do dns
		
se DNS is slave
	Conectar com DNS(Master)
	Recebe lista de replicas
	Deixa aberto comando para eleicao



