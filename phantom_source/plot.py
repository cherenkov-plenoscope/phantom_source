import numpy as np


def ax3d_add_mesh(
    ax3d, vertices, edges, color="b",
):
    for e in edges:
        ax3d.plot(
            xs=[vertices[e[0], 0], vertices[e[1], 0]],
            ys=[vertices[e[0], 1], vertices[e[1], 1]],
            zs=[vertices[e[0], 2], vertices[e[1], 2]],
            color=color,
        )


def ax_add_mesh(
    ax, vertices, edges, color="b",
):
    for e in edges:
        ax.plot(
            [vertices[e[0], 0], vertices[e[1], 0]],
            [vertices[e[0], 1], vertices[e[1], 1]],
            color=color,
        )


def save_view(path, figsize=(12, 16), dpi=200, elev=5, azim=-45, zlabel=None):
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax3d = fig.add_subplot(111, projection="3d")
    xy_radius = 0.4
    max_object_distance = 25
    ax3d_add_mesh(ax3d, triangle_vertices * 1e-3, triangle_edges, "k")
    ax3d_add_mesh(ax3d, spiral_vertices * 1e-3, spiral_edges, "k")
    ax3d_add_mesh(ax3d, sun_vertices * 1e-3, sun_edges, "k")
    ax3d_add_mesh(ax3d, smiley_vertices * 1e-3, smiley_edges, "k")
    ax3d_add_mesh(ax3d, cross_vertices * 1e-3, cross_edges, "k")
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [0, max_object_distance]:
                ax3d.plot(xs=[x * xy_radius], ys=[y * xy_radius], zs=[z])
    ax3d.set_xlabel(r"$x$/km")
    ax3d.set_ylabel(r"$y$/km")
    ax3d.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax3d.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax3d.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    if zlabel:
        ax3d.set_zlabel(r"depth $g$/km")
    else:
        ax3d.set_zticks([])
    ax3d.view_init(elev=elev, azim=azim)
    fig.savefig(path)


def save_projection(vertices, edges, path):
    fig = plt.figure(figsize=(2, 1.75), dpi=400)
    ax = fig.add_axes((0.3, 0.3, 0.7, 0.7))
    ax_add_mesh(ax, vertices, edges, "k")
    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$/m")
    ax.set_ylabel(r"$y$/m")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.grid(color="k", linestyle="-", linewidth=0.66, alpha=0.1)
    fig.savefig(path)
