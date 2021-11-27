from Obj3D import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from Camera import Camera
import pyrr
import glfw

cam = Camera()
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
        cam.processar_teclas("LEFT", 0.05)
    if right:
        cam.processar_teclas("RIGHT", 0.05)
    if forward:
        cam.processar_teclas("FORWARD", 0.05)
    if backward:
        cam.processar_teclas("BACKWARD", 0.05)

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

    cam.processar_movimento_mouse(xoffset, yoffset)

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

# Adicionando o programa de shadder
glUseProgram(shader)
glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Definindo a projeção como perspectiva de acordo com o tamanho da janela
projecao = pyrr.matrix44.create_perspective_projection_matrix(5000, 1280 / 720, 0.1, 10000)

# Definindo posição da camera, parametros: pos_do_olho, direção_da_camera, vertor_up
visualizacao = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 8]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

localizacao_modelo = glGetUniformLocation(shader, "modelo")
localizacao_projecao = glGetUniformLocation(shader, "projecao")
localizacao_visualizacao = glGetUniformLocation(shader, "visualizacao")

glUniformMatrix4fv(localizacao_projecao, 1, GL_FALSE, projecao)
glUniformMatrix4fv(localizacao_visualizacao, 1, GL_FALSE, visualizacao)

vao_macaco, vbo_macaco, textura_macaco, indices_macaco, posicao_macaco = carregar_objeto("samples/objetos/macaco/monkey.obj", "samples/objetos/macaco/monkey.jpg", [-4, 0, 0])
vao_chibi, vbo_chibi, textura_chibi, indices_chibe, posicao_chibe = carregar_objeto("samples/objetos/chibi/chibi.obj", "samples/objetos/chibi/chibi.png", [0, -5, -10])
vao_cube, vbo_cube, textura_cube, indices_cube, posicao_cube = carregar_objeto("samples/objetos/cube/cube.obj", "samples/objetos/cube/cube.jpg", [0, 0, 0])

scale = pyrr.Matrix44.from_scale(pyrr.Vector3([30, 30, 30]))

# Main loop da aplicação
while not glfw.window_should_close(janela):
    glfw.poll_events()
    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_janela_visualizacao()
    glUniformMatrix4fv(localizacao_visualizacao, 1, GL_FALSE, view)

    exibir_objeto(localizacao_modelo, vao_macaco, textura_macaco, indices_macaco, posicao_macaco)

    exibir_objeto(localizacao_modelo, vao_chibi, textura_chibi, indices_chibe, posicao_chibe)

    posicao_cube_scale = pyrr.matrix44.multiply(scale, posicao_cube)
    exibir_objeto(localizacao_modelo, vao_cube, textura_cube, indices_cube, posicao_cube_scale)

    glfw.swap_buffers(janela)

# Termina o processo glfw e desaloca todos os recursos
glfw.terminate()