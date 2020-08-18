import os
import json
import math
import time
import lib.fs
import lib.geom
import lib.util
import lib.paint
import lib.style
import lib.neuron


def exec(cfg, brayns, flags):
    movie_index = cfg["firstMovieToProcess"]
    movies = cfg["movies"]
    if movie_index >= len(movies):
        return False
    movie = movies[movie_index]

    if not "preview" in flags:
        generate(cfg, brayns, movie, movie_index)

    simulation_steps = get_simulation_steps(cfg, movie)
    compose(cfg, movie, simulation_steps, flags)

    movie_path = movie["outputFilename"]
    print(lib.style.info("    Rendering movie in ", movie_path))
    command = f"ffmpeg -hide_banner -loglevel warning -y -framerate 30 -i \"{cfg['tempFolder']}/final/%05d.jpg\" -c:v libx264 -crf 23 -profile:v high -pix_fmt yuv420p -color_primaries 1 -color_trc 1 -colorspace 1 -movflags +faststart -an \"{movie_path}\""
    os.system(command)

    cfg["firstMovieToProcess"] = cfg["firstMovieToProcess"] + 1
    return True


def compose(cfg, movie, simulation_steps, flags):
    frames_count = len(simulation_steps)
    print(lib.style.info("    Compositing ", f"{frames_count} frame(s)"))
    path = f"{cfg['tempFolder']}/final"
    lib.fs.clean_folder(path)
    for frame_idx in range(frames_count):
        (w, h) = cfg["resolution"]
        frame_name = f"{lib.util.pad(frame_idx, 5)}.png"
        frame = lib.paint.Paint(w, h)
        frame.paint_image("./gfx/background.jpg")
        frame.paint_image(f"{cfg['tempFolder']}/cell/{frame_name}")
        size = h / 2
        margin = 8
        crop = (0, margin / 2, size, size - margin)
        frame.paint_image("./gfx/zoom-back.png", w - size, 0, crop=crop)
        frame.paint_image(f"{cfg['tempFolder']}/soma/{frame_name}", w - size, 0, crop=crop)
        frame.paint_image("./gfx/zoom-back.png", w - size, size + margin, crop=crop)
        frame.paint_image(f"{cfg['tempFolder']}/dendrites/{frame_name}", w - size, size + margin, crop=crop)
        frame.paint_image("./gfx/colorbar.49x369.png", 8, h / 2 - 185)
        (v_min, v_max) = movie["voltageRange"]
        frame.print(f"{v_max} mV", 60, h / 2 - 185, align_v="C")
        frame.print(f"{v_min} mV", 60, h / 2 - 185 + 369, align_v="C")
        frame.printTitle(movie["title"], 16, 16)
        frame.printSubTitle(movie["subTitle"], 16, 48)
        frame.print(
            f"({simulation_steps[frame_idx] / 10} ms)",
            w / 2,
            16,
            align_h="C", align_v="T"
        )
        frame.save(f"{path}/{lib.util.pad(frame_idx, 5)}.jpg", "preview" in flags)
        if "preview" in flags:
            break


def generate(cfg, brayns, movie, movie_index):
    print(lib.style.info("Generating movie: ", f"{movie_index} / {len(cfg['movies'])}"))
    lib.fs.clean_folder(cfg["tempFolder"])
    brayns.reset()
    model = brayns.add_model(
        movie["circuit"],
        movie["report"],
        movie["gid"]
    )
    model_id = model["id"]
    brayns.set_material(
        model_id,
        cfg["materialSpecularExponent"],
        cfg["materialGlossiness"],
        cfg["materialEmission"]
    )
    model_bounds = lib.geom.ConstBounds(
        model["bounds"]["min"],
        model["bounds"]["max"]
    )
    model_center = model_bounds.center()
    simulation_start = movie["firstSimulationStep"]
    simulation_stop = movie["lastSimulationStep"]
    print(f"    Simulation steps from {simulation_start} to {simulation_stop}")
    neuron = lib.neuron.Neuron(movie["circuit"], movie["gid"])
    camera_distance = model_bounds.diameter()
    [width, height] = cfg["resolution"]
    animation_frames = get_simulation_steps(cfg, movie)
    print(lib.style.info("    Making movie for ", "CELL"))
    make_movie(
        brayns, cfg["tempFolder"], "cell",
        model_center, camera_distance,
        simulation_start, simulation_stop,
        width, height,
        animation_frames
    )
    print(lib.style.info("    Making movie for ", "SOMA"))
    make_movie(
        brayns, cfg["tempFolder"], "soma",
        neuron.soma_center, camera_distance / 12,
        simulation_start, simulation_stop,
        height / 2, height / 2,
        animation_frames
    )
    print(lib.style.info("    Making movie for ", "DENDRITES"))
    make_movie(
        brayns, cfg["tempFolder"], "dendrites",
        neuron.apical_dendrites_center, camera_distance / 5,
        simulation_start, simulation_stop,
        height / 2, height / 2,
        animation_frames
    )


def get_simulation_steps(cfg, movie):
    fps = cfg["fps"]
    duration = movie["duration"]
    simulation_start = movie["firstSimulationStep"]
    simulation_stop = movie["lastSimulationStep"]
    frames_count = math.ceil(fps * duration)
    last = frames_count - 1
    size = simulation_stop - simulation_start + 1
    return [math.floor(simulation_start + size * n / last) for n in range(frames_count)]


def make_movie(brayns, output_folder, prefix, camera_target, camera_distance, simulation_start, simulation_stop, width, height, animation_frames):
    path = f"{output_folder}/{prefix}"
    lib.fs.clean_folder(path)
    print(lib.style.att("        resolution", [width, height]))
    brayns.exec("set-application-parameters", {
        "viewport": [width, height]
    })
    brayns.look_at(camera_target, camera_distance)
    simulation_length = len(animation_frames)
    camera_frame = brayns.get_camera_frame()
    camera_frames = []
    for i in range(simulation_length):
        for v in camera_frame:
            camera_frames.append(v)
    params = {
        "path": path,
        "format": "png",
        "quality": 100,
        "spp": 50,
        "start_frame": 0,
        "animation_information": animation_frames,
        "camera_information": camera_frames
    }
    result = brayns.exec("export-frames-to-disk", params)
    if result != None:
        print(lib.style.att("        result", result))
    progress = 0.0
    while progress < 1.0:
        progress = brayns.get_progress()
        if progress < 1.0:
            print(lib.style.att("        Progress: ", f"{int(progress * 100)}%"))
        time.sleep(2)
    print(lib.style.att("        Progress: ", "100%"))
