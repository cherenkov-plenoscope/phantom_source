import numpy as np
import os
import subprocess
import shutil


def propagate_photons(
    input_path,
    output_path,
    light_field_geometry_path,
    mct_propagate_raw_photons_path,
    config_path,
    random_seed=0,
):
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    mct_propagate_call = [
        mct_propagate_raw_photons_path,
        "-l",
        light_field_geometry_path,
        "-c",
        config_path,
        "-i",
        input_path,
        "-o",
        output_path,
        "--all_truth",
        "-r",
        str(random_seed),
    ]

    o_path = output_path + ".stdout.txt"
    e_path = output_path + ".stderr.txt"
    with open(o_path, "wt") as fo, open(e_path, "wt") as fe:
        rc = subprocess.call(mct_propagate_call, stdout=fo, stderr=fe)
    return rc


def write_ascii_table_of_photons(path, supports, directions, wavelengths):
    number_photons = supports.shape[0]
    photons = np.zeros(shape=(number_photons, 8))
    photons[:, 0] = np.arange(number_photons)
    photons[:, 1:4] = supports
    photons[:, 4:7] = directions
    photons[:, 7] = wavelengths
    np.savetxt(path, photons, delimiter=" ", newline="\n")
