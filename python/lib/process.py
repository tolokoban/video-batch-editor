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


UNIPOLAR = [[0,0,0],[0.003921568859368563,0.003921568859368563,0.12941177189350128],[0.007843137718737125,0.007843137718737125,0.25882354378700256],[0.0117647061124444,0.0117647061124444,0.3921568691730499],[0.01568627543747425,0.01568627543747425,0.5215686559677124],[0.019607843831181526,0.019607843831181526,0.6549019813537598],[0.03529411926865578,0.0784313753247261,0.686274528503418],[0.0470588244497776,0.13333334028720856,0.7215686440467834],[0.05882352963089943,0.1882352977991104,0.7568627595901489],[0.07450980693101883,0.24705882370471954,0.7882353067398071],[0.08627451211214066,0.3019607961177826,0.8235294222831726],[0.09803921729326248,0.3607843220233917,0.8588235378265381],[0.11372549086809158,0.4156862795352936,0.8901960849761963],[0.125490203499794,0.47058823704719543,0.9254902005195618],[0.13725490868091583,0.529411792755127,0.95686274766922],[0.21960784494876862,0.46666666865348816,0.8745098114013672],[0.3019607961177826,0.40392157435417175,0.7960784435272217],[0.3843137323856354,0.34117648005485535,0.7137255072593689],[0.48235294222831726,0.2862745225429535,0.5960784554481506],[0.5764706134796143,0.22745098173618317,0.47843137383461],[0.6705882549285889,0.16862745583057404,0.364705890417099],[0.7686274647712708,0.11372549086809158,0.24705882370471954],[0.8627451062202454,0.054901961237192154,0.13333334028720856],[0.95686274766922,0,0.01568627543747425],[0.95686274766922,0.019607843831181526,0.01568627543747425],[0.9529411792755127,0.04313725605607033,0.01568627543747425],[0.9490196108818054,0.06666667014360428,0.01568627543747425],[0.9450980424880981,0.08627451211214066,0.01568627543747425],[0.9411764740943909,0.10980392247438431,0.01568627543747425],[0.9372549057006836,0.13333334028720856,0.0117647061124444],[0.9333333373069763,0.1568627506494522,0.0117647061124444],[0.9333333373069763,0.1764705926179886,0.0117647061124444],[0.929411768913269,0.20000000298023224,0.0117647061124444],[0.9254902005195618,0.2235294133424759,0.0117647061124444],[0.9215686321258545,0.24705882370471954,0.0117647061124444],[0.9176470637321472,0.2666666805744171,0.007843137718737125],[0.9137254953384399,0.29019609093666077,0.007843137718737125],[0.9098039269447327,0.3137255012989044,0.007843137718737125],[0.9098039269447327,0.33725491166114807,0.007843137718737125],[0.9058823585510254,0.35686275362968445,0.007843137718737125],[0.9019607901573181,0.3803921639919281,0.007843137718737125],[0.8980392217636108,0.40392157435417175,0.003921568859368563],[0.8941176533699036,0.42352941632270813,0.003921568859368563],[0.8901960849761963,0.4470588266849518,0.003921568859368563],[0.886274516582489,0.47058823704719543,0.003921568859368563],[0.8823529481887817,0.4941176474094391,0.003921568859368563],[0.8823529481887817,0.5137255191802979,0.003921568859368563],[0.8784313797950745,0.5372549295425415,0],[0.8745098114013672,0.5607843399047852,0],[0.8705882430076599,0.5843137502670288,0],[0.8666666746139526,0.6039215922355652,0],[0.8627451062202454,0.6274510025978088,0],[0.8588235378265381,0.6509804129600525,0],[0.8588235378265381,0.6745098233222961,0],[0.8588235378265381,0.6823529601097107,0.01568627543747425],[0.8627451062202454,0.6901960968971252,0.03529411926865578],[0.8666666746139526,0.7019608020782471,0.05098039284348488],[0.8705882430076599,0.7098039388656616,0.07058823853731155],[0.8705882430076599,0.7176470756530762,0.08627451211214066],[0.8745098114013672,0.729411780834198,0.10588235408067703],[0.8784313797950745,0.7372549176216125,0.125490203499794],[0.8823529481887817,0.7450980544090271,0.1411764770746231],[0.8823529481887817,0.7568627595901489,0.16078431904315948],[0.886274516582489,0.7647058963775635,0.1764705926179886],[0.8901960849761963,0.7764706015586853,0.19607843458652496],[0.8941176533699036,0.7843137383460999,0.21568627655506134],[0.8980392217636108,0.7921568751335144,0.23137255012989044],[0.8980392217636108,0.8039215803146362,0.250980406999588],[0.9019607901573181,0.8117647171020508,0.2666666805744171],[0.9058823585510254,0.8196078538894653,0.2862745225429535],[0.9098039269447327,0.8313725590705872,0.30588236451148987],[0.9098039269447327,0.8392156958580017,0.32156863808631897],[0.9137254953384399,0.8509804010391235,0.34117648005485535],[0.9176470637321472,0.8588235378265381,0.35686275362968445],[0.9215686321258545,0.8666666746139526,0.3764705955982208],[0.9215686321258545,0.8784313797950745,0.3960784375667572],[0.9254902005195618,0.886274516582489,0.4117647111415863],[0.929411768913269,0.8941176533699036,0.4313725531101227],[0.9333333373069763,0.9058823585510254,0.4470588266849518],[0.9372549057006836,0.9137254953384399,0.46666666865348816],[0.9372549057006836,0.9254902005195618,0.48627451062202454],[0.9411764740943909,0.9333333373069763,0.501960813999176],[0.9450980424880981,0.9411764740943909,0.5215686559677124],[0.9490196108818054,0.9529411792755127,0.5372549295425415],[0.9490196108818054,0.9607843160629272,0.5568627715110779],[0.9529411792755127,0.9686274528503418,0.5764706134796143],[0.95686274766922,0.9803921580314636,0.5921568870544434],[0.9607843160629272,0.9882352948188782,0.6117647290229797],[0.9647058844566345,1,0.6274510025978088],[0.9647058844566345,1,0.6392157077789307],[0.9647058844566345,1,0.6470588445663452],[0.9647058844566345,1,0.658823549747467],[0.9647058844566345,1,0.6666666865348816],[0.9686274528503418,1,0.6745098233222961],[0.9686274528503418,1,0.686274528503418],[0.9686274528503418,1,0.6941176652908325],[0.9686274528503418,1,0.7019608020782471],[0.9725490212440491,1,0.7137255072593689],[0.9725490212440491,1,0.7215686440467834],[0.9725490212440491,1,0.729411780834198],[0.9725490212440491,1,0.7411764860153198],[0.9725490212440491,1,0.7490196228027344],[0.9764705896377563,1,0.7568627595901489],[0.9764705896377563,1,0.7686274647712708],[0.9764705896377563,1,0.7764706015586853],[0.9764705896377563,1,0.7843137383460999],[0.9803921580314636,1,0.7960784435272217],[0.9803921580314636,1,0.8039215803146362],[0.9803921580314636,1,0.8117647171020508],[0.9803921580314636,1,0.8235294222831726],[0.9803921580314636,1,0.8313725590705872],[0.9843137264251709,1,0.843137264251709],[0.9843137264251709,1,0.8509804010391235],[0.9843137264251709,1,0.8588235378265381],[0.9843137264251709,1,0.8705882430076599],[0.9882352948188782,1,0.8784313797950745],[0.9882352948188782,1,0.886274516582489],[0.9882352948188782,1,0.8980392217636108],[0.9882352948188782,1,0.9058823585510254],[0.9882352948188782,1,0.9137254953384399],[0.9921568632125854,1,0.9254902005195618],[0.9921568632125854,1,0.9333333373069763],[0.9921568632125854,1,0.9411764740943909],[0.9921568632125854,1,0.9529411792755127],[0.9960784316062927,1,0.9607843160629272],[0.9960784316062927,1,0.9686274528503418],[0.9960784316062927,1,0.9803921580314636],[1,1,1]]


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
            f"{simulation_steps[frame_idx] / 10} ms",
            w / 2,
            16,
            align_h="C", align_v="T"
        )
        frame.save(f"{path}/{lib.util.pad(frame_idx, 5)}.jpg", "preview" in flags)
        if "preview" in flags:
            break


def generate(cfg, brayns, movie, movie_index):
    print(lib.style.info("Generating movie: ", f"{movie_index + 1} / {len(cfg['movies'])}"))
    lib.fs.clean_folder(cfg["tempFolder"])
    brayns.reset()
    model = brayns.add_model(
        movie["circuit"],
        movie["report"],
        movie["gid"]
    )
    model_id = model["id"]
    brayns.exec("set-model-transfer-function", {
        "id": model['id'],
        "transfer_function": {
            "colormap": {
                "colors": UNIPOLAR,
                "name": "unipolar"
            },
            "opacity_curve": [[0,1],[1,1]],
            "range": movie["voltageRange"]
        }
    })

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
    neuron = lib.neuron.Neuron(movie["circuit"], movie["gid"])
    camera_distance = model_bounds.diameter()
    [width, height] = cfg["resolution"]
    animation_frames = get_simulation_steps(cfg, movie)
    spp = cfg["spp"]
    print(lib.style.info(
        f"    Simulation steps from {simulation_start} to {simulation_stop}: ",
        f"{len(animation_frames)} frame(s)"
    ))
    print(lib.style.info("    Making movie for ", "CELL"))
    make_movie(
        brayns, cfg["tempFolder"], "cell",
        model_center, camera_distance,
        simulation_start, simulation_stop,
        width, height, spp,
        animation_frames
    )
    print(lib.style.info("    Making movie for ", "SOMA"))
    make_movie(
        brayns, cfg["tempFolder"], "soma",
        neuron.soma_center, camera_distance / 12,
        simulation_start, simulation_stop,
        height / 2, height / 2, spp,
        animation_frames
    )
    print(lib.style.info("    Making movie for ", "DENDRITES"))
    make_movie(
        brayns, cfg["tempFolder"], "dendrites",
        neuron.apical_dendrites_center, camera_distance / 5,
        simulation_start, simulation_stop,
        height / 2, height / 2, spp,
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


def make_movie(brayns, output_folder, prefix, camera_target, camera_distance, simulation_start, simulation_stop, width, height, spp, animation_frames):
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
        "spp": spp,
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
