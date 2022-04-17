#!/usr/bin/env python3
import sys
from random import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotate(angle, 1, 0, 0)
    glRotate(angle, 0, 1, 0)
    glRotate(angle, 0, 0, 1)


def render_single_pyramid(time, x, y, z, h):
    # (x-h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))         (x+h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    #                                           (x, y, z)
    # (x-h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))         (x+h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    #                                 +z
    #                               -x + +x
    #                                 -z
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex(x, y, z)
    glVertex(x-h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glVertex(x+h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex(x, y, z)
    glVertex(x+h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glVertex(x+h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex(x, y, z)
    glVertex(x+h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glVertex(x-h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex(x, y, z)
    glVertex(x-h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glVertex(x-h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex(x-h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glVertex(x+h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glVertex(x-h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 1.0)
    glVertex(x-h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glVertex(x+h/numpy.sqrt(3), y-h, z-h/numpy.sqrt(3))
    glVertex(x+h/numpy.sqrt(3), y-h, z+h/numpy.sqrt(3))
    glEnd()


def render(time, x, y, z, h, r):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    render_sierpinski_pyramid(time, x, y, z, h, r)

    glFlush()


def render_sierpinski_pyramid(time, x, y, z, h, r):
    if r > 0:
        r = r - 1
        if r == 0:
            render_single_pyramid(time, x, y, z, h)

        render_sierpinski_pyramid(time, x, y, z, h/2, r)
        render_sierpinski_pyramid(time, x-h/(2*numpy.sqrt(3)), y-(h/2), z+h/(2*numpy.sqrt(3)), h/2, r)
        render_sierpinski_pyramid(time, x+h/(2*numpy.sqrt(3)), y-(h/2), z+h/(2*numpy.sqrt(3)), h/2, r)
        render_sierpinski_pyramid(time, x-h/(2*numpy.sqrt(3)), y-(h/2), z-h/(2*numpy.sqrt(3)), h/2, r)
        render_sierpinski_pyramid(time, x+h/(2*numpy.sqrt(3)), y-(h/2), z-h/(2*numpy.sqrt(3)), h/2, r)

    glFlush()


def generate_random_colors(n):

    colors = []

    for i in range(n):
        colors.append([])
        for j in range(n):
            colors[i].append([])
            for k in range(3):
                colors[i][j].append([0])

    for u_index in range(n):
        for v_index in range(n):
            colors[u_index][v_index][0] = random()
            colors[u_index][v_index][1] = random()
            colors[u_index][v_index][2] = random()

    return colors


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
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    number_of_points = 51

    startup()
    while not glfwWindowShouldClose(window):
        # render(glfwGetTime())
        # render_egg_lines(glfwGetTime(), vertices, number_of_points)
        # render_egg_triangles(glfwGetTime(), vertices, number_of_points, colors)
        render(glfwGetTime(), 0, 0, 0, 5, 2)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
