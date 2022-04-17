import sys
import numpy
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

theta_light = 0.0
phi_light = 0.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light0_ambient = [0.1, 0.1, 0.0, 1.0]
light0_diffuse = [0.8, 0.8, 0.0, 1.0]
light0_specular = [1.0, 1.0, 1.0, 1.0]
light0_position = [0.0, 0.0, 10.0, 1.0]

light1_ambient = [0.1, 0.0, 0.1, 1.0]
light1_diffuse = [0.0, 0.0, 0.8, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [10.0, 10.0, 0.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

choose_ads = 0
choose_rgb = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    # glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    # glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    # glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    # glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    #
    # glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    # glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    # glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    # zad1
    # glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta
    global phi
    global theta_light
    global phi_light
    # global light0_position

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

    if right_mouse_button_pressed:
        theta_light += delta_x * pix2angle
        phi_light += delta_y * pix2angle
        if theta_light > 360:
            theta_light -= 360
        elif theta_light < 0:
            theta_light += 360
        if phi_light > 360:
            phi_light -= 360
        elif phi_light < 0:
            phi_light += 360

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)

    xs = 5 * numpy.cos(theta_light * (numpy.pi / 180)) * numpy.cos(phi_light * (numpy.pi / 180))
    ys = 5 * numpy.sin(phi_light * (numpy.pi / 180))
    zs = 5 * numpy.sin(theta_light * (numpy.pi / 180)) * numpy.cos(phi_light * (numpy.pi / 180))

    glLightfv(GL_LIGHT0, GL_AMBIENT, light0_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light0_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light0_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, [xs, ys, zs])

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glEnable(GL_LIGHT0)

    quadric = gluNewQuadric()
    # GLU_FILL
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glDisable(GL_LIGHT0)

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
    global choose_rgb
    global choose_ads

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_Z and action == GLFW_PRESS:
        choose_ads += 1
        if choose_ads == 3:
            choose_ads = 0
        print(f"ADS mode: {choose_ads + 1}")

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        choose_rgb += 1
        if choose_rgb == 3:
            choose_rgb = 0
        print(f"RGB mode: {choose_rgb + 1}")

    if key == GLFW_KEY_C and action == GLFW_PRESS:
        if choose_ads == 0:
            light0_ambient[choose_rgb] -= 0.1
            if light0_ambient[choose_rgb] < 0.0:
                light0_ambient[choose_rgb] = 0.0
            print(f"Light ambient: {light0_ambient[choose_rgb]}")
        elif choose_ads == 1:
            light0_diffuse[choose_rgb] -= 0.1
            if light0_diffuse[choose_rgb] < 0.0:
                light0_diffuse[choose_rgb] = 0.0
            print(f"Light diffuse: {light0_diffuse[choose_rgb]}")
        else:
            light0_specular[choose_rgb] -= 0.1
            if light0_specular[choose_rgb] < 0.0:
                light0_specular[choose_rgb] = 0.0
            print(f"Light specular: {light0_specular[choose_rgb]}")

    if key == GLFW_KEY_V and action == GLFW_PRESS:
        if choose_ads == 0:
            light0_ambient[choose_rgb] += 0.1
            if light0_ambient[choose_rgb] > 1.0:
                light0_ambient[choose_rgb] = 1.0
            print(f"Light ambient: {light0_ambient[choose_rgb]}")
        elif choose_ads == 1:
            light0_diffuse[choose_rgb] += 0.1
            if light0_diffuse[choose_rgb] > 1.0:
                light0_diffuse[choose_rgb] = 1.0
            print(f"Light diffuse: {light0_diffuse[choose_rgb]}")
        else:
            light0_specular[choose_rgb] += 0.1
            if light0_specular[choose_rgb] > 1.0:
                light0_specular[choose_rgb] = 1.0
            print(f"Light specular: {light0_specular[choose_rgb]}")


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
    global right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


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
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
