# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:35:56 2019

@author(s): Douglas Violante, Daniel Colioni, Rodrigo Carrareto
"""
# Versão Windows Apenas!

import socket 

html_file = []

listen_socket = socket.socket()           #Criando um objeto do tipo socket
HOST, PORT = socket.getfqdn(), 80         #Definindo o nome do HOST(Nome do computador) e a porta
listen_socket.bind(("192.168.42.87" , PORT))         #Utilizando a função bind para ligar o HOST e o PORT

print("\nServidor Iniciado!")
print("\nAguardando na porta: %s" % PORT)

listen_socket.listen(1)                   #Fazendo o servidor esperar por alguma conexão


def html_OK_Streamer(client_connection, html_file):
    
    #Cabeçalho de 200 Ok
    client_connection.send("HTTP/1.1 200 OK\r\n".encode())
    client_connection.send("Content-Type: text/html\r\n".encode())
    
    output_stream = html_file.read() #Lê página html requisitada
        
    for i in range(0, len(output_stream)): #Strema o conteúdo da página HTML passada no argumento
        client_connection.send(output_stream[i].encode())
            
    client_connection.send("\r\n".encode()) 
    client_connection.close()
 
    
while(True):                                                            
    
    (client_connection, client_address) = listen_socket.accept()        #Aceitando conexões
    request = client_connection.recv(1024).decode()                     #Recebendo uma requisição de conexão
    print("\nOrigem da Conexao: ", client_connection, client_address)   #Mostrando na tela o IP do usuário
    print("\n", request)                                                #Mostra request recebido do cliente

    
    try: 
        
        #Tratamento da requisição
        filename = request.split()[1]
        filename = filename.replace('/', '')
        filename2 = filename + '.html'
        
        #Tenta abrir o arquivo requisitado, gera exceção se não encontrado
        html_file = open(filename2) 
        
        html_OK_Streamer(client_connection, html_file)
        
        print("\nPagina Entregue!")
        print("\n ------------------------------------------------ ")

    except IOError:
        
        print(filename2, "Not Found!")
        
        #Cabeçalho de 404 Not Found
        client_connection.send("HTTP/1.1 404 NOT FOUND \r\n".encode())
        
        client_connection.close()
        
        print("\nEnvio de Not Found Entregue")
        print("\n ------------------------------------------------ ")
