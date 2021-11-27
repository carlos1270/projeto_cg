from src import Obj3D
from src import camera
from src import skybox
from src import navegacao
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import glfw
import numpy as np

class App:
    def __init__(self, width:int, height:int, titulo:str):
        #inicializar a bilbioteca
        if not glfw.init():
            raise Exception("glfw nao pode ser inicializado!")

        #cria a janela
        #penultima nulo pra modo full screen e a ultima pra compartilhar recursos
        self.janela = glfw.create_window(width, height, titulo, None, None)
        #camera
        self.cam = camera.Camera()
        lastX, lastY = width / 2, height / 2
        first_mouse = True
        left, right, forward, backward = False, False, False, False
        #navegacao
        self.nav = navegacao.Navegacao(self.cam, left, right, forward, backward, first_mouse, lastX, lastY)

        #se nao criou entao termina e avisa
        if not self.janela:
            glfw.terminate()
            raise Exception("a janela não pode ser criada!")

        #caso contrario posiciona a janela
        monitor = glfw.get_primary_monitor()
        pos = glfw.get_monitor_pos(monitor)
        tamanho = glfw.get_window_size(self.janela)
        modo = glfw.get_video_mode(monitor)
        glfw.set_window_pos(
            self.janela,
            int(pos[0] + (modo.size.width - tamanho[0]) / 2),
            int(pos[1] + (modo.size.height - tamanho[1]) / 2))

        #fazer o conteudo ser o da janela 
        # Setando a função que reajusta o tamanho da janela
        glfw.set_window_size_callback(self.janela, self.reajustando_janela)

        # set the mouse position callback
        glfw.set_cursor_pos_callback(self.janela, self.nav.mouse_look_clb)
        # set the keyboard input callback
        glfw.set_key_callback(self.janela, self.nav.key_input_clb)
        # capture the mouse cursor
        glfw.set_input_mode(self.janela, glfw.CURSOR, glfw.CURSOR_DISABLED)

        # Construindo o contexto atual
        glfw.make_context_current(self.janela)

        # Compilando o programa de shadder auxiliar
        shader = skybox.createShader("shaders/vertex_3d.txt",
                                                "shaders/fragment_3d.txt")

        # Adicionando o programa de shadder
        glUseProgram(shader)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Definindo a projeção como perspectiva de acordo com o tamanho da janela
        projecao = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 600)

        #self.skyBox, shader3DCubemap = skybox.carregar_objeto("objetos/ground/sky")
        self.vao_cube, self.vbo_cube, self.textura_cube, self.indices_cube, self.posicao_cube = Obj3D.carregar_objeto("objetos/cube/cube.obj", "objetos/cube/cube_sky.jpg", [0, 0, 0])
        
        self.vao_cenario, self.vbo_cenario, self.textura_cenario, self.indices_cenario, self.posicao_cenario = Obj3D.carregar_objeto("objetos/cenario/cenario.obj", "objetos/cenario/cenario.png", [0, 0, 0])

        self.scale = pyrr.Matrix44.from_scale(pyrr.Vector3([200, 200, 200]))

        # Definindo posição da camera, parametros: pos_do_olho, direção_da_camera, vertor_up
        visualizacao = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, -85]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

        self.localizacao_modelo = glGetUniformLocation(shader, "modelo")
        self.localizacao_projecao = glGetUniformLocation(shader, "projecao")
        self.localizacao_visualizacao = glGetUniformLocation(shader, "visualizacao")

        glUniformMatrix4fv(self.localizacao_projecao, 1, GL_FALSE, projecao)
        glUniformMatrix4fv(self.localizacao_visualizacao, 1, GL_FALSE, visualizacao)



    def main_loop(self):
        #enquanto a janela não for fechada
        while not glfw.window_should_close(self.janela):
            #receba os eventos do teclado
            glfw.poll_events()

            self.nav.do_movement()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = self.cam.get_view_matrix()
            glUniformMatrix4fv(self.localizacao_visualizacao, 1, GL_FALSE, view)

            rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
            multi = pyrr.matrix44.multiply(self.scale, rot_y)

            posicao_cube_scale = pyrr.matrix44.multiply(self.scale, self.posicao_cube)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_cube, self.textura_cube, self.indices_cube, posicao_cube_scale, GL_TRIANGLES)

            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_cenario, self.textura_cenario, self.indices_cenario, self.posicao_cenario, GL_TRIANGLES)


            glfw.swap_buffers(self.janela)
        #finaliza  janela
        glfw.terminate()
        
    # glfw callback função
    def reajustando_janela(self, window, largura, altura):
        glViewport(0, 0, largura, altura)
        projecao = pyrr.matrix44.create_perspective_projection_matrix(45, largura / altura, 0.1, 100)
        glUniformMatrix4fv(self.localizacao_projecao, 1, GL_FALSE, projecao)