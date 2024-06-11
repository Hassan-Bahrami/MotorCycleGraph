import numpy as np
import Particle as P
import matplotlib.pyplot as plt
import pyvista as pv


class MotorcycleGraph:
	def __init__(self, mesh, vertices, faces, edges, extraordinaryVertices, boundary_vertices, boundary_edges):
		self.mesh = mesh
		self.V = vertices
		self.Q = faces  # Define the quads based on your implementation
		self.E = edges  # Define the edges based on your implementation
		self.extraordinaryVertices = extraordinaryVertices
		self.boundary_vertices = boundary_vertices
		self.boundary_edges = boundary_edges
		self.H = {}
		self.particles = []
		self.motorcycleEdges = []
		self.submeshes = []

	def constructMotorcycleGraph(self):
		assigned_edges = set()  # Set to keep track of assigned edges

		for v in self.extraordinaryVertices:
			# Place a particle on each edge incident to v
			incident_edges = self.get_incident_edges(v)
			for edge in incident_edges:
				face = self.find_face_containing_edge(edge)
				if edge not in assigned_edges and (edge[1], edge[0]) not in assigned_edges:
					particle = P.Particle(edge, v, face)
					self.particles.append(particle)
					assigned_edges.add(edge)
					self.motorcycleEdges.append(edge)

		# self.visualize_motorcycle_edges_vista(self.mesh)
		iteration = 0
		particles_to_remove = []  # List to hold particles to be removed
		while len(self.particles) != len(particles_to_remove):
			for particle in self.particles:
				if particle not in particles_to_remove:
					if particle.meets_boundary_vertex(self.boundary_vertices):
						# Stop particle
						particles_to_remove.append(particle)
					elif particle.meets_another_particles_track(self.particles):
						# Stop particle and mark stopping vertex in H
						stopping_vertex = particle.edge[1]
						self.H[particle] = stopping_vertex
						particles_to_remove.append(particle)
					elif particle.meets_multiple_particles(self.particles):
						if len(particle.met_particles) > 1:
							self.H[particle] = particle.vertex
							particles_to_remove.append(particle)
							for met_particle in particle.met_particles:
								self.H[met_particle] = met_particle.vertex
								particles_to_remove.append(met_particle)
						elif len(particle.met_particles) == 1:
							particle2 = particle.met_particles[0]
							reveresed_edge_of_particle1 = particle.edge[1], particle.edge[0]
							reveresed_edge_of_particle2 = particle2.edge[1], particle2.edge[0]
							face_of_reveresed_edge_of_particle2 = self.find_face_containing_edge(reveresed_edge_of_particle2)
							face_of_reveresed_edge_of_particle1 = self.find_face_containing_edge(reveresed_edge_of_particle1)
							if np.array_equal(face_of_reveresed_edge_of_particle2, particle.face):
								new_edge, new_face = self.get_opposite_edge_topo(particle)
								particle.move_to(new_edge, new_face)
								self.motorcycleEdges.append(new_edge)
								self.H[particle2] = particle2.vertex
								particles_to_remove.append(particle2)
							elif np.array_equal(face_of_reveresed_edge_of_particle1, particle2.face):
								self.H[particle] = particle.vertex
								particles_to_remove.append(particle)
							else:
								self.H[particle] = particle.vertex
								self.H[particle2] = particle2.vertex
								particles_to_remove.extend([particle, particle2])
					elif particle.at_interior_vertex(self.extraordinaryVertices):
						# Move particle to the opposite edge at the vertex
						new_edge, new_face = self.get_opposite_edge_topo(particle)
						particle.move_to(new_edge, new_face)
						self.motorcycleEdges.append(new_edge)
			iteration+=1
			#Remove particles marked for removal
			particles_to_remove_set = set(particles_to_remove)  # Convert to set to remove duplicates
			particles_to_remove = list(particles_to_remove_set)

		self.visualize_motorcycle_edges_vista(self.mesh)

	def get_incident_edges(self, vertex):
		incident_edges = []

		for face in self.Q:
			if vertex in face:
				idx = np.where(face == vertex)[0][0]

				# Clockwise orientation
				edge_clockwise = (face[idx], face[(idx + 1) % 4])
				if edge_clockwise not in incident_edges and (edge_clockwise[1], edge_clockwise[0]) not in incident_edges:
					incident_edges.append(edge_clockwise)

				# Counter-clockwise orientation
				edge_counter_clockwise = (face[idx], face[(idx - 1) % 4])
				if edge_counter_clockwise not in incident_edges and (edge_counter_clockwise[1], edge_counter_clockwise[0]) not in incident_edges:
					incident_edges.append(edge_counter_clockwise)

		return incident_edges

	def visualize_motorcycle_edges(self):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		for edge in self.motorcycleEdges:
			v1_idx, v2_idx = edge
			v1 = self.V[v1_idx-1] # -1 for especial cases when faces index starts from 1
			v2 = self.V[v2_idx-1] # -1 for especial cases when faces index starts from 1
			x = [v1[0], v2[0]]
			y = [v1[1], v2[1]]
			z = [v1[2], v2[2]]
			ax.plot(x, y, z, marker='o')

		ax.set_xlabel('X-axis')
		ax.set_ylabel('Y-axis')
		ax.set_zlabel('Z-axis')
		ax.set_title('Motorcycle Edges 3D Visualization')
		plt.show()

	def visualize_motorcycle_edges_vista(self, mesh):
		# Create a PyVista plotter with two viewports (1 row, 2 columns)
		plotter = pv.Plotter(shape=(1, 2), window_size=(800, 400))

		# Add the first mesh to the left viewport
		plotter.subplot(0, 0)
		plotter.add_mesh(mesh, color="cyan", show_edges=True)

		# Add the second mesh to the right viewport
		plotter.subplot(0, 1)
		plotter.add_mesh(mesh, color="white", edge_color="black", show_edges=True)

		# Create arrays for points and lines
		points = np.zeros((0, 3))
		lines = []

		# Add the motorcycle edges as lines to the arrays
		for edge in self.motorcycleEdges:
			v1_idx, v2_idx = edge
			v1 = self.V[v1_idx - 1]  # -1 for indexing
			v2 = self.V[v2_idx - 1]  # -1 for indexing
			new_line = [2, len(points), len(points) + 1]
			lines.append(new_line)
			points = np.vstack((points, [v1, v2]))

		# Convert the lines list to a numpy array
		lines = np.array(lines, dtype=int)

		# Create a PyVista PolyData object
		lines_polydata = pv.PolyData(points, lines=lines)

		plotter.add_mesh(lines_polydata, color="red", line_width=3, render_lines_as_tubes=True)

		# Show the plot
		plotter.show()

	def find_face_containing_edge(self, edge):
		v1, v2 = edge
		for face in self.Q:
			if np.any(face == v1) and np.any(face == v2):
				idx_v1 = np.where(face == v1)[0][0]
				idx_v2 = np.where(face == v2)[0][0]
				if (idx_v1 + 1) % 4 == idx_v2:
					return face
		return None  # Return None if no such face is found

	def find_edge_index_in_face(self, face, edge):
		for i in range(4):
			if (face[i], face[(i + 1) % 4]) == edge:
				return i
		return None  # Return None if edge is not found in the face

	def get_opposite_edge_topo(self, particle):
		current_face = particle.face #self.find_face_containing_edge(particle.edge)
		idx_current_edge = self.find_edge_index_in_face(current_face, particle.edge)
		next_edge = current_face[(idx_current_edge+1)%4], current_face[(idx_current_edge+2)%4]
		reverse_of_next_edge = (next_edge[1], next_edge[0])
		new_face = self.find_face_containing_edge(reverse_of_next_edge)
		idx_reverse_of_next_edge = self.find_edge_index_in_face(new_face, reverse_of_next_edge)
		opposite_edge = new_face[(idx_reverse_of_next_edge+1)%4], new_face[(idx_reverse_of_next_edge+2)%4]

		return opposite_edge, new_face

	def visualize_loops_as_lines(self, mesh, loop):
		# Create a PyVista plotter with two viewports (1 row, 2 columns)
		plotter = pv.Plotter(shape=(1, 2), window_size=(800, 600))

		# Add the first mesh to the left viewport
		plotter.subplot(0, 0)
		plotter.add_mesh(mesh, color="white", edge_color="black", show_edges=True)

		# Create arrays for points and lines
		points = np.zeros((0, 3))
		lines = []

		# Add the motorcycle edges as lines to the arrays
		for edge in self.motorcycleEdges:
			v1_idx, v2_idx = edge
			v1 = self.V[v1_idx - 1]  # -1 for indexing
			v2 = self.V[v2_idx - 1]  # -1 for indexing
			new_line = [2, len(points), len(points) + 1]
			lines.append(new_line)
			points = np.vstack((points, [v1, v2]))

		# Convert the lines list to a numpy array
		lines = np.array(lines, dtype=int)

		# Create a PyVista PolyData object
		lines_polydata = pv.PolyData(points, lines=lines)

		plotter.add_mesh(lines_polydata, color="red", line_width=3, render_lines_as_tubes=True)


		# Add the second mesh to the right viewport
		plotter.subplot(0, 1)
		# Create arrays for points and lines
		points = np.zeros((0, 3))
		lines = []

		# Add the edges of the unique loops as lines to the arrays

		for i in range(len(loop)):
			v1_idx = loop[i]
			v2_idx = loop[(i + 1) % len(loop)]  # Connect back to the first vertex to form a loop
			v1 = self.V[v1_idx-1]
			v2 = self.V[v2_idx-1]
			new_line = [2, len(points), len(points) + 1]
			lines.append(new_line)
			points = np.vstack((points, [v1, v2]))

		# Convert the lines list to a numpy array
		lines = np.array(lines, dtype=int)

		# Create a PyVista PolyData object
		lines_polydata = pv.PolyData(points, lines=lines)

		plotter.add_mesh(mesh, color="white", edge_color="black", show_edges=True)
		# Add the loops as red lines
		plotter.add_mesh(lines_polydata, color="blue", line_width=3, render_lines_as_tubes=True)

		# Show the plot
		plotter.show()


	def save_motorcycle_edges_info(self, mesh_name):

		motorcycle_edges = self.motorcycleEdges
		vertices = self.V
		# Define the file path
		file_path = f"MotorCycleEdges_{mesh_name}.txt"

		# Open the file for writing
		with open(file_path, "w") as file:
			# Write the title
			file.write(f"// File contains the MotorCycle edges of mesh '{mesh_name}'\n")
			# Write motorcycle edges
			file.write(f"\nMotorcycle Edges: {len(motorcycle_edges)}\n")
			for edge in motorcycle_edges:
				v1, v2 = edge
				file.write(f"e {v1} {v2}\n")

	def write_extraOrdinary_vertices(self, mesh_name):

		file_path = f"extraOrdinaryVerticesOf_{mesh_name}.txt"
		with open(file_path, 'w') as file:
			# Write the header
			file.write(f'// Extra Ordinary vertices of "{mesh_name}.obj"\n\n')

			# Write submesh faces
			file.write('// extraOrdinary vertices size: \n')
			file.write(f'f {len(self.extraordinaryVertices)}\n')
			for vertexInx in self.extraordinaryVertices:
				file.write(f'f {vertexInx}\n')
			file.write('\n')
