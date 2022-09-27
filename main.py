from grafo import Grafo

grafo1 = Grafo('dolphins.net')
grafo1.debugDics()
grafo1.debugQ1()

grafo2 = Grafo('questao2.txt')
grafo2.printBusca(grafo2.buscaEmLargura(4))

grafo3 = Grafo('ContemCicloEuleriano.net')
grafo3.printCiclo(grafo3.cicloEuleriano())

grafo4 = Grafo('fln_pequena.net')
grafo4.printBellmanFord(grafo4.bellmanFord(6))

grafo5 = Grafo('questao2.txt')
grafo5.printFloydWarshall(grafo5.floydWarshall())