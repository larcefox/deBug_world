#!/home/larce/Documents/game1/game1_venv/bin/python
import ursina as ua
from time import perf_counter
t = perf_counter()
ua.Entity(model='cube', shader=ua.Shader())
ua.EditorCamera()
print('ttttttttttttt', perf_counter() - t)
app = ua.Ursina()


# def input(key):
#     if held_keys['control'] and key == 'r':
#         reload_shaders()

def reload_shaders():
    for e in ua.scene.entities:
        if hasattr(e, '_shader'):
            print('-------', e.shader)
            
def update():
    if (ua.held_keys['r']):
        reload_shaders()

app.run()