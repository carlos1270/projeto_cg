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
        #glfw.set_window_size_callback(self.janela, self.reajustando_janela)

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
        
        # Carregando cenario e animais 
        self.vao_cenario, self.vbo_cenario, self.textura_cenario, self.indices_cenario, self.posicao_cenario = Obj3D.carregar_objeto("objetos/cenario/cenario.obj", "objetos/cenario/cenario.png", [0, 0, 0])
        
        #elefante
        self.vao_elefante, self.vbo_elefante, self.textura_elefante, self.indices_elefante, self.posicao_elefante = Obj3D.carregar_objeto("objetos/elefante/elefante.obj", "objetos/elefante/elefante.png", [-55, -28.5, 4])
        self.vao_elefante_cerca, self.vbo_elefante_cerca, self.textura_elefante_cerca, self.indices_elefante_cerca, self.posicao_elefante_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [-46.3, -28.5, 0])

        #avestruz
        self.vao_avestruz, self.vbo_avestruz, self.textura_avestruz, self.indices_avestruz, self.posicao_avestruz = Obj3D.carregar_objeto("objetos/avestruz/avestruz.obj", "objetos/girafa/Textures.png", [-46, -24.2, 109])
        self.vao_avestruz_cerca, self.vbo_avestruz_cerca, self.textura_avestruz_cerca, self.indices_avestruz_cerca, self.posicao_avestruz_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [-43, -28.2, 101])

        #veado
        self.vao_veado, self.vbo_veado, self.textura_veado, self.indices_veado, self.posicao_veado = Obj3D.carregar_objeto("objetos/veado/veado.obj", "objetos/girafa/Textures.png", [-98, -29.44, 5])
        self.vao_veado_cerca, self.vbo_veado_cerca, self.textura_veado_cerca, self.indices_veado_cerca, self.posicao_veado_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [-88, -29.44, -3])

        #rino
        self.vao_rino, self.vbo_rino, self.textura_rino, self.indices_rino, self.posicao_rino = Obj3D.carregar_objeto("objetos/rino/rino.obj", "objetos/girafa/Textures.png", [0, -26, 84])
        self.vao_rino_cerca, self.vbo_rino_cerca, self.textura_rino_cerca, self.indices_rino_cerca, self.posicao_rino_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [20, -29.4, 84])

        #panda
        self.vao_panda, self.vbo_panda, self.textura_panda, self.indices_panda, self.posicao_panda = Obj3D.carregar_objeto("objetos/panda/panda.obj", "objetos/panda/panda.png", [6, -23, -11])
        self.vao_panda_cerca, self.vbo_panda_cerca, self.textura_panda_cerca, self.indices_panda_cerca, self.posicao_panda_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [27, -29.7, -25])

        #tigre
        self.vao_tigre, self.vbo_tigre, self.textura_tigre, self.indices_tigre, self.posicao_tigre = Obj3D.carregar_objeto("objetos/tigre/tigre.obj", "objetos/tigre/tigercolor.png", [-12, -28.2, 150])
        self.vao_tigre_cerca, self.vbo_tigre_cerca, self.textura_tigre_cerca, self.indices_tigre_cerca, self.posicao_tigre_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [-5, -28.2, 150])

        #girafa
        self.vao_girafa, self.vbo_girafa, self.textura_girafa, self.indices_girafa, self.posicao_girafa = Obj3D.carregar_objeto("objetos/girafa/girafa.obj", "objetos/girafa/Textures.png", [70, -29, 72])
        self.vao_girafa_cerca, self.vbo_girafa_cerca, self.textura_girafa_cerca, self.indices_girafa_cerca, self.posicao_girafa_cerca = Obj3D.carregar_objeto("objetos/cerca/cerca.obj", "objetos/cerca/cerca.png", [85, -28.2, 52])

        # Carregando placas dos animais
        self.vao_p_elefante, self.vbo_p_elefante, self.textura_p_elefante, self.indices_p_elefante, self.posicao_p_elefante = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-elefante.png", [-37, -29, -2])
        self.vao_p_avestruz, self.vbo_p_avestruz, self.textura_p_avestruz, self.indices_p_avestruz, self.posicao_p_avestruz = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-avestruz.png", [-35, -28.8, 109])
        self.vao_p_rino, self.vbo_p_rino, self.textura_p_rino, self.indices_p_rino, self.posicao_p_rino = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-rinoceronte.png", [0, -29.5, 61])
        self.vao_p_veado, self.vbo_p_veado, self.textura_p_veado, self.indices_p_veado, self.posicao_p_veado = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-veado.png", [-80, -29, 5])
        self.vao_p_panda, self.vbo_p_panda, self.textura_p_panda, self.indices_p_panda, self.posicao_p_panda = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-panda.png", [0, -28.8, 50])
        self.vao_p_tigre, self.vbo_p_tigre, self.textura_p_tigre, self.indices_p_tigre, self.posicao_p_tigre = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-tigre.png", [-10, -28.9, 140])
        self.vao_p_girafa, self.vbo_p_girafa, self.textura_p_girafa, self.indices_p_girafa, self.posicao_p_girafa = Obj3D.carregar_objeto("objetos/placas/placa.obj", "objetos/placas/placa-girafa.png", [45, -29, 72])

        #Girando placas
        rot_y = pyrr.Matrix44.from_y_rotation(1.4)
        self.posicao_p_elefante = pyrr.matrix44.multiply(rot_y, self.posicao_p_elefante)
        self.posicao_p_avestruz = pyrr.matrix44.multiply(rot_y, self.posicao_p_avestruz)
        self.posicao_p_veado = pyrr.matrix44.multiply(rot_y, self.posicao_p_veado)
        rot_y = pyrr.Matrix44.from_y_rotation(3.4)
        self.posicao_p_panda = pyrr.matrix44.multiply(rot_y, self.posicao_p_panda)
        rot_y = pyrr.Matrix44.from_y_rotation(-1.8)
        self.posicao_p_girafa = pyrr.matrix44.multiply(rot_y, self.posicao_p_girafa)

        self.scale = pyrr.Matrix44.from_scale(pyrr.Vector3([200, 200, 200]))
        
        # Definindo posição da camera, parametros: pos_do_olho, direção_da_camera, vertor_up
        visualizacao = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, -85]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

        self.localizacao_modelo = glGetUniformLocation(shader, "modelo")
        self.localizacao_projecao = glGetUniformLocation(shader, "projecao")
        self.localizacao_visualizacao = glGetUniformLocation(shader, "visualizacao")

        glUniformMatrix4fv(self.localizacao_projecao, 1, GL_FALSE, projecao)
        glUniformMatrix4fv(self.localizacao_visualizacao, 1, GL_FALSE, visualizacao)

        self.posicao_cube_scale = pyrr.matrix44.multiply(self.scale, self.posicao_cube)

        #avestruz
        self.posicao_avestruz_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([0.25, 0.25, 0.25])), self.posicao_avestruz)
        self.posicao_avestruz_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([1.0, 2.0, 1.0])), self.posicao_avestruz_cerca)

        #veado
        self.posicao_veado_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([0.25, 0.25, 0.25])), self.posicao_veado)
        self.posicao_veado_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([1.0, 1.0, 1.0])), self.posicao_veado_cerca)

        #elefante
        self.posicao_elefante_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([1.2, 1.6, 1.5])), self.posicao_elefante_cerca)

        #rino
        self.posicao_rino_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([0.25, 0.25, 0.25])), self.posicao_rino)
        self.posicao_rino_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([2.0, 1.6, 2.0])), self.posicao_rino_cerca)

        #panda
        self.posicao_panda_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([0.5, 0.5, 0.5])), self.posicao_panda)
        self.posicao_panda_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([2.0, 2.0, 2.0])), self.posicao_panda_cerca)

        #tigre
        self.posicao_tigre_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([2.0, 2.0, 2.0])), self.posicao_tigre)

        #girafa
        self.posicao_girafa_scale = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([0.25, 0.25, 0.25])), self.posicao_girafa)
        self.posicao_girafa_cerca = pyrr.matrix44.multiply(pyrr.Matrix44.from_scale(pyrr.Vector3([2.0, 2.0, 2.0])), self.posicao_girafa_cerca)



    def main_loop(self):
        #enquanto a janela não for fechada
        while not glfw.window_should_close(self.janela):
            #receba os eventos do teclado
            glfw.poll_events()

            self.nav.do_movement()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = self.cam.get_view_matrix()
            glUniformMatrix4fv(self.localizacao_visualizacao, 1, GL_FALSE, view)

            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_cube, self.textura_cube, self.indices_cube, self.posicao_cube_scale, GL_TRIANGLES)
            
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_cenario, self.textura_cenario, self.indices_cenario, self.posicao_cenario, GL_TRIANGLES)

            #elefante
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_elefante, self.textura_elefante, self.indices_elefante, self.posicao_elefante, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_elefante_cerca, self.textura_elefante_cerca, self.indices_elefante_cerca, self.posicao_elefante_cerca, GL_QUADS)

            #avestruz
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_avestruz, self.textura_avestruz, self.indices_avestruz, self.posicao_avestruz_scale, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_avestruz_cerca, self.textura_avestruz_cerca, self.indices_avestruz_cerca, self.posicao_avestruz_cerca, GL_QUADS)

            #veado
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_veado, self.textura_veado, self.indices_veado, self.posicao_veado_scale, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_veado_cerca, self.textura_veado_cerca, self.indices_veado_cerca, self.posicao_veado_cerca, GL_QUADS)

            #rino
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_rino, self.textura_rino, self.indices_rino, self.posicao_rino_scale, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_rino_cerca, self.textura_rino_cerca, self.indices_rino_cerca, self.posicao_rino_cerca, GL_QUADS)

            
            #panda
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_panda, self.textura_panda, self.indices_panda, self.posicao_panda_scale, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_panda_cerca, self.textura_panda_cerca, self.indices_panda_cerca, self.posicao_panda_cerca, GL_QUADS)

            #tigre
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_tigre, self.textura_tigre, self.indices_tigre, self.posicao_tigre_scale, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_tigre_cerca, self.textura_tigre_cerca, self.indices_tigre_cerca, self.posicao_tigre_cerca, GL_QUADS)

            #girafa
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_girafa, self.textura_girafa, self.indices_girafa, self.posicao_girafa_scale, GL_TRIANGLES)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_girafa_cerca, self.textura_girafa_cerca, self.indices_girafa_cerca, self.posicao_girafa_cerca, GL_QUADS)

            #placas
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_elefante, self.textura_p_elefante, self.indices_p_elefante, self.posicao_p_elefante, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_avestruz, self.textura_p_avestruz, self.indices_p_avestruz, self.posicao_p_avestruz, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_rino, self.textura_p_rino, self.indices_p_rino, self.posicao_p_rino, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_veado, self.textura_p_veado, self.indices_p_veado, self.posicao_p_veado, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_panda, self.textura_p_panda, self.indices_p_panda, self.posicao_p_panda, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_tigre, self.textura_p_tigre, self.indices_p_tigre, self.posicao_p_tigre, GL_QUADS)
            Obj3D.exibir_objeto(self.localizacao_modelo, self.vao_p_girafa, self.textura_p_girafa, self.indices_p_girafa, self.posicao_p_girafa, GL_QUADS)

            glfw.swap_buffers(self.janela)
        #finaliza  janela
        glfw.terminate()
        
    # glfw callback função
    def reajustando_janela(self, window, largura, altura):
        glViewport(0, 0, largura, altura)
        projecao = pyrr.matrix44.create_perspective_projection_matrix(45, largura / altura, 0.1, 100)
        glUniformMatrix4fv(self.localizacao_projecao, 1, GL_FALSE, projecao)