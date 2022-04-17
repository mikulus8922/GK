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


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def spin(angle):
    glRotate(angle, 1, 0, 0)
    glRotate(angle, 0, 1, 0)
    glRotate(angle, 0, 0, 1)


def get_vertices(n):
    n_table = numpy.linspace(0, 1, n)
    vertices = []

    for i in range(n):
        vertices.append([])
        for j in range(n):
            vertices[i].append([])
            for k in range(3):
                vertices[i][j].append([0])

    for u_index in range(n):
        for v_index in range(n):
            vertices[u_index][v_index][0] = (- 90 * n_table[u_index]**5 + 225 * n_table[u_index]**4
                                             - 270 * n_table[u_index]**3 + 180 * n_table[u_index]**2
                                             - 45 * n_table[u_index]) * numpy.cos(numpy.pi * n_table[v_index])
            vertices[u_index][v_index][1] = (160 * n_table[u_index]**4 - 320 * n_table[u_index]**3
                                             + 160 * n_table[u_index]**2)
            vertices[u_index][v_index][2] = (- 90 * n_table[u_index]**5 + 225 * n_table[u_index]**4
                                             - 270 * n_table[u_index]**3 + 180 * n_table[u_index]**2
                                             - 45 * n_table[u_index]) * numpy.sin(numpy.pi * n_table[v_index])

    return vertices


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    axes()

    glFlush()


def render_egg_points(time, vertices, number_of_points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    glBegin(GL_POINTS)

    for i in range(number_of_points):
        for j in range(number_of_points):
            glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])

    glEnd()

    glFlush()


def render_egg_lines(time, vertices, number_of_points):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    for i in range(number_of_points - 1):
        for j in range(number_of_points - 1):
            glBegin(GL_LINES)
            glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
            glEnd()
            glBegin(GL_LINES)
            glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex(vertices[i][j+1][0], vertices[i][j+1][1], vertices[i][j+1][2])
            glEnd()

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


def render_egg_triangles(time, vertices, number_of_points, colors):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    for i in range(number_of_points - 1):
        for j in range(number_of_points - 1):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glBegin(GL_TRIANGLES)
            glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
            glVertex(vertices[i][j+1][0], vertices[i][j+1][1], vertices[i][j+1][2])
            glEnd()
            glBegin(GL_TRIANGLES)
            glVertex(vertices[i+1][j+1][0], vertices[i+1][j+1][1], vertices[i+1][j+1][2])
            glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
            glVertex(vertices[i][j+1][0], vertices[i][j+1][1], vertices[i][j+1][2])
            glEnd()

    glFlush()


def render_edd_triangle_strip(time, vertices, number_of_points, colors):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    for i in range(number_of_points - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(number_of_points):
            glColor3f(colors[i][j][0], colors[i][j][1], colors[i][j][2])
            glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
            glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
        glEnd()

    glFlush()


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

    vertices = get_vertices(number_of_points)
    colors = generate_random_colors(number_of_points)

    startup()
    while not glfwWindowShouldClose(window):
        # render(glfwGetTime())
        render_egg_points(glfwGetTime(), vertices, number_of_points)
        #render_egg_lines(glfwGetTime(), vertices, number_of_points)
        #render_egg_triangles(glfwGetTime(), vertices, number_of_points, colors)
        #render_edd_triangle_strip(glfwGetTime(), vertices, number_of_points, colors)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
