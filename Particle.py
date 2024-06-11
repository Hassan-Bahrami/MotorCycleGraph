import numpy as np

class Particle:
    particle_counter = 0  # Class-level variable to track the particle index

    def __init__(self, edge, vertex, face):
        self.index = Particle.particle_counter
        Particle.particle_counter += 1

        self.edge = edge  # The current edge the particle is on
        self.vertex = vertex  # The current vertex the particle is at
        self.face = face
        self.traveled_edges = [edge]
        self.met_particles = []

    def at_interior_vertex(self, extraordinary_vertices):
        # Get the vertices of the current edge
        v1, v2 = self.edge

        # Determine if the destination vertex (v2) is an ordinary (interior) vertex
        is_interior = v2 not in extraordinary_vertices  # Assuming self.extraordinaryVertices contains the list of extraordinary vertices

        return is_interior

    def move_to(self, new_edge, new_face):
        # Move the particle to a new edge and update its state
        self.vertex = self.edge[1]  # Update the current vertex to the destination vertex of the current edge
        self.edge = new_edge # Update the current edge to the opposite edge
        self.face = new_face # Update the current face to the opposite face
        self.traveled_edges.append(new_edge)

    def get_traveled_edges(self):
        return self.traveled_edges

    def meets_another_particles_track(self, particles):
        # Check if the particle meets another particle's track
        current_edge = self.edge
        current_vertex = self.vertex

        for other_particle in particles:
            if other_particle != self:
                other_edges = other_particle.get_traveled_edges()
                for edge in other_edges:
                    # if (edge[0] == current_vertex and edge[1] != current_edge[0]) or (edge[1] == current_vertex and edge[0] != current_edge[0]):
                    if (edge[0] == current_edge[1]):
                        return True  # Intersection found

        return False  # No intersection found

    def meets_boundary_vertex(self, boundary_vertices):
        # Check if the particle meets a boundary vertex
        v1, v2 = self.edge

        # Check if either vertex v1 or v2 is a boundary vertex
        if v2 in boundary_vertices:
            return True

        return False

    def meets_multiple_particles(self, particles):
        self.meeting_counter(particles)

        if len(self.met_particles) >= 1:
            return True

        return False

    def meeting_counter(self, particles):
        self.met_particles = []
        current_edge = self.edge

        for other_particle in particles:
            if other_particle != self and other_particle.edge[1] == current_edge[1]:
                self.met_particles.append(other_particle)

