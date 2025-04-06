from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget  # Correct import for PyQt6
import sys
from OpenGL.GL import *
from PyQt6.QtCore import QThread, pyqtSignal, Qt
import numpy as np
from model import OpenGLWidget
from motion import Gravitation


class SimulationThread(QThread):
    update_signal = pyqtSignal(object,object,object)
    def __init__(self,motion , object):
        super().__init__()
        self.object = object
        self.motion = motion
        self.running = True  # Control flag
    def run(self):
        while self.running:
            new_state1 , new_state2,new_state3= self.motion.force(self.object.state1,self.object.state2,self.object.state3)
            self.update_signal.emit(new_state1 ,new_state2,new_state3)
            self.msleep(1)
    def stop(self):
        self.running = False



class InvertedPendulam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.object = OpenGLWidget(self)
        
        container = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.object)
        container.setLayout(main_layout) 
        self.setCentralWidget(container)
        self.motion = Gravitation()
        # theta = 2*np.pi/3
        # sint = np.sin(theta)
        # cost = np.cos(theta)
        # tant = np.tan(theta)
        # vel_mag = 0.1
        pos1 = np.array([0, 0])
        pos2 = np.array([3, 0])
        pos3 = np.array([3.25,0 ])
        vel1 = np.array([0, 0])
        vel2 = np.array([0,10])
        vel3 = np.array([0,0.1])
        self.state1 = np.array([pos1, vel1], dtype=float)
        self.state2 = np.array([pos2, vel2], dtype=float)
        self.state3 = np.array([pos3, vel3], dtype=float)



        # fig 8
        # self.state1 = np.array([[0.97000436, -0.24308753], [0.4662036850, 0.4323657300]], dtype=float)
        # self.state2 = np.array([[-0.97000436, 0.24308753], [0.4662036850, 0.4323657300]], dtype=float)
        # self.state3 = np.array([[0.0, 0.0], [-0.93240737, -0.86473146]], dtype=float)

        self.intial()
        self.simulation_thread = SimulationThread(self.motion, self.object)
        self.simulation_thread.update_signal.connect(self.update_motion)

    def intial(self):
        self.object.state1 = self.state1
        self.object.state2 = self.state2
        self.object.state3 = self.state3
        self.object.update()
    def update_motion(self,new_state1 , new_state2,new_state3):
        self.object.state1 = new_state1
        self.object.state2 = new_state2
        self.object.state3 = new_state3
        self.object.update()
    def keyPressEvent(self, event):
        key = event.key()
        if key == 87:
            if not self.simulation_thread.isRunning():
                self.simulation_thread.start()   
        self.object.update()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvertedPendulam()
    window.show()
    sys.exit(app.exec())  