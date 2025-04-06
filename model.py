from PyQt6.QtOpenGLWidgets import QOpenGLWidget 
from PyQt6.QtCore import QTimer # Correct import for PyQt6
from OpenGL.GL import *
import math
import numpy as np

class OpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800,600)
        self.state1 = np.array([[0,0],[0,0]],dtype=float)
        self.state2 = np.array([[0,0],[0,0]],dtype=float)
        self.state3 = np.array([[0,0],[0,0]],dtype=float)
        self.mass1 = 50
        self.mass2 = 10
        self.mass3 = 2
        self.mass = self.mass1+self.mass2+self.mass3
        self.trail1 = []
        self.trail2 = []
        self.trail3 = []
        self.max_trail_length = 10000  # adjust for longer or shorter trails


    def initializeGL(self):
            glClearColor(0, 0, 0, 0)  # White background
            glEnable(GL_LINE_SMOOTH)  # Anti-aliasing
    def resizeGL(self, w, h):
        """ Adjust viewport and projection """
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-3, 3, -2, 2, -1, 1)  # Set coordinate system
        glMatrixMode(GL_MODELVIEW)
    def paintGL(self):
        center_x = (self.mass1 * self.state1[0][0] + self.mass2 * self.state2[0][0] + self.mass3 * self.state3[0][0]) / self.mass
        center_y = (self.mass1 * self.state1[0][1] + self.mass2 * self.state2[0][1] + self.mass3 * self.state3[0][1]) / self.mass
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-center_x, -center_y, 0)

        # Append current positions to trail
        self.trail1.append(tuple(self.state1[0]))
        self.trail2.append(tuple(self.state2[0]))
        self.trail3.append(tuple(self.state3[0]))
        # Limit trail length
        if len(self.trail1) > self.max_trail_length:
            self.trail1.pop(0)
        if len(self.trail2) > self.max_trail_length:
            self.trail2.pop(0)
        if len(self.trail3) > self.max_trail_length:
            self.trail3.pop(0)


        glPushMatrix()  # Save the current transformation state
        glTranslatef(self.state1[0][0] , self.state1[0][1] ,0)
        glColor3f(1.0, 0.0, 0.0) # 1
        self.draw_circle(0, 0, 0.1, 100)
        glPopMatrix()

        glPushMatrix()  # Save the current transformation state # 2
        glTranslatef(self.state2[0][0] , self.state2[0][1] ,0)
        glColor3f(0.0, 1.0, 0.0)
        self.draw_circle(0, 0, 0.05, 100)
        glPopMatrix()


        glPushMatrix()  # Save the current transformation state # 2
        glTranslatef(self.state3[0][0] , self.state3[0][1] ,0)
        glColor3f(0.0, 0.0, 1.0)
        self.draw_circle(0, 0, 0.03, 100)
        glPopMatrix()


        # Draw trail for mass1 (red)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for x, y in self.trail1:
            glVertex2f(x, y)
        glEnd()

        # Draw trail for mass2 (green)
        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for x, y in self.trail2:
            glVertex2f(x, y)
        glEnd()

        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINE_STRIP)
        for x, y in self.trail3:
            glVertex2f(x, y)
        glEnd()
    
    def draw_circle(self, cx, cy, radius, num_segments):
        """Draw a filled circle using GL_TRIANGLE_FAN"""
        # glTranslatef(0, self.state[0], 0)
          # Set color to red
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)  # Center of the circle
        for i in range(num_segments + 1):
            angle = 2.0 * math.pi * i / num_segments
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            glVertex2f(x, y)
        glEnd()