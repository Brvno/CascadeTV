import socket
import time
import threading
import sys, getopt
import os

## from Dns import DnsServer

# Constantes
REPLICA_DNS_PORT = 13005
MSG_PORT = 13013
DNS_PORT = 10000
MAX_ID = 666

#TODO: Adicionar DNS Master na lista

class DnsServer(object):
    #@args: IP do DNS Lider
    def __init__(self, master_IP = 0):
        print "Cascade TV DNS Server instanciado"
        
        self.listen_addr = ("", DNS_PORT)
        self.replica_addr = ("", REPLICA_DNS_PORT)
        self.stream_list = {}
        self.dns_list = []
        self.dns_id = MAX_ID
        
        #Socket para funcionalidades do DNS
        self.dnsSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        self.dnsSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        
        #Socket responsavel para administracao interna. Como Replicacao e Consistencia
        self.internSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        self.internSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Socket responsavel para administracao interna. Como Replicacao e Consistencia
        self.msgSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        self.msgSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
	    #Bindings
        self.dnsSock.bind(self.listen_addr)
        self.internSock.bind(self.replica_addr)
        self.msgSock.bind(("", MSG_PORT))

	
		
        #Variavel de controle das atualizacoes
        self.leasing = False
        
        #Verifica lider
        if(master_IP == 0):
            self.master_addr = ('localhost', REPLICA_DNS_PORT)
            self.isMaster = True
        else:
            self.master_addr = (master_IP, REPLICA_DNS_PORT)
            self.isMaster = False
             

    # Comeca DNS Server
    def start(self):
        print "Loading..."
                
        if(self.isMaster):
            print "Cascade TV Master DNS Server running..."
            #Abre Threads do Master
            thread_master = threading.Thread(target=self.recvTH)
            thread_consistencia = threading.Thread(target=self.consistencia)
            thread_funcionalidade = threading.Thread(target=self.funcionalidade)
            
            thread_master.start()
            thread_consistencia.start()
            thread_funcionalidade.start()

            while True:
                time.sleep(10)
               
                print "==== DNS LIST ==="
                for i in self.dns_list:
                    print i[0]
                print "================="
                print ""

            
        else:
            #Avisa o Master que virou um slave. Recebe Seu ID como retorno
            for i in range(1,4):   
                print "Tentando Conexao com o Master..."

                self.internSock.sendto(str('Replic'), self.master_addr)

                print "Esperando resposta do Master"
                self.internSock.settimeout(3.0)
                try:
                    msg, lixo = self.internSock.recvfrom(2048)
                    print "Conectou no Master DNS ", self.master_addr
                    print "====", msg, lixo 
                    self.dns_id = msg.split(":")[1]
                    break
                except:       
                    print "Tempo esgotado"
             
             #Abre Threads do Slave
            thread_eleicao = threading.Thread(target=self.aguarda_eleicao)
            thread_aguarda_msg = threading.Thread(target=self.aguarda_mensagem)
            thread_consistencia = threading.Thread(target=self.consistencia)
            #thread_slave = threading.Thread(target=self.recvTH)
            #self.consistencia()
            #thread_slave.start()
            thread_aguarda_msg.start()
            thread_eleicao.start()
            thread_consistencia.start()

                
    #envia a lista das streams para os viewers
    def send_list(self, addr):
    	print "viewer conectou e enviou a lista de streamers pra ele"
        self.dnsSock.sendto(str(self.stream_list), addr)
      
    #faz o controle das conexoes dos viewers e streamers    
    def funcionalidade(self):
        #TODO ARRUMAR 
        
        while True:
            #TODO deve-se criar um novo parametro booleano,se streamer e premium ou nao
            data, addr = self.dnsSock.recvfrom(1024)
            string = data.split(':')
            print string
            print data, addr
            
            # Report on all data packets received
            # data -> <tipo>:<nome>

            #Se recebeu uma mensagem de uma stream,adiciona a stream na lista de todas as stream
            if string[0] == 'stream':
                self.stream_list[string[1]] = addr
                self.leasing = True
            #se recebeu uma mensagem de um viewer ele envia de volta uma lista com todas as streams e o ip dos streamers
            
            elif string[0] == 'viewer':
                self.send_list(addr)
                
            print " --Stream List-- "
            print self.stream_list
   
    
    #Thread esperando replicas
    def adiciona_replica(self, addr):        
        if not addr in self.dns_list:
            print ("Replica conectada", addr[0])
            self.internSock.sendto("ID:"+str(len(self.dns_list)), addr)
            self.dns_list.append(addr)
            self.leasing = True
                         
    #Thread da consistencia. Onde fica atualizando os dados das replicas
    def consistencia(self):
        while True:
            if self.isMaster and self.leasing:
                #Enviando dados para as Replicas
                for rep_addr in self.dns_list:
                    print "Atualizando listas do", rep_addr[0]
                    #self.internSock.sendto(str(self.dns_list), rep_addr)
                    self.internSock.sendto(str(self.stream_list), rep_addr)
                    #time.sleep(3)
                #    updateSock.sendto(str(self.stream_list), rep_addr)
                self.leasing = False

                

            #Slaves consistencia
            elif not self.isMaster:
                #Se passar 10s sem atualizacoes, pede o Master
                self.internSock.settimeout(30.0)
                try:
                    data, a = self.internSock.recvfrom(2048)
                    print "Atualizacao Recebida"
                    self.dns_list = self.convertData2List(data)

                    print "==== DNS LIST ==="
                    for i in self.dns_list:
                        print i
                    print "================="
                    print ""

                    data, a = self.internSock.recvfrom(2048)
                    self.steam_list = data
                    print "==== Stream LIST ==="
                    print self.stream_list
                    print "================="
                    print ""
                

                except:
                    print "Requisitando Update do Master"
                    self.internSock.sendto("Update", self.master_addr)
                
    #Thread do Master para receber mensagens e trata-las
    def recvTH(self):
        while True:
            try:
                data, rep = self.internSock.recvfrom(1024)
                if data == 'Update':
                    print "Requisitado Update", rep[0]
                    self.leasing = True
                    data = ''
                elif data == 'Eleicao':
                    print "Requisitado Eleicao", rep
                    self.eleicao()
                    self.internSock.sendto("sou maior", rep)
                    data = ''
                elif data == 'Replic':
                    self.adiciona_replica(rep)
                    data = ''
            except:
                print ""
           

                    
    def eleicao(self):
        print '== Comecando a eleicao =='
        for index in range(0, int(self.dns_id)):
            #Envia para os maiores ID


            print "Hey, id=",index, self.dns_list[index], ". Exijo uma nova eleicao"
            self.internSock.sendto('Eleicao', (self.dns_list[index][0], MSG_PORT))

        #thread fica esperando o tempo acabar                    
        self.internSock.settimeout(10.0)               
        try:
            data, addr  = self.internSock.recvfrom(1024)

            #Alguem tem mais prioridade
            if( data == 'sou maior'):
                print "Nao serei o lider"
                print "Aguardando a nomeacao"
                
                data, addr  = self.msgSock.recvfrom(1024)
                lider = data.split(':')
                if(lider[0] == 'novo_lider'):  
                    lider = lider[1].replace("'", "")
                    self.master_addr = (lider, REPLICA_DNS_PORT)
                    print "Lider nomeado", self.master_addr[0]
                    
        except:              
            #Ganho a eleicao
            self.isMaster = True
            self.master_addr = self.dns_list[int(self.dns_id)]
            #Aviso que ganhei para todos
            print ">>>>>>>>> Kneel before me. <<<<<<<<<<"
            for index, dns in enumerate(self.dns_list):
                if index != self.dns_id:
                    print "Avisando ", dns[0]
                    self.internSock.sendto('novo_lider:'+str(self.master_addr[0]), (dns[0], MSG_PORT))

    def aguarda_mensagem(self):
        while True:
            elec, addr = self.msgSock.recvfrom(1024)

            if elec == "Eleicao":
                print '-----------| Eleicao Requisitada |----------- '
                #envia que eh maior. Utilizando internSock, por isso espera em outra porta
                self.internSock.sendto('sou maior', (addr[0], REPLICA_DNS_PORT))
                self.eleicao()
            else:
                lider = elec.split(':')
                if(lider[0] == 'novo_lider'):  
                    lider = lider[1].replace("'", "")
                    self.master_addr = (lider, REPLICA_DNS_PORT)
                    print "Lider nomeado", self.master_addr
           
    def aguarda_eleicao(self):        
        while True:
            eleicao = raw_input() 
            if eleicao == 'ELEICAO':
                print '-----------| Eleicao Requisitada |----------- '
                self.eleicao()


    #Funcao para converter listas de tuplas que foram recebidas como strings
    def convertData2List(self, data):
        data = data.replace("[","")
        data = data.replace("]","")
        data = data.replace("),",")|")
        data = data.split('|')

        lis = []
        for element in data:
            element = element.replace('(','')
            element = element.replace(')','')
            element = element.split(',')
            element[0] = element[0].replace('\'','') 
            element[0] = element[0].replace(' ','') 
            element[1] = int(element[1])
            lis.append((element[0], element[1]))

        return lis
        
     #TODO algoritmo eleicao
     #eleicao vai ser uma thread que vai ficar rodando em todos os dns esperando a string "eleicao" ser digitada no teclado
    #def Eleicao(self)
        #detectou que eleicao foi escrito
        #envia eleicao e seu id para todos os dns com id maior que o seu
        #aguarda a resposta de confirmacao de todos os dns com id maior
        #se nao recebeu nenhuma resposta de confirmacao
        #     envia lider e seu id para todos os computadores
        #senao
        #     aguarda mensagem de novo lider
    #TODO manutencao do server premium
    #server premium deve contantemente enviar mensagens sobre viewers que conectaram nele e viewers que desconectaram dele
    #para garantir a exclusao mutua ja que o numero de viewers no server premium e limitado
    #def Controla_server_premium()
    #   thread recebe mensagens do server premium
    #   se a mensagem e "viewer desconectou"
    #       qtd_viewers--
    #       se a qtd_viewers == qtd_maxima-1
    #       ativa mutex travando lista de streams
    #       altera ip da stream na lista de streams,do ip do streamer para o ip do server premium      
    #   se a mensagem e "viewer conectou"
    #       qtd_viewers++
    #       se a qtd_viewers == qtd_maxima
    #           ativa mutex travando lista de streams
    #           altera o ip da stream na lista de streams, do ip do server premium para o ip do streamer
    #     
 
if __name__ == "__main__":
    os.system('clear')

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:m", ["help", "master="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        print "Criando DNS Master: dnsServer.py -m <IPv4>"
        print "Criando DNS Slave: dnsServer.py"
        sys.exit(2)
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print "Criando DNS Master: dnsServer.py -m <IPv4>"
            print "Criando DNS Slave: dnsServer.py"
            sys.exit()
        elif o in ("-m", "--master"):
            cascade = DnsServer(str(args[0]))
        else:
            assert False, "unhandled option"
    
    if not opts:
        cascade = DnsServer()

    cascade.start()
