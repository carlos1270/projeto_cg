from src import Obj3D
from src import camera
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import glfw
import numpy as np
from PIL import Image

cam = camera.Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False


# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False


# do the movement, call this function in the main loop
def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)


# the mouse position callback function
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def createShader(vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader

class CubeMapMaterial:
    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #load textures
        image = Image.open(f"{filepath}_left.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        image = Image.open(f"{filepath}_right.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        image = Image.open(f"{filepath}_top.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        image = Image.open(f"{filepath}_bottom.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        image = Image.open(f"{filepath}_back.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

        image = Image.open(f"{filepath}_front.png")
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    
    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP,self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))

class CubeMapModel:
    def __init__(self, shader, l, w, h, r, g, b, material):
        self.material = material
        self.shader = shader
        glUseProgram(shader)
        # x, y, z, r, g, b
        self.vertices = (
                -l/2, -w/2, -h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b,

                 l/2,  w/2, -h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,

                 l/2,  w/2,  h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,

                -l/2, -w/2,  h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,

                -l/2, -w/2,  h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,

                -l/2,  w/2, -h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,

                 l/2, -w/2, -h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,

                 l/2,  w/2,  h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,

                 l/2, -w/2,  h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,

                -l/2, -w/2, -h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,

                 l/2,  w/2, -h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,

                -l/2,  w/2,  h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b
            )
        self.vertex_count = len(self.vertices)//6
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def draw(self, position):
        glUseProgram(self.shader)
        self.material.use()
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(model_transform, pyrr.matrix44.create_from_translation(vec=position,dtype=np.float32))
        glUniformMatrix4fv(glGetUniformLocation(self.shader,"model"),1,GL_FALSE,model_transform)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
class skyBox:
    def __init__(self, model):
        self.model = model

    def draw(self,position):
        self.model.draw(position)

    def destroy(self):
        self.model.destroy()

vertex_src = """
# version 330

layout(location = 0) in vec3 a_posicao;
layout(location = 1) in vec2 a_textura;
layout(location = 2) in vec3 a_normal;

uniform mat4 modelo;
uniform mat4 projecao;
uniform mat4 visualizacao;

out vec2 v_texture;

void main()
{
    gl_Position = projecao * visualizacao * modelo * vec4(a_posicao, 1.0);
    v_texture = a_textura;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

# glfw callback função
def reajustando_janela(window, largura, altura):
    glViewport(0, 0, largura, altura)
    projecao = pyrr.matrix44.create_perspective_projection_matrix(45, largura / altura, 0.1, 100)
    glUniformMatrix4fv(localizacao_projecao, 1, GL_FALSE, projecao)

# Inicializando biblioteca glfw
if not glfw.init():
    raise Exception("Glfw não pode ser inicializada!")

# Criando a janela
janela = glfw.create_window(1280, 720, "Minha janela OpenGL", None, None)

# Chegando se a janela foi criada
if not janela:
    glfw.terminate()
    raise Exception("Janela glfw não pode ser criada!")

# Setando a posicação da janela
monitor = glfw.get_primary_monitor()
pos = glfw.get_monitor_pos(monitor)
tamanho = glfw.get_window_size(janela)
modo = glfw.get_video_mode(monitor)
glfw.set_window_pos(
    janela,
    int(pos[0] + (modo.size.width - tamanho[0]) / 2),
    int(pos[1] + (modo.size.height - tamanho[1]) / 2))

# Setando a função que reajusta o tamanho da janela
glfw.set_window_size_callback(janela, reajustando_janela)

# set the mouse position callback
glfw.set_cursor_pos_callback(janela, mouse_look_clb)
# set the keyboard input callback
glfw.set_key_callback(janela, key_input_clb)
# capture the mouse cursor
glfw.set_input_mode(janela, glfw.CURSOR, glfw.CURSOR_DISABLED)

# Construindo o contexto atual
glfw.make_context_current(janela)

# Compilando o programa de shadder auxiliar
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
shader3DCubemap = createShader("shaders/vertex_3d_cubemap.txt",
                                        "shaders/fragment_3d_cubemap.txt")


# Adicionando o programa de shadder
glUseProgram(shader)
glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Definindo a projeção como perspectiva de acordo com o tamanho da janela
projecao = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 400)

glUseProgram(shader3DCubemap)
glUniformMatrix4fv(glGetUniformLocation(shader3DCubemap,"projecao"),1,GL_FALSE,projecao)
glUniform1i(glGetUniformLocation(shader3DCubemap, "skyBox"), 0)

# Definindo posição da camera, parametros: pos_do_olho, direção_da_camera, vertor_up
visualizacao = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, -85]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

localizacao_modelo = glGetUniformLocation(shader, "modelo")
localizacao_projecao = glGetUniformLocation(shader, "projecao")
localizacao_visualizacao = glGetUniformLocation(shader, "visualizacao")

glUniformMatrix4fv(localizacao_projecao, 1, GL_FALSE, projecao)
glUniformMatrix4fv(localizacao_visualizacao, 1, GL_FALSE, visualizacao)

vao_arvore, vbo_arvore, textura_arvore, indices_arvore, posicao_arvore = Obj3D.carregar_objeto("objetos/grama lowpoly/grass.obj", "objetos/grama lowpoly/depositphotos_79228002-stock-illustration-shades-of-green-abstract-polygonal.jpg", [0, 0, 0])
skyBoxTexture = CubeMapMaterial("objetos/ground/sky")
skyBoxModel = CubeMapModel(shader3DCubemap, 200,200,200,1,1,1, skyBoxTexture)
skyBox = skyBox(skyBoxModel)

scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

# Main loop da aplicação
while not glfw.window_should_close(janela):
    glfw.poll_events()

    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    skyBox.draw(np.array([0,0,1.2],dtype=np.float32))
    glEnable(GL_CULL_FACE)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(localizacao_visualizacao, 1, GL_FALSE, view)

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    multi = pyrr.matrix44.multiply(scale, rot_y)
    model = pyrr.matrix44.multiply(rot_y, posicao_arvore)

    Obj3D.exibir_objeto(localizacao_modelo, vao_arvore, textura_arvore, indices_arvore, posicao_arvore)

    glfw.swap_buffers(janela)

# Termina o processo glfw e desaloca todos os recursos
glfw.terminate()