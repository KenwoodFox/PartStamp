import numpy as np

from stl import mesh

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QOpenGLWidget

from OpenGL.GL import *
from OpenGL.GLU import *


class STLViewer(QMainWindow):
    def __init__(self, stl_mesh):
        super().__init__()

        self.stl_mesh = stl_mesh
        self.opengl_widget = OpenGLWidget(stl_mesh)
        self.setCentralWidget(self.opengl_widget)
        self.setWindowTitle("STL Viewer")
        self.setGeometry(100, 100, 800, 600)


class OpenGLWidget(QOpenGLWidget):
    def __init__(self, stl_mesh):
        super().__init__()
        self.stl_mesh = stl_mesh
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom_factor = 1.0
        self.center_mesh()

        # Set focus policy to enable capturing keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

    def center_mesh(self):
        """Calculate the center and scale the mesh to fit the view."""
        min_coords = np.min(self.stl_mesh.vectors, axis=(0, 1))
        max_coords = np.max(self.stl_mesh.vectors, axis=(0, 1))
        self.mesh_center = (min_coords + max_coords) / 2
        self.mesh_scale = 2.0 / np.max(max_coords - min_coords)  # Scale to fit

    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)  # Set background color
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glEnable(GL_LIGHTING)  # Enable lighting
        glEnable(GL_LIGHT0)  # Add a light source
        glEnable(GL_COLOR_MATERIAL)  # Enable material color
        glShadeModel(GL_SMOOTH)  # Smooth shading

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply zoom and rotation
        glTranslatef(0.0, 0.0, -10.0 * self.zoom_factor)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

        # Center the mesh and scale it
        glScalef(self.mesh_scale, self.mesh_scale, self.mesh_scale)
        glTranslatef(-self.mesh_center[0], -self.mesh_center[1], -self.mesh_center[2])

        # Render the STL mesh
        self.render_stl()

    def render_stl(self):
        glBegin(GL_TRIANGLES)
        for triangle in self.stl_mesh.vectors:
            for vertex in triangle:
                glVertex3fv(vertex)
        glEnd()

    def keyPressEvent(self, event):
        """Handle key events for rotating and zooming."""

        key = event.key()
        if key == Qt.Key_Left:
            self.rotation_y -= 5
        elif key == Qt.Key_Right:
            self.rotation_y += 5
        elif key == Qt.Key_Up:
            self.rotation_x -= 5
        elif key == Qt.Key_Down:
            self.rotation_x += 5
        elif key == Qt.Key_Plus or key == Qt.Key_Equal:
            self.zoom_factor *= 0.9  # Zoom in
        elif key == Qt.Key_Minus:
            self.zoom_factor *= 1.1  # Zoom out
        self.update()  # Request a repaint


def load_stl(file_path):
    """Load an STL file and return the mesh object."""
    return mesh.Mesh.from_file(file_path)


def engrave_text_on_stl(input_stl, text, position, size, output_stl):
    """Mock function for engraving text on the STL file."""
    print(f"Engraving '{text}' at position {position} with size {size}")
    input_stl.save(output_stl)  # Save unchanged for now
