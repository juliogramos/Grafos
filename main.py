from math import inf
from grafo import Grafo

def debugQ1(grafo):
    print(grafo.qtdVertices())
    print(grafo.qtdArestas())
    print(grafo.grau(52))
    print(grafo.rotulo(52))
    print(grafo.vizinhos(52))
    print(grafo.haAresta(52, 5))
    print(grafo.haAresta(52, 1))
    print(grafo.peso(52, 5))

def formataBuscaEmLargura(tupla):
    niveis = {}
    n = 0
    for vertice, distancia in enumerate(tupla[0]):
        if distancia != inf:
            if distancia not in niveis:
                niveis[distancia] = []
            niveis[distancia].append(str(vertice))
            if distancia > n:
                n = distancia
    
    for i in range(n+1):
        nivel = ",".join(niveis[i])
        txt = str(i) + ": " + nivel
        print(txt)

grafo1 = Grafo('dolphins.net')
#debugQ1(grafo)

grafo2 = Grafo('questao2.txt')
#formataBuscaEmLargura(grafo2.buscaEmLargura(4))

grafo3 = Grafo('ContemCicloEuleriano.net')
(r, ciclo) = grafo3.cicloEuleriano()
print(r)
print(ciclo)