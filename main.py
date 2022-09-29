from grafo import Grafo

#Questao 1
grafo1 = Grafo('dolphins.net')
#Esse metodo imprime para o arquivo debug.txt
grafo1.debugDics()
#Esse imprime no terminal
grafo1.debugQ1()

#Questao 2
grafo2 = Grafo('questao2.txt')
grafo2.printBusca(grafo2.buscaEmLargura(4))

#Questao 3
grafo3 = Grafo('ContemCicloEuleriano.net')
grafo3.printCiclo(grafo3.cicloEuleriano())

#Questao 4
grafo4 = Grafo('fln_pequena.net')
grafo4.printBellmanFord(grafo4.bellmanFord(6))

#Questao 5
grafo5 = Grafo('questao2.txt')
grafo5.printFloydWarshall(grafo5.floydWarshall())