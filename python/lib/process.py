import time
import lib.geom
import lib.style
import lib.neuron


def exec(cfg, brayns):
    movie_index = cfg["firstMovieToProcess"]
    movies = cfg["movies"]
    if movie_index >= len(movies):
        return False
    movie = movies[movie_index]
    print(lib.style.info("Processing movie: ", f"{movie_index} / {len(movies)}"))
    brayns.reset()
    model = brayns.add_model(
        movie["circuit"],
        movie["report"],
        movie["gid"]
    )
    model_id = model["id"]
    model_bounds = lib.geom.ConstBounds(
        model["bounds"]["min"],
        model["bounds"]["max"]
    )
    model_center = model_bounds.center()
    simulation_start = movie["firstSimulationStep"]
    simulation_stop = movie["lastSimulationStep"]
    if simulation_stop < simulation_start:
        simulation_stop = brayns.get_last_simulation_step()
    print(f"    Simulation steps from {simulation_start} to {simulation_stop}")
    neuron = lib.neuron.Neuron(movie["circuit"], movie["gid"])
    camera_distance = model_bounds.diameter()
    print(lib.style.info("    Making movie for ", "CELL"))
    # make_movie(
    #     brayns, cfg["tempFolder"], "cell",
    #     model_center, camera_distance,
    #     simulation_start, simulation_stop
    # )
    make_movie(
        brayns, cfg["tempFolder"], "cell",
        neuron.soma_center, camera_distance / 10,
        simulation_start, simulation_stop
    )

    #brayns.look_at(neuron.soma_center, model_bounds.diameter() / 10)

    cfg["firstMovieToProcess"] = cfg["firstMovieToProcess"] + 1
    return True

def make_movie(brayns, output_folder, prefix,
        camera_target, camera_distance,
        simulation_start, simulation_stop):
    brayns.look_at(camera_target, camera_distance)
    simulation_length = simulation_stop - simulation_start + 1
    camera_frames = brayns.get_camera_frame() * simulation_length
    animation_frames = [x for x in range(simulation_start, simulation_stop + 1)]
    brayns.exec("export-frames-to-disk", {
        "path": "output_folder",
        "spp": 10,
        "animation_frames": animation_frames,
        "camera_definitions": camera_frames
    })
    progress = 0.0
    while progress < 1.0:
        progress = brayns.get_progress()
        print(lib.style.att("        Progress: ", f"{int(progress * 100)}%"))
        time.sleep(2)
    print(lib.style.att("        Progress: ", "100%"))
