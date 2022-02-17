from . import light_field
from . import merlict
from . import plot

import numpy as np


def length_of_mesh(vertices, edges):
    length = 0
    for edge in edges:
        length += np.linalg.norm(vertices[edge[0]] - vertices[edge[1]])
    return length


def make_mesh_triangle(x, y, z, radius):
    r = radius
    vertices = np.array(
        [
            [
                x + r * np.cos(2 * np.pi * 0.25),
                y + r * np.sin(2 * np.pi * 0.25),
                z,
            ],
            [
                x + r * np.cos(2 * np.pi * 0.5833),
                y + r * np.sin(2 * np.pi * 0.5833),
                z,
            ],
            [
                x + r * np.cos(2 * np.pi * 0.9166),
                y + r * np.sin(2 * np.pi * 0.9166),
                z,
            ],
        ]
    )

    edges = np.array([[0, 1], [1, 2], [2, 0]])
    return vertices, edges


def make_mesh_spiral(x, y, z, turns, outer_radius, fn=110):
    azimuth = np.linspace(0, turns * 2 * np.pi, fn, endpoint=False)
    radius = np.linspace(0, outer_radius, fn)

    vertices = []
    edges = []

    for n in range(fn - 1):
        radius_s = z * radius[n]
        azimuth_s = azimuth[n]
        vertex_s = [
            x + np.cos(azimuth_s) * radius_s,
            y + np.sin(azimuth_s) * radius_s,
            z,
        ]

        radius_e = z * radius[n + 1]
        azimuth_e = azimuth[n + 1]
        vertex_e = [
            x + np.cos(azimuth_e) * radius_e,
            y + np.sin(azimuth_e) * radius_e,
            z,
        ]

        vertices.append(vertex_s)
        vertices.append(vertex_e)
        edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices = np.array(vertices)
    edges = np.array(edges)

    return vertices, edges


def make_mesh_sun(x, y, z, radius, num_flares, fn=50):
    number_flares_sun = 11

    vertices = []
    edges = []

    azimuths = np.linspace(0, 2 * np.pi, fn)
    for n in range(fn - 1):
        start_vertex = [
            x + radius * np.cos(azimuths[n]),
            y + radius * np.sin(azimuths[n]),
            z,
        ]
        end_vertex = [
            x + radius * np.cos(azimuths[n + 1]),
            y + radius * np.sin(azimuths[n + 1]),
            z,
        ]
        vertices.append(start_vertex)
        vertices.append(end_vertex)
        edges.append([len(vertices) - 2, len(vertices) - 1])

    azimuths_flares = np.linspace(0, 2 * np.pi, num_flares, endpoint=False)

    for n in range(num_flares):
        az = azimuths_flares[n]
        start_vertex = [
            x + 1.1 * radius * np.cos(az),
            y + 1.1 * radius * np.sin(az),
            z,
        ]
        end_vertex = [
            x + 1.4 * radius * np.cos(az),
            y + 1.4 * radius * np.sin(az),
            z,
        ]
        vertices.append(start_vertex)
        vertices.append(end_vertex)
        edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices = np.array(vertices)
    edges = np.array(edges)
    return vertices, edges


def make_mesh_cross(x, y, z, radius):
    vertices = []
    edges = []

    vertices.append([x + radius, y + radius, z])
    vertices.append([x - radius, y - radius, z])
    edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices.append([x - radius, y + radius, z])
    vertices.append([x - radius * 0.1, y + radius * 0.1, z])
    edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices.append([x + radius, y - radius, z])
    vertices.append([x + radius * 0.1, y - radius * 0.1, z])
    edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices = np.array(vertices)
    edges = np.array(edges)

    return vertices, edges


def make_mesh_smiley(x, y, z, radius, fn=50):
    vertices = []
    edges = []

    azimuths = np.linspace(0, 2 * np.pi, fn)

    # face
    for n in range(fn - 1):
        start_vertex = [
            x + radius * np.cos(azimuths[n]),
            y + radius * np.sin(azimuths[n]),
            z,
        ]
        end_vertex = [
            x + radius * np.cos(azimuths[n + 1]),
            y + radius * np.sin(azimuths[n + 1]),
            z,
        ]
        vertices.append(start_vertex)
        vertices.append(end_vertex)
        edges.append([len(vertices) - 2, len(vertices) - 1])

    # mouth
    for n in range((fn - 1) // 2):
        start_vertex = [
            x + 0.7 * radius * np.cos(np.pi + azimuths[n]),
            y + 0.7 * radius * np.sin(np.pi + azimuths[n]),
            z,
        ]
        end_vertex = [
            x + 0.7 * radius * np.cos(np.pi + azimuths[n + 1]),
            y + 0.7 * radius * np.sin(np.pi + azimuths[n + 1]),
            z,
        ]
        vertices.append(start_vertex)
        vertices.append(end_vertex)
        edges.append([len(vertices) - 2, len(vertices) - 1])

    # eyes
    vertices.append([x + radius * 0.25, y + 0, z])
    vertices.append([x + radius * 0.25, y + radius * 0.5, z])
    edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices.append([x - radius * 0.25, y + 0, z])
    vertices.append([x - radius * 0.25, y + radius * 0.5, z])
    edges.append([len(vertices) - 2, len(vertices) - 1])

    vertices = np.array(vertices)
    edges = np.array(edges)

    return vertices, edges
