from math import inf
from queue import Queue

class Grafo:

    #QUESTAO 1

    def __init__(self, arquivo) -> None:
        # As chaves do dicionario sao os numeros dos vertices
        # O conteudo eh o rotulo do vertice
        self.vertices = {}

        # A chave do dicionario eh um conjunto frozenset com dois vertices
        # O conteudo eh o peso da aresta
        self.arestas = {}

        self.ler(arquivo)

    def qtdVertices(self) -> int:
        return len(self.vertices.keys())

    def qtdArestas(self) -> int:
        return len(self.arestas.keys())

    def grau(self, v: int) -> int:
        contador = 0
        for i in self.arestas.keys():
            if v in i:
                contador += 1
        return contador

    def rotulo(self, v: int) -> str:
        return self.vertices[v]

    def vizinhos(self, v: int) -> list:
        vizinhos = []
        for i in self.arestas.keys():
            if v in i:
                lista = list(i)
                for j in lista:
                    if j != v:
                        vizinhos.append(j)
        return vizinhos

    def haAresta(self, u: int, v: int) -> bool:
        if frozenset((u, v)) in self.arestas.keys():
            return True
        return False

    def peso(self, u: int, v: int) -> int:
        if frozenset((u,v)) in self.arestas.keys():
            return self.arestas[frozenset((u,v))]
        return inf

    def ler(self, arquivo):
        mode = ""
        with open(arquivo) as f:
            for line in f:
                newline = line.strip().split(' ')
                if newline[0] == "*vertices":
                    mode = "VERTICES"
                elif newline[0] == "*edges":
                    mode = "EDGES"
                else:
                    if mode == "VERTICES":
                        self.vertices[int(newline[0])] = newline[1]
                    elif mode == "EDGES":
                        v = int(newline[0])
                        u = int(newline[1])
                        peso = float(newline[2])
                        self.arestas[frozenset((u,v))] = peso

    #QUESTAO 2

    def buscaEmLargura(self, s):
        #c = [False] * len(self.vertices.keys())
        c = {}
        for i in self.vertices.keys():
            c[i] = False

        #d = [inf] * len(self.vertices.keys())
        d = {}
        for i in self.vertices.keys():
            d[i] = inf

        #a = [None] * len(self.vertices.keys())
        a = {}
        for i in self.vertices.keys():
            a[i] = None

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
        c = {}
        for key in self.arestas.keys():
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
        E = {}
        for key, value in self.arestas.items():
            E[key] = value

        #Começa o algoritmo
        d = [inf] * (len(self.vertices)+1)

        a = [None] * (len(self.vertices)+1)

        d[s] = 0

        for _ in range(len(self.vertices)):
            for aresta in E.keys():
                aTupla = tuple(aresta)
                u = aTupla[0]
                v = aTupla[1]

                if  d[u] != inf and d[v] > (d[u] + E[aresta]):
                    d[v] = d[u] + E[aresta]
                    a[v] = u

                if  d[v] != inf and d[u] > (d[v] + E[aresta]):
                    d[u] = d[v] + E[aresta]
                    a[u] = v
            
        for aresta in E.keys():
            aTupla = tuple(aresta)
            v = aTupla[0]
            u = aTupla[1]

            if d[u] != inf and d[v] > d[u] + E[aresta]:
                return (False, [], [])

            if d[v] != inf and d[u] > d[v] + E[aresta]:
                return (False, [], [])

        d = d[1:]
        a = a[1:]
        return (True, d, a)

    def floydWarshall(self):
        E = {}
        for key, value in self.arestas.items():
            E[key] = value

        W = [ [None] * (self.qtdVertices()) for _ in range(self.qtdVertices()) ]
        for u in range (self.qtdVertices()):
            for v in range (self.qtdVertices()):
                if u == v:
                    W[u][v] = 0
                elif frozenset((u+1,v+1)) in E.keys():
                    W[u][v] = E[frozenset((u+1,v+1))]
                else:
                    W[u][v] = inf
        D = []
        D.append(W)

        for k in range(1, self.qtdVertices()):
            D.append([ [None] * (self.qtdVertices()) for _ in range(self.qtdVertices()) ])
            for u in self.vertices.keys():
                for v in self.vertices.keys():
                    D[k][u-1][v-1] = min(D[k-1][u-1][v-1], D[k-1][u-1][k] + D[k-1][k][v-1])
        return D[len(self.vertices.keys())-1]


    #FUNCOES PARA PRINT/DEBUG
    def debugQ1(self):
        print(self.qtdVertices())
        print(self.qtdArestas())
        print(self.grau(52))
        print(self.rotulo(52))
        print(self.vizinhos(52))
        print(self.haAresta(52, 5))
        print(self.haAresta(52, 1))
        print(self.peso(52, 5))

    def debugDics(self):
        debugFile = open('debug.txt', 'w')
        print("VERTICES + ROTULOS", file=debugFile)
        for i in self.vertices.keys():
            vertice = str(i)
            rotulo = self.vertices[i]
            txt = vertice + ' ' + rotulo
            print(txt, file=debugFile)
        print("ARESTAS", file=debugFile)
        for i in self.arestas.keys():
            print(str(tuple(i)) + ": " + str(self.arestas[i]), file=debugFile)
        print(self.qtdArestas(), file=debugFile)
        debugFile.close()

    def printBusca(self, tupla):
        n = max(list(tupla[0].values()))
        niveis = [ [] * (n+1) for i in range(n+1) ]
        for key, value in tupla[0].items():
            niveis[value].append(str(key))
        for i in range(n+1):
            nivel = str(i)
            verts = ','.join(niveis[i])
            print(nivel + ": " + verts)

    def printCiclo(self, tupla):
        (r, ciclo) = tupla
        print(r)
        print(ciclo)

    def printBellmanFord(self, tupla):
        (res, d, a) = tupla
        print(res)
        print(d)
        print(a)

    def printFloydWarshall(self, matriz):
        for index, lista in enumerate(matriz):
            strInts = ','.join(str(n) for n in lista)
            print(str(index+1) + ":" + strInts)