from stl import mesh
from PyQt5.QtWidgets import QMainWindow
from OpenGL.GL import *
from OpenGL.GLU import *


class STLViewer(QMainWindow):
    def __init__(self, stl_mesh):
        super().__init__()
        self.stl_mesh = stl_mesh
        self.setWindowTitle("STL Viewer")
        self.setGeometry(100, 100, 800, 600)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -5)  # Adjust as needed
        self.render_stl()
        glFlush()

    def render_stl(self):
        glBegin(GL_TRIANGLES)
        for triangle in self.stl_mesh.vectors:
            for vertex in triangle:
                glVertex3fv(vertex)
        glEnd()

    def resizeGL(self, w, h):
        if h == 0:
            h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


def load_stl(file_path):
    """Load an STL file and return the mesh object."""
    return mesh.Mesh.from_file(file_path)


def engrave_text_on_stl(input_stl, text, position, size, output_stl):
    """Mock function for engraving text on the STL file."""
    print(f"Engraving '{text}' at position {position} with size {size}")
    input_stl.save(output_stl)  # Save unchanged for now
