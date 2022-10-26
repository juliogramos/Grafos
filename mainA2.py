from grafo import Grafo

#Teste de grafos dirigidos com funcoes auxiliares
grafo1 = Grafo('dirigido2.net', None, None)
#Esse metodo imprime para o arquivo debug.txt
grafo1.debugDics()
#Esse imprime no terminal
grafo1.debugQ1A2()

#Questao 1
grafo1.printCFC(grafo1.CFC())

#Questao 2
grafo2 = Grafo('manha.net', None, None)
grafo2.printOT(grafo2.OT())

#Questao 3
grafo3 = Grafo('testeAGM.txt', None, None)
grafo3.printKruskal(grafo3.kruskal())