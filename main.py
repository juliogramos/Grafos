from grafo import Grafo

#Teste de grafos dirigidos com funcoes auxiliares
grafo1 = Grafo('fluxo.net')
grafo2 = Grafo('pequeno.net')
grafo3 = Grafo('cor3.net')
#Esse metodo imprime para o arquivo debug.txt
#grafo1.debugDics()
#Esse imprime no terminal
#grafo1.debugQ1A3()

#Questao 1
#grafo1.printEdmondsKarp(grafo1.edmondsKarp(1,4))

#Questao 2
print(grafo2.hopcroftKarp())

#Questao 3
#print(grafo3.lawler())