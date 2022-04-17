#!/usr/bin/env python3
import sys
import numpy

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

is_wall_visible = True
is_first_texture_loaded = True

image1 = None
image2 = None

n_table = None


def get_vertices(n):
    global n_table
    n_table = numpy.linspace(0, 1, n)
    # print(n_table)
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


def render_egg_triangles(time, vertices, number_of_points):
    for i in range(number_of_points - 1):
        for j in range(number_of_points - 1):
            if i < (number_of_points/2) - 1:
                glBegin(GL_TRIANGLES)
                glTexCoord2f(n_table[i], n_table[j])
                glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
                glTexCoord2f(n_table[i+1], n_table[j])
                glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
                glTexCoord2f(n_table[i], n_table[j+1])
                glVertex(vertices[i][j+1][0], vertices[i][j+1][1], vertices[i][j+1][2])
                glEnd()
                glBegin(GL_TRIANGLES)
                glTexCoord2f(n_table[i], n_table[j+1])
                glVertex(vertices[i][j+1][0], vertices[i][j+1][1], vertices[i][j+1][2])
                glTexCoord2f(n_table[i+1], n_table[j])
                glVertex(vertices[i+1][j][0], vertices[i+1][j][1], vertices[i+1][j][2])
                glTexCoord2f(n_table[i+1], n_table[j+1])
                glVertex(vertices[i+1][j+1][0], vertices[i+1][j+1][1], vertices[i+1][j+1][2])
                glEnd()
            else:
                glBegin(GL_TRIANGLES)
                glTexCoord2f(n_table[i + 1], n_table[j])
                glVertex(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
                glTexCoord2f(n_table[i], n_table[j])
                glVertex(vertices[i][j][0], vertices[i][j][1], vertices[i][j][2])
                glTexCoord2f(n_table[i], n_table[j + 1])
                glVertex(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
                glEnd()
                glBegin(GL_TRIANGLES)
                glTexCoord2f(n_table[i + 1], n_table[j])
                glVertex(vertices[i + 1][j][0], vertices[i + 1][j][1], vertices[i + 1][j][2])
                glTexCoord2f(n_table[i], n_table[j + 1])
                glVertex(vertices[i][j + 1][0], vertices[i][j + 1][1], vertices[i][j + 1][2])
                glTexCoord2f(n_table[i + 1], n_table[j + 1])
                glVertex(vertices[i + 1][j + 1][0], vertices[i + 1][j + 1][1], vertices[i + 1][j + 1][2])
                glEnd()
    glFlush()


def startup():
    global image1
    global image2

    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    image1 = Image.open("textures/Mona-Lisa-256x256.tga")

    image2 = Image.open("textures/tekstura.tga")

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image1.size[0], image1.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image1.tobytes("raw", "RGB", 0, -1)
    )


def shutdown():
    pass


def render(time, vertices, number_of_points):
    global theta
    global phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
        if theta > 360:
            theta -= 360
        elif theta < 0:
            theta += 360
        if phi > 360:
            phi -= 360
        elif phi < 0:
            phi += 360

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    render_egg_triangles(time, vertices, number_of_points)

    # glBegin(GL_TRIANGLES)
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(-2.0, 2.0, 0.0)
    # glTexCoord2f(0.0, 0.0)
    # glVertex3f(-2.0, -2.0, 0.0)
    # glTexCoord2f(0.0, 1.0)
    # glVertex3f(2.0, -2.0, 0.0)
    # glEnd()
    #
    # glBegin(GL_TRIANGLES)
    # glTexCoord2f(1.0, 1.0)
    # glVertex3f(2.0, 2.0, 0.0)
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(-2.0, 2.0, 0.0)
    # glTexCoord2f(0.0, 1.0)
    # glVertex3f(2.0, -2.0, 0.0)
    # glEnd()
    #
    # # 1
    # if is_wall_visible:
    #     glBegin(GL_TRIANGLES)
    #     glTexCoord2f(0.5, 0.5)
    #     glVertex3f(0.0, 0.0, -2.0)
    #     glTexCoord2f(0.0, 0.0)
    #     glVertex3f(-2.0, -2.0, 0.0)
    #     glTexCoord2f(0.0, 1.0)
    #     glVertex3f(-2.0, 2.0, 0.0)
    #     glEnd()
    # # 2
    # glBegin(GL_TRIANGLES)
    # glTexCoord2f(0.5, 0.5)
    # glVertex3f(0.0, 0.0, -2.0)
    # glTexCoord2f(0.0, 1.0)
    # glVertex3f(-2.0, 2.0, 0.0)
    # glTexCoord2f(1.0, 1.0)
    # glVertex3f(2.0, 2.0, 0.0)
    # glEnd()
    # # 3
    # glBegin(GL_TRIANGLES)
    # glTexCoord2f(0.5, 0.5)
    # glVertex3f(0.0, 0.0, -2.0)
    # glTexCoord2f(1.0, 1.0)
    # glVertex3f(2.0, 2.0, 0.0)
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(2.0, -2.0, 0.0)
    # glEnd()
    # # 4
    # glBegin(GL_TRIANGLES)
    # glTexCoord2f(0.5, 0.5)
    # glVertex3f(0.0, 0.0, -2.0)
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(2.0, -2.0, 0.0)
    # glTexCoord2f(0.0, 0.0)
    # glVertex3f(-2.0, -2.0, 0.0)
    # glEnd()

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
    global is_wall_visible
    global is_first_texture_loaded
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        is_wall_visible = not is_wall_visible

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        is_first_texture_loaded = not is_first_texture_loaded
        if is_first_texture_loaded:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, image1.size[0], image1.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, image1.tobytes("raw", "RGB", 0, -1)
            )
        else:
            glTexImage2D(
                GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
            )


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

    number_of_points = 51
    vertices = get_vertices(number_of_points)

    print(vertices)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertices, number_of_points)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
