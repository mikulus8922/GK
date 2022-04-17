#!/usr/bin/env python3
import sys


from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

theta = 0.0
phi = 0.0
scale = 0.01
pix2angle = 1.0

w_key_pressed = 0
s_key_pressed = 0
a_key_pressed = 0
d_key_pressed = 0
left_mouse_button_pressed = 0

mouse_x_pos_old = 0
delta_x = 0
mouse_y_pos_old = 0
delta_y = 0

eye = [-4, 0, -4]
center = [0, 0, 0]
speed = 0.05


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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


def render(time, x, y, z, h, r):
    global theta
    global phi
    global speed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi -= delta_y * pix2angle
        if theta > 360:
            theta -= 360
        if theta < 0:
            theta += 360
        if phi > 360:
            phi -= 360
        if phi < 0:
            phi += 360

    if w_key_pressed:
        eye[0] += numpy.cos(theta * numpy.pi / 180) * speed
        eye[1] += numpy.sin(phi * numpy.pi / 180) * speed
        eye[2] += numpy.sin(theta * numpy.pi / 180) * speed

    if s_key_pressed:
        eye[0] -= numpy.cos(theta * numpy.pi / 180) * speed
        eye[1] -= numpy.sin(phi * numpy.pi / 180) * speed
        eye[2] -= numpy.sin(theta * numpy.pi / 180) * speed

    if a_key_pressed:
        eye[0] -= numpy.cos((theta + 90) * numpy.pi / 180) * speed
        eye[2] -= numpy.sin((theta + 90) * numpy.pi / 180) * speed

    if d_key_pressed:
        eye[0] += numpy.cos((theta + 90) * numpy.pi / 180) * speed
        eye[2] += numpy.sin((theta + 90) * numpy.pi / 180) * speed

    center[0] = eye[0] + numpy.cos(theta * numpy.pi / 180) * numpy.cos(phi * numpy.pi / 180)
    center[1] = eye[1] + numpy.sin(phi * numpy.pi / 180)
    center[2] = eye[2] + numpy.sin(theta * numpy.pi / 180) * numpy.cos(phi * numpy.pi / 180)

    up = 1.0
    if 90 < phi % 360 < 270:
        up = -1.0

    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2], 0.0, up, 0.0)

    render_sierpinski_pyramid(time, x, y, z, h, r)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle

    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global w_key_pressed
    global s_key_pressed
    global a_key_pressed
    global d_key_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        w_key_pressed = 1
    if key == GLFW_KEY_W and action == GLFW_RELEASE:
        w_key_pressed = 0

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        s_key_pressed = 1
    if key == GLFW_KEY_S and action == GLFW_RELEASE:
        s_key_pressed = 0
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        a_key_pressed = 1
    if key == GLFW_KEY_A and action == GLFW_RELEASE:
        a_key_pressed = 0

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        d_key_pressed = 1
    if key == GLFW_KEY_D and action == GLFW_RELEASE:
        d_key_pressed = 0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global delta_y
    global mouse_x_pos_old
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos
    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), 0, 0, 0, 5, 5)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
