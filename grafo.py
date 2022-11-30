from math import inf
from queue import Queue
from itertools import chain,combinations

class Grafo:

    #ATIVIDADE 1
    #QUESTAO 1 + auxiliares

    def __init__(self, arquivo, vertices=None, arestas=None) -> None:
        if vertices == None or arestas == None:
            # As chaves do dicionario sao os numeros dos vertices
            # O conteudo eh o rotulo do vertice
            self.vertices = {}

            # A chave do dicionario eh um conjunto frozenset com dois vertices
            # O conteudo eh o peso da aresta
            self.arestas = {}

            self.dirigido = False

            self.ler(arquivo)
        else:
            self.vertices = vertices
            self.arestas = arestas
            if not self.arestas:
                self.dirigido = False
            else:
                if isinstance(list(self.arestas.keys())[0], tuple):
                    self.dirigido = True
                else:
                    self.dirigido = False

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
        if self.dirigido:
            if (u, v) in self.arestas.keys() or (v, u) in self.arestas.keys():
                return True
            return False
        else:
            if frozenset((u, v)) in self.arestas.keys():
                return True
            return False

    def peso(self, u: int, v: int) -> int:
        if self.dirigido:
            if (u,v) in self.arestas.keys():
                return self.arestas[(u,v)]
            elif (v,u) in self.arestas.keys():
                return self.arestas[(v,u)]
            return inf
        else:
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
                    self.dirigido = False
                elif newline[0] == "*arcs":
                    mode = "ARCS"
                    self.dirigido = True
                else:
                    if mode == "VERTICES":
                        rot = ' '.join(newline[1:])
                        self.vertices[int(newline[0])] = rot
                    elif mode == "EDGES":
                        v = int(newline[0])
                        u = int(newline[1])
                        peso = float(newline[2])
                        self.arestas[frozenset((u,v))] = peso
                    elif mode == "ARCS":
                        u = int(newline[0])
                        v = int(newline[1])
                        peso = float(newline[2])
                        self.arestas[(u,v)] = peso

    def mudaCustoResidual(self,par,novo):
        self.arestas[par] = novo

    def criaArestasResidual(self):
        adicionar = []
        for aresta in self.arestas.keys():
            if (aresta[1],aresta[0]) not in self.arestas.keys():
                adicionar.append((aresta[1],aresta[0]))
        for novo in adicionar:
            self.arestas[novo] = 0

    #QUESTAO 2

    def buscaEmLargura(self, s):
        c = {}
        for i in self.vertices.keys():
            c[i] = False

        d = {}
        for i in self.vertices.keys():
            d[i] = inf

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
        #Começa o algoritmo
        d = [inf] * (len(self.vertices)+1)

        a = [None] * (len(self.vertices)+1)

        d[s] = 0

        for _ in range(len(self.vertices)):
            for aresta in self.arestas.keys():
                aTupla = tuple(aresta)
                u = aTupla[0]
                v = aTupla[1]

                if  d[u] != inf and d[v] > (d[u] + self.arestas[aresta]):
                    d[v] = d[u] + self.arestas[aresta]
                    a[v] = u

                if  d[v] != inf and d[u] > (d[v] + self.arestas[aresta]):
                    d[u] = d[v] + self.arestas[aresta]
                    a[u] = v
            
        for aresta in self.arestas.keys():
            aTupla = tuple(aresta)
            v = aTupla[0]
            u = aTupla[1]

            if d[u] != inf and d[v] > d[u] + self.arestas[aresta]:
                return (False, [], [])

            if d[v] != inf and d[u] > d[v] + self.arestas[aresta]:
                return (False, [], [])

        d = d[1:]
        a = a[1:]
        return (True, d, a)

    #Questao 5

    def floydWarshall(self):
        W = [ [None] * (self.qtdVertices()) for _ in range(self.qtdVertices()) ]
        for u in range (self.qtdVertices()):
            for v in range (self.qtdVertices()):
                if u == v:
                    W[u][v] = 0
                elif frozenset((u+1,v+1)) in self.arestas.keys():
                    W[u][v] = self.arestas[frozenset((u+1,v+1))]
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

    #ATIVIDADE 2
    #Metodos auxiliares
    def entrantes(self, vertice):
        lista = []
        for arco in self.arestas.keys():
            if vertice == arco[1]:
                lista.append(arco[0])
        return lista
    
    def saintes (self,vertice):
        lista = []
        for arco in self.arestas.keys():
            if vertice == arco[0]:
                lista.append(arco[1])
        return lista

    #Questao 1
    def CFC(self):
        (C,T,Alinha, f) = self.DFS(self)
        At = {}
        for (u, v) in self.arestas.keys():
            At[v,u] = self.arestas[(u,v)]
        grafoT = Grafo(None, self.vertices, At)
        (Ct, Tt, Alinhat, Ft) = self.DFSadaptado(grafoT, f)
        return Alinhat

    def DFS(self, grafo):
        c = {}
        for v in grafo.vertices.keys():
            c[v] = False

        t = {}
        for v in grafo.vertices.keys():
            t[v] = inf

        f = {}
        for v in grafo.vertices.keys():
            f[v] = inf

        a = {}
        for v in grafo.vertices.keys():
            a[v] = None

        tempo = [0]

        for u in grafo.vertices.keys():
            if c[u] == False:
                self.DFSvisit(grafo, u, c, t, a, f, tempo)

        return (c, t, a, f)

    def DFSadaptado(self, grafo, f):
        c = {}
        for v in grafo.vertices.keys():
            c[v] = False

        t = {}
        for v in grafo.vertices.keys():
            t[v] = inf

        a = {}
        for v in grafo.vertices.keys():
            a[v] = None

        tempo = [0]

        fSorted = {}
        sorted_keys = reversed(sorted(f, key=f.get))
        for w in sorted_keys:
            fSorted[w] = f[w]
        #print(fSorted)

        for u in fSorted.keys():
            if c[u] == False:
                self.DFSvisit(grafo, u, c, t, a, f, tempo)

        return (c, t, a, f)

    def DFSvisit(self, grafo, v, c, t, a, f, tempo):
        c[v] = True
        tempo[0] += 1
        t[v] = tempo[0]
        for u in grafo.saintes(v):
            if c[u] == False:
                a[u] = v
                #print(a)
                self.DFSvisit(grafo, u, c, t, a, f, tempo)
        tempo[0] += 1
        f[v] = tempo[0]

    #Questao 2
    def OT(self):
        c = {}

        for v in self.vertices.keys():
            c[v] = False

        o = []
        for v in self.vertices.keys():
            #print("OT: " + str(v))
            if c[v] == False:
                self.visitOT(v, o, c)
        return o

    def visitOT(self, v, o, c):
        c[v] = True
        for u in self.saintes(v):
            #print(u)
            if c[u] == False:
                self.visitOT(u,o,c)
        o.insert(0, v)
        #print(o)

    #Questao 3
    def kruskal(self):
        a = []
        s = {}
        for v in self.vertices.keys():
            s[v] = {v}
        eLinha = dict(sorted(self.arestas.items(), key=lambda x : x[1]))
        for aresta in eLinha.keys():
            arestaTup = tuple(aresta)
            if s[arestaTup[0]] != s[arestaTup[1]]:
                a.append(aresta)
                x = s[arestaTup[0]].union(s[arestaTup[1]])
                for y in x:
                    s[y] = x
        return a

    #ATIVIDADE 3
    #Questao 1

    def edmondsKarp(self, s, t):
        residual = Grafo(None, self.vertices, self.arestas)
        residual.criaArestasResidual()
        f = 0
        p = residual.edmondsKarpBFS(s,t)
        while p != None:
            cfp = min(self.pesosCaminho(p))
            for u,v in self.paresCaminho(p):
                residual.mudaCustoResidual((u,v), residual.peso(u,v) - cfp)
                residual.mudaCustoResidual((v,u), residual.peso(v,u) - cfp)
            f += cfp
            p = residual.edmondsKarpBFS(s,t)
        return (f, residual)

    def edmondsKarpBFS(self, s, t):
        c = {}
        a = {}
        for v in self.vertices.keys():
            c[v] = False
            a[v] = None
        c[s] = True
        q = Queue()
        q.put(s)
        while q.empty() == False:
            u = q.get()
            for v in self.saintes(u):
                if c[v] == False and self.peso(u,v) > 0:
                    c[v] = True
                    a[v] = u
                    if v == t:
                        p = [t]
                        w = t
                        while w != s:
                            w = a[w]
                            p.insert(0, w)
                        return p
                    q.put(v)
        return None

    def pesosCaminho(self, p):
        pesos = []
        for i in range(1,len(p)):
            pesos.append(self.peso(p[i-1],p[i]))
        return pesos

    def paresCaminho(self,p):
        pares = []
        for i in range(1,len(p)):
            pares.append((p[i-1],p[i]))
        return pares

    #Questao 2
    def hopcroftKarp(self):
        xLista, yLista = self.particoes()
        d = {}
        mate = {}
        for v in self.vertices.keys():
            d[v] = inf
            mate[v] = None
        d[None] = inf #Dnull
        m = 0
        while self.hkBFS(mate, d, xLista) == True:
            for x in xLista:
                if mate[x] == None:
                    if self.hkDFS(mate, x, d) == True:
                        m += 1
        return (m, mate)
    
    def hkBFS(self, mate, d, xLista):
        q = Queue()
        for x in xLista:
            if mate[x] == None:
                d[x] = 0
                q.put(x)
            else:
                d[x] = inf
        d[None] = inf
        while q.empty() == False:
            x = q.get()
            if d[x] < d[None]:
                for y in self.vizinhos(x):
                    if d[mate[y]] == inf:
                        d[mate[y]] = d[x] + 1
                        q.put(mate[y])
        return d[None] != inf


    def hkDFS(self, mate, x, d):
        if x != None:
            for y in self.vizinhos(x):
                if d[mate[y]] == d[x] + 1:
                    if self.hkDFS(mate, mate[y], d) == True:
                        mate[y] == x
                        mate[x] == y
                        return True
            d[x] = inf
            return False
        return True


    def particoes(self):
        x = []
        y = []
        verts = list(self.vertices.keys())
        for i in range(len(verts)//2):
            x.append(verts[i])
        for i in range(len(verts)//2, len(verts)):
            y.append(verts[i])
        return (x, y)

    #Questao 3
    def lawler(self):
        x = [None for i in range (0, 2**len(self.vertices))]
        x[0] = 0
        a = [set(x) for x in self.powerset(self.vertices)]
        for sIndex, s in enumerate(a[1:]):
            sIndex += 1
            x[sIndex] = inf
            novosVertices, novasArestas = self.montaGrafo(s)
            gLinha = Grafo(None, novosVertices, novasArestas)
            for c in gLinha.conjIndMax():
                dif = s.difference(c)
                i = a.index(dif)
                if 1 + x[i] < x[sIndex]:
                    x[sIndex] = 1 + x[i]
        return x[-1]

    def conjIndMax(self):
        l = list(self.powerset(self.vertices))
        l.reverse()
        lRes = list(self.powerset(self.vertices))
        lRes.reverse()
        for s in l:
            if s not in lRes:
                continue
            pares = [frozenset(x) for x in combinations(s, 2)]
            existe = self.existeAresta(pares)
            if not existe:
                subs = list(self.powerset(s))
                mesmo = subs.pop(-1)
                for sub in subs:
                    if sub in lRes: lRes.remove(sub)
            else:
                lRes.remove(s)
        return [set(x) for x in lRes]

    def existeAresta(self, pares):
        for p in pares:
            if p in self.arestas.keys():
                return True
        return False

    def montaGrafo(self, s):
        novosVertices = {}
        novasArestas = {}
        for aresta, peso in self.arestas.items():
            aLista = list(aresta)
            if aLista[0] in s and aLista[1] in s:
                novasArestas[aresta] = peso

        for v in s:
            novosVertices[v] = self.vertices[v]
        return(novosVertices, novasArestas)

    #https://docs.python.org/3/library/itertools.html#itertools-recipes
    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
                
    #FUNCOES PARA PRINT/DEBUG
    def debugQ1A1(self):
        print("-----DEBUG-----")
        print(self.qtdVertices())
        print(self.qtdArestas())
        print(self.grau(52))
        print(self.rotulo(52))
        print(self.vizinhos(52))
        print(self.haAresta(52, 5))
        print(self.haAresta(52, 1))
        print(self.peso(52, 5))

    def debugQ1A2(self):
        print("-----DEBUG-----")
        print(self.qtdVertices())
        print(self.qtdArestas())
        print(self.grau(2))
        print(self.rotulo(2))
        print(self.vizinhos(2))
        print(self.haAresta(2, 3))
        print(self.haAresta(2, 7))
        print(self.haAresta(2, 8))
        print(self.peso(2, 7))
        print(self.entrantes(2))
        print(self.saintes(2))

    def debugQ1A3(self):
        print("-----DEBUG-----")
        print(self.qtdVertices())
        print(self.qtdArestas())
        print(self.grau(2))
        print(self.rotulo(2))
        print(self.vizinhos(2))
        print(self.haAresta(2, 4))
        print(self.haAresta(2, 6))
        print(self.haAresta(3, 2))
        print(self.peso(2, 4))
        print(self.entrantes(2))
        print(self.saintes(2))


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
        print("-----DEBUG.TXT ATUALIZADO-----")

    def printBusca(self, tupla):
        print("-----BUSCA EM LARGURA-----")
        n = max(list(tupla[0].values()))
        niveis = [ [] * (n+1) for i in range(n+1) ]
        for key, value in tupla[0].items():
            niveis[value].append(str(key))
        for i in range(n+1):
            nivel = str(i)
            verts = ','.join(niveis[i])
            print(nivel + ": " + verts)

    def printCiclo(self, tupla):
        print("-----CICLO EULERIANO-----")
        (r, ciclo) = tupla
        print(r)
        print(ciclo)

    def printBellmanFord(self, tupla):
        print("-----BELLMAN-FORD-----")
        (res, d, a) = tupla
        print(res)
        print(d)
        print(a)

    def printFloydWarshall(self, matriz):
        print("-----FLOYD-WARSHALL-----")
        for index, lista in enumerate(matriz):
            strInts = ','.join(str(n) for n in lista)
            print(str(index+1) + ":" + strInts)

    def printCFC(self, arv):
        print("-----COMPONENTES FORTEMENTE CONEXAS-----")
        comps = []
        while len(arv) > 0:
            for key, value in arv.items():
                if value == None:
                    comps.append([key])
                    arv.pop(key)
                    break
                else:
                    if self.checaSublistas(comps, value, key, arv):
                        break
        
        for sub in comps:
            if len(sub) > 1:
                print(','.join(str(v) for v in sub))

    def checaSublistas(self, comps, value, key, arv):
        for sub in comps:
            if value in sub:
                sub.append(key)
                arv.pop(key)
                return True
        return False

    def printOT(self, o):
        print("-----ORDENACAO TOPOLOGICA-----")
        #print(o)
        l = []
        for v in o:
            l.append(self.rotulo(v).strip('"'))
        print(' -> '.join(l))

    def printKruskal(self, a):
        print("-----KRUSKAL-----")
        soma = 0
        arestasPrint = []
        for aresta in a:
            soma += self.arestas[aresta]
            arestaTup = tuple(aresta)
            arestasPrint.append(str(arestaTup[0]) + "-" + str(arestaTup[1]))
        print(soma)
        print(', '.join(arestasPrint))

    def printEdmondsKarp(self, res):
        print(res[0])