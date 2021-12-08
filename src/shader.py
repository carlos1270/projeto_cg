from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

'''Um Fragment Shader é o estágio de Shader que processará um Fragment gerado pela Rasterização
 em um conjunto de cores e um único valor de profundidade.
O  Fragment Shader é o estágio de pipeline do OpenGL depois que uma primitiva é rasterizada. 
Para cada amostra dos pixels cobertos por uma primitiva, um "fragmento" é gerado. 
Cada fragmento tem uma posição Window Space, alguns outros valores e contém todos os valores de 
saída por vértice interpolados do último estágio de Processamento de Vértices.'''


def createShader(vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        #criar um shader e compilar vertex e fragment
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader