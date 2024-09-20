import logging
import numpy as np
import pkg_resources

from stl import mesh

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QOpenGLWidget, QWidget

from OpenGL.GL import *
from OpenGL.GLU import *

from partstamp.utils.logging_setup import setup_logging


class STLViewer(QMainWindow):
    def __init__(self, stl_mesh):
        super().__init__()

        # Load the .ui file
        ui_path = pkg_resources.resource_filename("partstamp.gui", "main.ui")
        loadUi(ui_path, self)

        # Set up logging
        setup_logging(self.loggingWindow)

        # Find the placeholder QOpenGLWidget from the .ui file
        placeholder_widget = self.findChild(QOpenGLWidget, "opengl_widget")

        # Ensure the placeholder widget exists
        if placeholder_widget is None:
            raise RuntimeError("opengl_widget not found in the .ui file")

        # Create an instance of GLViewer
        self.opengl_widget = GLViewer(self)
        self.opengl_widget.stl_mesh = stl_mesh  # Pass the STL mesh to the GLViewer

        # Copy the geometry and parent information from the placeholder widget
        self.opengl_widget.setGeometry(placeholder_widget.geometry())
        self.opengl_widget.setParent(placeholder_widget.parentWidget())

        # Show the new widget
        self.opengl_widget.show()

        # Safely remove the placeholder widget
        placeholder_widget.deleteLater()

        self.opengl_widget.initialize_mesh()


class GLViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stl_mesh = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom_factor = 1.0

    def initialize_mesh(self):
        """Initialize the mesh and OpenGL state."""
        if self.stl_mesh:
            self.center_mesh()

    def center_mesh(self):
        """Calculate the center and scale the mesh to fit the view."""
        min_coords = np.min(self.stl_mesh.vectors, axis=(0, 1))
        max_coords = np.max(self.stl_mesh.vectors, axis=(0, 1))
        self.mesh_center = (min_coords + max_coords) / 2
        self.mesh_scale = 2.0 / np.max(max_coords - min_coords)  # Scale to fit

    def initializeGL(self):
        """Initialize OpenGL settings."""
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        """Resize the OpenGL viewport."""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Render the STL model."""
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
        if self.stl_mesh:
            self.render_stl()

    def render_stl(self):
        """Render the STL mesh using OpenGL."""
        glColor3f(0.8, 0.8, 0.8)  # Set mesh color to gray
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
