#!/home/larce/Documents/game1/game1_venv/bin/python

####
import random
import configparser
import sys
from perlin import mesh_3d
import numpy as np
from loguru import logger
import ursina as ua
from math import sin
from ursina.prefabs.first_person_controller import FirstPersonController


####

app = ua.Ursina()
ua.window.borderless = False
ua.window.exit_button.visible = False
ua.window.show_ursina_splash = True

####

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

####


class Environment(object):
    def __init__(self, config):
        self.screen = ua.window
        self.config = config
        self.matrix_size = int(config["SCREEN"]["WIDTH"])
        self.mesh_width = int(config["MeshParam"]["WIDTH"])
        self.mesh_height = int(config["MeshParam"]["HEIGHT"])
        self.mesh_3d = mesh_3d(self.mesh_width, self.mesh_height)
        self.original_mesh_3d = self.mesh_3d
        self.screen_x = int(config["SCREEN"]["WIDTH"])
        self.screen_y = int(config["SCREEN"]["HEIGHT"])
        self.screen.size = (self.screen_x, self.screen_y)
        self.bioms_dict = config[f"Colors"]
        self.DEEP = int(config["MeshParam"]["MAX_DEEP"])
        self.color_dict = {i:self.bioms_dict[i] for i in self.bioms_dict}
        self.mesh_entity = None
        self.multiplier_matrix = np.ones(self.mesh_3d.shape)
        self.multiplier_ocean_matrix = np.zeros(self.mesh_3d.shape)
        np.where(self.mesh_3d < 5, self.multiplier_ocean_matrix, 1)
        self.multiplier = 1.1

    def draw_mesh(self):
        verts, tris, colors = self.calc_grid()
        # uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
        norms = ((0,0,-1),) * len(verts)

        self.mesh_entity = ua.Entity(model=ua.Mesh(vertices=verts, triangles=tris, uvs=None, normals=norms, colors=colors), scale=2)
        self.mesh_entity.collider = ua.MeshCollider(self.mesh_entity, mesh=self.mesh_entity.model, center=ua.Vec3(0,0,0))
        # logger.info(self.mesh_3d[0])
        cat = ua.Entity(
            model="3d_mod/Cat/kitten",
            # texture="3d_mod/Cat/kitten", 
            rotation=(0,0,0), 
            scale=(1, 1, 1), 
            position=(25, 25, 52), 
            parent=ua.scene,
            collision=True,
            collider = 'box' 
        )

        cat.color = ua.color.black
        cat.gravity = 1
        cat.grounded = True

    @property
    def propperty(self):
        return self.mesh_entity.collider

    def mesh_color_chooser(self, e, m, element_number, mesh_shape):
        if e < -0.3:
            self.multiplier_ocean_matrix[
                (0 if element_number < mesh_shape[1] else element_number // mesh_shape[0]),
                element_number % mesh_shape[0]
                ][1] = 1
            return "deep_ocean"
        elif e < 0.1:
            self.multiplier_ocean_matrix[
                (0 if element_number < mesh_shape[1] else element_number // mesh_shape[0]),
                element_number % mesh_shape[0]
                ][1] = 1
            return "ocean"
        
        elif e > 0.8:
            if m < 0.1:
                return "scorched"
            elif m < 0.2:
                return "bare"
            elif m < 0.5:
                return "tundra"
            return "snow"

        elif e > 0.6:
            if m < 0.33:
                return "temperate_desert"
            elif m < 0.66:
                return "shrubland"
            return "taiga"

        elif e > 0.3:
            if m < 0.16:
                return "temperate_desert"
            elif m < 0.50:
                return "grassland"
            elif m < 0.83:
                return "temperate_deciduous_forest"
            return "temperate_rain_forest"

        elif m < 0.16:
            return "subtropical_desert"
        elif m < 0.33:
            return "grassland"
        elif m < 0.66:
            return "tropical_seasonal_forest"

        return "tropical_rain_forest"
    
    def mesh_eval_inc(self):
        matrix = np.array([[(x, z * self.multiplier, y) for x, z, y in row] for row in self.multiplier_matrix])
        self.mesh_3d = self.original_mesh_3d * matrix
        self.mesh_entity.model.vertices, self.mesh_entity.model.triangles, self.mesh_entity.model.colors = self.calc_grid()
        self.mesh_entity.model.generate()
        self.multiplier += 0.1

    def mesh_planer(self):
        matrix = np.array([[(x, z ** 2, y) for x, z, y in row] for row in self.multiplier_matrix])
        self.mesh_3d = self.original_mesh_3d * matrix
        self.mesh_entity.model.vertices, self.mesh_entity.model.triangles, self.mesh_entity.model.colors = self.calc_grid()
        self.mesh_entity.model.generate()

    def mesh_waving(self):
        matrix = self.multiplier_ocean_matrix * sin(ua.time.process_time()) + 1
        # logger.info(self.multiplier_ocean_matrix)
        self.mesh_3d = self.original_mesh_3d * matrix
        self.mesh_entity.model.vertices, self.mesh_entity.model.triangles, self.mesh_entity.model.colors = self.calc_grid()
        self.mesh_entity.model.generate()

    def calc_grid(self):
        mesh_size = self.mesh_3d.size
        mesh_shape = self.mesh_3d.shape
        verts = [(i[0], i[1] * self.DEEP, i[2]) for i in self.mesh_3d.reshape(int(mesh_size / 3), 3)]
        tris = []
        evaluate = self.mesh_3d.ravel()[1::3]
        moisture = evaluate[::-1]
        colors = [ua.color.hex(self.color_dict[self.mesh_color_chooser(evaluate[i], moisture[i], i, mesh_shape)]) for i in range(len(evaluate))]
        rows = self.mesh_3d.shape[0]
        for j in range(self.mesh_3d.shape[1])[:-1]:
            for i in range(self.mesh_3d.shape[0])[:-1]:
                tris.append(
                    (
                        i + mesh_shape[1] + (j * rows), 
                        i + 1 + (j * rows),
                        i + mesh_shape[1] + 1 + (j * rows)
                    ))
                tris.append(
                    (
                        i + (j * rows), 
                        i + 1 + (j * rows),
                        i + mesh_shape[1] + (j * rows)
                    ))
        return verts, tris, colors
####

if __name__ == "__main__":

    env = Environment(config)
    env.draw_mesh()
    player = FirstPersonController()
    player.collider = 'mesh_shape'
    player.speed = 15
    player.mouse_sensitivity = (5, 5)
    player.gravity = 0.1
    player.jump_height = 15
    # player.position = (30, 120, 30)
    # player.position = ua.Vec3(94, 72, 96)
    # camera = ua.EditorCamera()

    # ua.Cursor()
    # ua.mouse.visible = False
    # ua.mouse.velocity = ua.Vec3(2,2,2) 
    # ua.mouse.update_step = 2 
    # ua.mouse.enabled = False 
    
    def update():
        if (ua.held_keys['o']):
            env.mesh_eval_inc()
        if (ua.held_keys['i']):
            env.mesh_waving()
        # logger.info(env.propperty)
        env.mesh_waving()

    app.run()