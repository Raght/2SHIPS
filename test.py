from Mesh import *
from shapes import *
from pygame import *

p = Vector2(0, 0)
c = Color(255, 0, 0)
mesh = Mesh([Rectangle(p, 1, 2, c), Circle(p, 1, c), Triangle(p, p, p, c)])

for shape in mesh:
    print(shape)