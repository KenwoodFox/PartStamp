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

        # Get the mesh
        self.stl_mesh = stl_mesh
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom_factor = 1.0

        # Initialize variables for mouse interaction
        self.mouse_pos = None  # Store the mouse position
        self.hover_point = None  # Store the hover point's XYZ coordinates

        # Center the mesh
        self.center_mesh()

        # Set focus policy to enable capturing keyboard events
        self.setFocusPolicy(Qt.StrongFocus)

    def center_mesh(self):
        """
        Calculate the center and scale the mesh to fit the view.
        """

        min_coords = np.min(self.stl_mesh.vectors, axis=(0, 1))
        max_coords = np.max(self.stl_mesh.vectors, axis=(0, 1))
        self.mesh_center = (min_coords + max_coords) / 2
        self.mesh_scale = 2.0 / np.max(max_coords - min_coords)  # Scale to fit

    def initializeGL(self):
        """
        Things to initialize openGL
        """

        glClearColor(0.1, 0.1, 0.1, 1.0)  # Set background color
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering
        glEnable(GL_LIGHTING)  # Enable lighting
        glEnable(GL_LIGHT0)  # Add a light source
        glEnable(GL_COLOR_MATERIAL)  # Enable material color
        glShadeModel(GL_SMOOTH)  # Smooth shading

    def resizeGL(self, width, height):
        """
        Used to zoom in and out
        """

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """
        Repaints the openGL 3d
        """

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

        # Render edge shading
        self.render_edge_shading()

        # Render hover point if available
        if self.hover_point is not None:
            self.draw_hover_point(self.hover_point)

    def render_stl(self):
        """
        Actually re-renders the stl
        """

        glColor3f(0.8, 0.8, 0.8)  # Set mesh color to gray
        glBegin(GL_TRIANGLES)
        for triangle in self.stl_mesh.vectors:
            for vertex in triangle:
                glVertex3fv(vertex)
        glEnd()

    def render_edge_shading(self):
        """
        Render the edges of the STL model as a wireframe.
        """

        glColor3f(0, 0, 0)  # Black color for edges
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Wireframe mode
        glBegin(GL_TRIANGLES)
        for triangle in self.stl_mesh.vectors:
            for vertex in triangle:
                glVertex3fv(vertex)
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Reset back to fill mode

    def draw_hover_point(self, point):
        """
        Draw a small red circle at the given point.
        """

        glColor3f(1.0, 0.0, 0.0)  # Red color for hover point
        glPointSize(10.0)  # Set point size
        glBegin(GL_POINTS)
        glVertex3f(point[0], point[1], point[2])
        glEnd()

    def mouseMoveEvent(self, event):
        """
        Handle mouse movement for hover detection.
        """

        self.mouse_pos = event.pos()
        self.hover_point = self.get_hover_point(self.mouse_pos)
        self.update()

    def get_hover_point(self, mouse_pos):
        """
        Convert mouse position to 3D coordinates (mockup).
        """

        # You would need raycasting or OpenGL picking for real calculations
        # For now, we'll mock it with the center of the mesh
        return self.mesh_center  # Replace this with real intersection calculations

    def keyPressEvent(self, event):
        """
        Handle key events for rotating and zooming.
        """

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
