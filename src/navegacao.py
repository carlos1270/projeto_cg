import glfw

class Navegacao:
    def __init__(self, cam, left, right, forward, backward, first_mouse, lastX, lastY):
        self.cam = cam
        self.esquerda = left
        self.direita = right
        self.frente = forward
        self.tras = backward
        self.first_mouse = first_mouse
        self.lastX = lastX
        self.lastY = lastY

    # Função de callback de captura do teclado
    def key_input_clb(self, window, key, scancode, action, mode):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if key == glfw.KEY_W and action == glfw.PRESS:
            self.frente = True
        elif key == glfw.KEY_W and action == glfw.RELEASE:
            self.frente = False
        if key == glfw.KEY_S and action == glfw.PRESS:
            self.tras = True
        elif key == glfw.KEY_S and action == glfw.RELEASE:
            self.tras = False
        if key == glfw.KEY_A and action == glfw.PRESS:
            self.esquerda = True
        elif key == glfw.KEY_A and action == glfw.RELEASE:
            self.esquerda = False
        if key == glfw.KEY_D and action == glfw.PRESS:
            self.direita = True
        elif key == glfw.KEY_D and action == glfw.RELEASE:
            self.direita = False


    # Função que detecta o movimento da camera
    def do_movement(self):
        if self.esquerda:
            self.cam.process_keyboard("LEFT", 0.05)
        if self.direita:
            self.cam.process_keyboard("RIGHT", 0.05)
        if self.frente:
            self.cam.process_keyboard("FORWARD", 0.05)
        if self.tras:
            self.cam.process_keyboard("BACKWARD", 0.05)


    # Função de callback de captura do mouse
    def mouse_look_clb(self, window, xpos, ypos):
        if self.first_mouse:
            self.lastX = xpos
            self.lastY = ypos
            self.first_mouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        self.cam.process_mouse_movement(xoffset, yoffset)
