from src import Obj3D
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import glfw

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
glfw.set_window_pos(janela, 400, 200)

# Setando a função que reajusta o tamanho da janela
glfw.set_window_size_callback(janela, reajustando_janela)

# Construindo o contexto atual
glfw.make_context_current(janela)

# Compilando o programa de shadder auxiliar
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Adicionando o programa de shadder
glUseProgram(shader)
glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Definindo a projeção como perspectiva de acordo com o tamanho da janela
projecao = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 150)

# Definindo posição da camera, parametros: pos_do_olho, direção_da_camera, vertor_up
visualizacao = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, -85]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

localizacao_modelo = glGetUniformLocation(shader, "modelo")
localizacao_projecao = glGetUniformLocation(shader, "projecao")
localizacao_visualizacao = glGetUniformLocation(shader, "visualizacao")

glUniformMatrix4fv(localizacao_projecao, 1, GL_FALSE, projecao)
glUniformMatrix4fv(localizacao_visualizacao, 1, GL_FALSE, visualizacao)

vao_arvore, vbo_arvore, textura_arvore, indices_arvore, posicao_arvore = Obj3D.carregar_objeto("objetos/grass/10450_Rectangular_Grass_Patch_v1_iterations-2.obj", "objetos/grass/10450_Rectangular_Grass_Patch_v1_Diffuse.jpg", [0, 0, 0])

scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

# Main loop da aplicação
while not glfw.window_should_close(janela):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    multi = pyrr.matrix44.multiply(scale, rot_y)
    model = pyrr.matrix44.multiply(multi, posicao_arvore)

    Obj3D.exibir_objeto(localizacao_modelo, vao_arvore, textura_arvore, indices_arvore, model, modo_exibicao=GL_POLYGON)

    glfw.swap_buffers(janela)

# Termina o processo glfw e desaloca todos os recursos
glfw.terminate()