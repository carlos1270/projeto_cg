from OpenGL.GL import *
from OpenGL.GL.shaders import *
from PIL import Image
from ObjLoad import ObjLoad
import pyrr


# Carregando a textura no buffer de textura
def carregando_textura(caminho, texture):
    glBindTexture(GL_TEXTURE_2D, texture)

    # Setando a textura no objeto
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    # Setando a textura com os parametro de filtro
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Carregando a imagem de textura
    image = Image.open(caminho)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    
    return texture

def exibir_objeto(localizacao_do_modelo, vao, textura, indices, posicao_obj):
    glBindVertexArray(vao)
    glBindTexture(GL_TEXTURE_2D, textura)
    glUniformMatrix4fv(localizacao_do_modelo, 1, GL_FALSE, posicao_obj)
    glDrawArrays(GL_TRIANGLES, 0, len(indices))

def alocar_buffers(buffer):
    # Alocando buffers
    vertex_array_obj = glGenVertexArrays(1)
    vertex_buffer_obj = glGenBuffers(1)
    textura = glGenTextures(1)

    # Linkando buffers
    glBindVertexArray(vertex_array_obj)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_obj)
    glBufferData(GL_ARRAY_BUFFER, buffer.nbytes, buffer, GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(0))
    # texturas
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(12))
    # normais
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    return vertex_array_obj, vertex_buffer_obj, textura

def carregar_objeto(caminho_obj, caminho_textura, posicao=[0, 0, 0]):
    indices, buffer = ObjLoad.load_model(caminho_obj)
    
    vao, vbo, textura = alocar_buffers(buffer)
    carregando_textura(caminho_textura, textura)

    posicao = pyrr.matrix44.create_from_translation(pyrr.Vector3(posicao))

    return vao, vbo, textura, indices, posicao