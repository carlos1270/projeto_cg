from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    def __init__(self):
        self.posicao_camera = Vector3([0.0, 0.0, 8.0])
        self.direcao_apontando = Vector3([0.0, 0.0, -1.0])
        self.vetor_up = Vector3([0.0, 1.0, 0.0])
        self.direita_camera = Vector3([1.0, 0.0, 0.0])

        self.sensibilidade_do_mouse = 0.25
        self.jaw = -90
        self.pitch = 0

    def get_janela_visualizacao(self):
        return matrix44.create_look_at(self.posicao_camera, self.posicao_camera + self.direcao_apontando, self.vetor_up)

    def processar_movimento_mouse(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensibilidade_do_mouse
        yoffset *= self.sensibilidade_do_mouse

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.update_vetores_camera()

    def update_vetores_camera(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.direcao_apontando = vector.normalise(front)
        self.direita_camera = vector.normalise(vector3.cross(self.direcao_apontando, Vector3([0.0, 1.0, 0.0])))
        self.vetor_up = vector.normalise(vector3.cross(self.direita_camera, self.direcao_apontando))

    # Camera method for the WASD movement
    def processar_teclas(self, direction, velocity):
        if direction == "FORWARD":
            self.posicao_camera += self.direcao_apontando * velocity
        if direction == "BACKWARD":
            self.posicao_camera -= self.direcao_apontando * velocity
        if direction == "LEFT":
            self.posicao_camera -= self.direita_camera * velocity
        if direction == "RIGHT":
            self.posicao_camera += self.direita_camera * velocity
















