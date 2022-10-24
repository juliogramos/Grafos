from grafo import Grafo

#Teste de grafos dirigidos com funcoes auxiliares
grafo1 = Grafo('dirigido1.net', None, None)
#Esse metodo imprime para o arquivo debug.txt
#grafo1.debugDics()
#Esse imprime no terminal
#grafo1.debugQ1A2()

#Questao 1
print(grafo1.CFC())