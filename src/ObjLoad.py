
import numpy as np

class ObjLoad:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1)


    @staticmethod # Ordena os vetores, textura e normais de acordo com as ordens da face
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: # Ordena a coordenada do vetor
                start = ind * 3
                end = start + 3
                ObjLoad.buffer.extend(vertices[start:end])
            elif i % 3 == 1: # Ordena a coordenada da textura
                start = ind * 2
                end = start + 2
                ObjLoad.buffer.extend(textures[start:end])
            elif i % 3 == 2: # Ordena a coordenada do vetor normal
                start = ind * 3
                end = start + 3
                ObjLoad.buffer.extend(normals[start:end])

    @staticmethod
    def show_buffer_data(buffer):
        for i in range(len(buffer)//8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])


    @staticmethod
    def load_model(file):
        vert_coords = [] # armazena as coordenadas dos vetor
        tex_coords = [] # armazena as coordenadas dos vetores de textura
        norm_coords = [] # armazena as coordenadas dos vetores normal

        all_indices = [] # armazena os indices de cada vetor, textura e normal
        indices = [] # armazena os indices das faces do objeto

        arquive = open(file, 'r')

        with arquive as f:
            line = f.readline()
            
            while line:
                values = line.split()
                if (len(values) != 0):
                    if values[0] == 'v':
                        ObjLoad.search_data(values, vert_coords, 'v', 'float')
                    elif values[0] == 'vt':
                        ObjLoad.search_data(values, tex_coords, 'vt', 'float')
                    elif values[0] == 'vn':
                        ObjLoad.search_data(values, norm_coords, 'vn', 'float')
                    elif values[0] == 'f':
                        for value in values[1:]:
                            val = value.split('/')
                            ObjLoad.search_data(val, all_indices, 'f', 'int')
                            indices.append(int(val[0])-1)

                line = f.readline()

        arquive.close()
        
        # Cria um array com os valores dos vetores ordenados por vetores, textura e normal
        # de acordo com o que é especificado na face do objeto
        ObjLoad.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords)

        # ObjLoader.show_buffer_data(ObjLoader.buffer)

        buffer = ObjLoad.buffer.copy() # Cria uma copia do array com os vetores do objeto, 
                                       # se essa copia não fosse realizada o array estatico seria sobrescrito
        ObjLoad.buffer = [] # Depois da copia esvazia o array da classe estatica

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')