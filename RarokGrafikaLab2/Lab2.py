import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import random
import numpy


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def generate_random_color():
    color = [random(), random(), random()]
    return color


def render_triangle(time):

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(0.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glFlush()


#  zadanie 1
def render_triangle_color(time):

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(-50, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50, 0)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0, 40)
    glEnd()

    glFlush()


#  zadanie 2, 3 (koordynaty x;y wskazują lewy górny wierzchołek)
def render_rectangle(time, x, y, a, b, color, d=0):

    a = a + a*d
    b = b + b*d

    glColor3f(color[0], color[1], color[2])

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+a, y)
    glVertex2f(x, y-b)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a, y)
    glVertex2f(x, y-b)
    glVertex2f(x+a, y-b)
    glEnd()

    glFlush()


#  zadanie 4
def render_sierpinski_carpet(time, x, y, a, b, color1, color2, r):
    render_rectangle(time, x, y, a, b, color1)
    render_sierpinski_carpet_holes(time, x, y, a, b, color2, r)


def render_sierpinski_carpet_holes(time, x, y, a, b, color, r):
    if r > 0:
        r = r-1
        render_rectangle(time, x + a / 3, y - b / 3, a / 3, b / 3, color)

        render_sierpinski_carpet_holes(time, x, y, a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x + a / 3, y, a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x + 2*(a / 3), y, a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x, y - b / 3, a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x + 2*(a / 3), y - b / 3, a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x, y - 2 * (b / 3), a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x + a / 3, y - 2 * (b / 3), a / 3, b / 3, color, r)
        render_sierpinski_carpet_holes(time, x + 2*(a / 3), y - 2 * (b / 3), a / 3, b / 3, color, r)


#  zadanie 5
def render_triangle_equilateral(time, x, y, h, color, orientation):
    if orientation == "up":
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x - h/numpy.sqrt(3), y - h)
        glVertex2f(x + h/numpy.sqrt(3), y - h)
        glEnd()
        glFlush()

    elif orientation == "down":
        glColor3f(color[0], color[1], color[2])
        glBegin(GL_TRIANGLES)
        glVertex2f(x, y)
        glVertex2f(x - h/numpy.sqrt(3), y + h)
        glVertex2f(x + h/numpy.sqrt(3), y + h)
        glEnd()
        glFlush()


# parametr "orientation" decyduje czy koordynaty x;y wskazują dolny czy górny wierzchołek trójkąta
def render_sierpinski_triangle(time, x, y, h, color1, color2, orientation, r):
    render_triangle_equilateral(time, x, y, h, color1, orientation)

    if orientation == "up":
        render_sierpinski_triangle_holes(time, x, y - h, h/2, color2, "down", r)
    elif orientation == "down":
        render_sierpinski_triangle_holes(time, x, y + h, h/2, color2, "up", r)


def render_sierpinski_triangle_holes(time, x, y, h, color, orientation, r):
    if r > 0:
        r = r - 1
        if orientation == "up":
            render_triangle_equilateral(time, x, y, h, color, orientation)
            render_sierpinski_triangle_holes(time, x, y - h, h/2, color, orientation, r)
            render_sierpinski_triangle_holes(time, x - h/numpy.sqrt(3), y, h / 2, color, orientation, r)
            render_sierpinski_triangle_holes(time, x + h/numpy.sqrt(3), y, h / 2, color, orientation, r)
        elif orientation == "down":
            render_triangle_equilateral(time, x, y, h, color, orientation)
            render_sierpinski_triangle_holes(time, x, y + h, h/2, color, orientation, r)
            render_sierpinski_triangle_holes(time, x - h/numpy.sqrt(3), y, h / 2, color, orientation, r)
            render_sierpinski_triangle_holes(time, x + h/numpy.sqrt(3), y, h / 2, color, orientation, r)


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():

    input_number = input("Wpisz numer zadania\n"
          "0 - trójkąt z przykładu\n"
          "1 - zadanie 1 (kolorowy trójkąt)\n"
          "2 - zadanie 2/3 (prostokąt z deformacjami i losowym kolorem)\n"
          "3 - zadanie 4 (dywan sierpińskiego)\n"
          "4 - zadanie 5 (trójkąt sierpińskiego)\n")

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    color1 = generate_random_color()  # jednorazowe wygenerowanie koloru prostokata
    color2 = generate_random_color()
    while not glfwWindowShouldClose(window):
        if input_number == '0':
            render_triangle(glfwGetTime())
        elif input_number == '1':
            render_triangle_color(glfwGetTime())
        elif input_number == '2':
            render_rectangle(glfwGetTime(), 0, 0, 50, 25, color1, d=-0.5)
        elif input_number == '3':
            render_sierpinski_carpet(glfwGetTime(), -90, 90, 180, 180, color1, color2, 5)
        elif input_number == '4':
            render_sierpinski_triangle(glfwGetTime(), 0, 90, 180, color1, color2, "up", 6)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
