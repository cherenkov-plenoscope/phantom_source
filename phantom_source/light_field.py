import numpy as np


def sample_2D_points_within_radius(prng, radius, size):
    rho = np.sqrt(prng.uniform(0, 1, size)) * radius
    phi = prng.uniform(0, 2 * np.pi, size)
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def make_light_field_from_line(
    prng,
    number_photons,
    line_start_x,
    line_start_y,
    line_start_z,
    line_stop_x,
    line_stop_y,
    line_stop_z,
    aperture_x,
    aperture_y,
    aperture_z,
    aperture_radius,
):
    supports = np.ones(shape=(number_photons, 3))

    line_start = np.array([line_start_x, line_start_y, line_start_z])
    line_end = np.array([line_stop_x, line_stop_y, line_stop_z])
    line_direction = line_end - line_start
    line_length = np.linalg.norm(line_direction)
    line_direction = line_direction / line_length
    alphas = prng.uniform(low=0, high=line_length, size=number_photons)
    supports = np.zeros(shape=(number_photons, 3))
    for i in range(number_photons):
        supports[i, :] = line_start + alphas[i] * line_direction

    intersections_on_disc = np.zeros(shape=(number_photons, 3))
    ix, iy = sample_2D_points_within_radius(
        prng=prng, radius=aperture_radius, size=number_photons
    )
    intersections_on_disc[:, 0] = ix + aperture_x
    intersections_on_disc[:, 1] = iy + aperture_y
    intersections_on_disc[:, 2] = aperture_z
    directions = intersections_on_disc - supports
    no = np.linalg.norm(directions, axis=1)
    directions[:, 0] /= no
    directions[:, 1] /= no
    directions[:, 2] /= no
    return supports, directions


def make_light_field_from_mesh(
    prng,
    number_photons,
    mesh_vertices,
    mesh_edges,
    aperture_x,
    aperture_y,
    aperture_z,
    aperture_radius,
):
    vertices = np.array(mesh_vertices)
    edges = np.array(mesh_edges)
    edge_lengths = np.zeros(edges.shape[0])
    for e in range(edges.shape[0]):
        edge_lengths[e] = np.linalg.norm(
            vertices[edges[e, 0]] - vertices[edges[e, 1]]
        )
    total_length = np.sum(edge_lengths)

    number_photons_on_edge = np.zeros(edges.shape[0], dtype=np.int64)
    for e in range(edges.shape[0]):
        number_photons_on_edge[e] = int(
            np.round(number_photons * edge_lengths[e] / total_length)
        )

    sups = []
    dirs = []
    for e in range(edges.shape[0]):
        supp_ed, dirs_ed = make_light_field_from_line(
            prng=prng,
            number_photons=number_photons_on_edge[e],
            line_start_x=vertices[edges[e, 0]][0],
            line_start_y=vertices[edges[e, 0]][1],
            line_start_z=vertices[edges[e, 0]][2],
            line_stop_x=vertices[edges[e, 1]][0],
            line_stop_y=vertices[edges[e, 1]][1],
            line_stop_z=vertices[edges[e, 1]][2],
            aperture_x=aperture_x,
            aperture_y=aperture_y,
            aperture_z=aperture_z,
            aperture_radius=aperture_radius,
        )
        sups.append(supp_ed)
        dirs.append(dirs_ed)

    return np.vstack(sups), np.vstack(dirs)


def make_supports_with_equal_distance_to_aperture(
    supports, directions, distance
):
    alpha = -supports[:, 2] / directions[:, 2]
    down_dirs = np.zeros(directions.shape)
    for i in range(down_dirs.shape[0]):
        down_dirs[i, :] = alpha[i] * directions[i, :]
    supports_xy = supports + down_dirs

    up_dirs = np.zeros(directions.shape)
    for i in range(up_dirs.shape[0]):
        up_dirs[i, :] = distance * directions[i, :]
    supports_up = supports_xy - up_dirs

    return supports_up
