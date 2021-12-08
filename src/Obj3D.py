from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image
from src import ObjLoad
import pyrr


# Carregando a textura no buffer de textura
def carregando_textura(caminho, textura, tipo_mapeamento=GL_DECAL):
    glBindTexture(GL_TEXTURE_2D, textura)
    # Setando a textura no objeto
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Setando a textura com os parametro de filtro para interpolacao pixel que dao sensacao ruidosa
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)   
    # Carregando a imagem de textura
    image = Image.open(caminho)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    #converter para formato de bytes
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    
    return textura

def exibir_objeto(localizacao_do_modelo, vao, textura, indices, posicao_obj, modo_exibicao):
    glBindVertexArray(vao)
    glBindTexture(GL_TEXTURE_2D, textura)
    glUniformMatrix4fv(localizacao_do_modelo, 1, GL_FALSE, posicao_obj)
    #exibir na tela com o modo de exibicao, de onde comeca os vertices e o numero de vertices
    glDrawArrays(modo_exibicao, 0, len(indices))

def alocar_buffers(buffer):
    # Alocando buffers
    vertice_array = glGenVertexArrays(1)
    vertice_buffer = glGenBuffers(1)
    textura = glGenTextures(1)

    # Linkando buffers
    glBindVertexArray(vertice_array)
    glBindBuffer(GL_ARRAY_BUFFER, vertice_buffer)
    #coloca de fato os dados no buffer
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # vertices 
    #o arguemnto passado é o layout location no arquivo do vertex shader 
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))
    # texturas
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))
    # normais
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    return vertice_array, vertice_buffer, textura

def carregar_objeto(caminho_obj, caminho_textura, posicao=[0, 0, 0], tipo_textura=GL_DECAL):
    indices, buffer = ObjLoad.ObjLoad.load_model(caminho_obj)
    
    vao, vbo, textura = alocar_buffers(buffer)
    textura = carregando_textura(caminho_textura, textura, tipo_textura)

    posicao = pyrr.matrix44.create_from_translation(pyrr.Vector3(posicao))

    #VBO =  VERTEX BUFFER OBJECT, buffer de vertice do objeto
    #VAO = VERTEX ARRAY OBJECT, array de vertice do objeto

    return vao, vbo, textura, indices, posicao