from logging import NullHandler
from math import inf
from queue import Queue

class Grafo:

    #QUESTAO 1

    def __init__(self, arquivo) -> None:
        # O contéudo da lista no indíce v é o conteúdo do vértice v.
        # Por enquanto, só rótulo
        self.vertices = []

        # O conteúdo da lista no indíce v é uma lista de tuplas.
        # As tuplas contém um vértice adjacente a v e o peso da aresta.
        self.arestas = []

        self.ler(arquivo)
        self.debugLists()

    def qtdVertices(self) -> int:
        return len(self.vertices)

    def qtdArestas(self) -> int:
        contador = 0
        for i in range(len(self.vertices)):
            contador += len(self.arestas[i])
        return contador//2

    def grau(self, v: int) -> int:
        return len(self.arestas[v])

    def rotulo(self, v: int) -> str:
        return self.vertices[v]

    def vizinhos(self, v: int) -> list:
        vizinhos = []
        for i in self.arestas[v]:
            vizinhos.append(i[0])
        return vizinhos

    def haAresta(self, u: int, v: int) -> bool:
        for i in self.arestas[u]:
            if i[0] == v:
                return True
        return False

    def peso(self, u: int, v: int) -> int:
        for i in self.arestas[u]:
            if i[0] == v:
                return i[0]
        return inf

    def ler(self, arquivo):
        mode = ""
        with open(arquivo) as f:
            for line in f:
                newline = line.strip().split(' ')
                if newline[0] == "*vertices":
                    mode = "VERTICES"
                    self.vertices = ["VAZIO"] * (int(newline[1]) + 1)
                    for _ in range (int(newline[1]) + 1):
                        self.arestas.append([])
                elif newline[0] == "*edges":
                    mode = "EDGES"
                else:
                    if mode == "VERTICES":
                        self.vertices[int(newline[0])] = newline[1]
                    elif mode == "EDGES":
                        v = int(newline[0])
                        u = int(newline[1])
                        peso = float(newline[2])
                        self.arestas[v].append((u,peso))
                        self.arestas[u].append((v,peso))

    def debugLists(self):
        debugFile = open('debug.txt', 'w')
        print("VÉRTICES + RÓTULOS", file=debugFile)
        for i in range(len(self.vertices)):
            vertice = str(i)
            rotulo = self.vertices[i]
            txt = vertice + ' ' + rotulo
            print(txt, file=debugFile)
        print("ARESTAS", file=debugFile)
        for i in range(len(self.arestas)):
            if self.arestas[i] == []:
                continue
            for j in self.arestas[i]:
                v = str(i)
                u = str(j).strip("(),")
                txt = v + ' ' + u
                print(txt, file=debugFile)
        print(self.qtdArestas(), file=debugFile)
        debugFile.close()

    #QUESTAO 2

    def buscaEmLargura(self, s):
        c = [False] * len(self.vertices)
        d = [inf] * len(self.vertices)
        a = [None] * len(self.vertices)
        c[s] = True
        d[s] = 0
        q = Queue(len(self.vertices))
        q.put(s)
        while q.empty() == False:
            u = q.get()
            for v in self.vizinhos(u):
                if c[v] == False:
                    c[v] = True
                    d[v] = d[u] + 1
                    a[v] = u
                    q.put(v)
        return (d, a)

    #QUESTAO 3

    def cicloEuleriano(self):
        #Cria dicionário com todas as arestas sem duplicatas
        todasArestas = []
        for index, arestas in enumerate(self.arestas):
            for aresta in arestas:
                novaTupla = (index,) + (aresta[0],)
                novaTupla = frozenset(novaTupla)
                todasArestas.append(novaTupla)
        c = dict.fromkeys(todasArestas)
        #print(c)

        #Comeca algoritmo
        for key in c:
            c[key] = False

        v = list(list(c)[0])[0]

        (r, ciclo) = self.buscaCiclo(v, c)

        if r == False:
            return (False, None)
        else:
            lista = c.values()
            for i in lista:
                if i == False:
                    return (False, None)
            return (True, ciclo)


    def buscaCiclo(self, v, c):
        ciclo = [v]
        t = v

        while True:
            vizinhos = self.vizinhos(v)
            breakFlag = 0
            u = None
            for i in vizinhos:
                teste = frozenset([i,v])
                if c[teste] == False:
                    u = i
                    break
                else:
                    breakFlag += 1
            if breakFlag == len(vizinhos):
                return (False, None)
            else:
                c[frozenset((v, u))] = True
                v = u
                ciclo.append(v)
            if v == t:
                break

        for x in ciclo:
            vizinhosX = self.vizinhos(x)
            for w in vizinhosX:
                if c[frozenset((x,w))] == False:
                    (r, ciclo2) = self.buscaCiclo(x, c)
                    if r == False:
                        return (False, None)
                    index = ciclo.index(x)
                    ciclo = ciclo[:index] + ciclo2 + ciclo[index+1:]
        return (True, ciclo)

    #QUESTAO 4

    def bellmanFord(self,s):
        #Cria dicionário com todas as arestas sem duplicatas
        # e coloca pesos
        todasArestas = []
        pesos = []
        for index, arestas in enumerate(self.arestas):
            for aresta in arestas:
                novaTupla = (index,) + (aresta[0],)
                novaTupla = frozenset(novaTupla)
                todasArestas.append(novaTupla)
                pesos.append(aresta[1])
        E = dict.fromkeys(todasArestas)
        pesos = list(dict.fromkeys(pesos))
        keys = E.keys()
        for index, key in enumerate(keys):
            E[key] = pesos[index]
        #for key, value in E.items():
            #print(key, ' : ', value)

        #Começa o algoritmo
        d = [inf] * len(self.vertices)
        a = [None] * len(self.vertices)
        d[s] = 0

        for i in range(len(self.vertices) - 1):
            for aresta in E.keys():
                aTupla = tuple(aresta)
                u = aTupla[0]
                v = aTupla[1]
                print('u: ' + str(u) +'\nv: ' + str(v) + '\nd[u]: ' + str(d[u]) + '\nd[v]: ' + str(d[v]))

                if  d[u] != inf and d[v] > (d[u] + E[aresta]):
                    d[v] = d[u] + E[aresta]
                    a[v] = u

                if  d[v] != inf and d[u] > (d[v] + E[aresta]):
                    d[u] = d[v] + E[aresta]
                    a[u] = v

            print(d)
            
        for aresta in E.keys():
            aTupla = tuple(aresta)
            v = aTupla[0]
            u = aTupla[1]

            if d[u] != inf and d[v] > d[u] + E[aresta]:
                return (False, [], [])

            if d[v] != inf and d[u] > d[v] + E[aresta]:
                return (False, [], [])

        return (True, d, a)