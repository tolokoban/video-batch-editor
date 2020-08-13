#!/usr/bin/python3

from brayns import Client, CircuitExplorer
from bluepy.v2 import Circuit
from neurom.core.types import NeuriteType
import sys
import math
import time
import numpy
import json

FOCUS_FULL_MORPHOLOGY = 0
FOCUS_SOMA = 1
FOCUS_AXONS = 2
FOCUS_APICAL_DENDRITE = 3
FOCUS_BASAL_DENDRITE = 4
focus = FOCUS_FULL_MORPHOLOGY

def usage():
    print("Usage:")
    print("> python3 {0} config.json")
    print("")
    print("Where `config.json` is a JSON file that looks like this:")
    print("""
{
    "braynsHostAndPort": "r1i7n8.bbp.epfl.ch:5000",
    "circuitPath": "/gpfs/bbp.cscs.ch/project/proj42/simulations/CA1.O1.20191017/full_comportment/BlueConfig",
    "cellGID": 841,
    "report": "somas",
    "radiusMultiplier": 3,
    "resolution": [3840, 2160],
    "start": 12300,
    "stop": 12500,
    "framesOutputDirectory": "/tmp/output"
}
    """)
    sys.exit(1)

if len(sys.argv) < 2:
    usage()

config_filename = sys.argv[1]
print("========================================")
print("Configuration: ", config_filename)
config_fd = open(config_filename, 'r')
config = json.load(config_fd)
config_fd.close()
print(json.dumps(config, indent=4))
print("----------------------------------------")

def read_config_string(attribute_name):
    value = config[attribute_name]
    if value == None:
        print("Missing config attribute: ", attribute_name)
        print()
        usage()
    return value

#############################################################################
# MINIMUM REQUIRED PARAMS
# -----------------------
# We can create a txt file with a line per video and automate the generation
# Then call the script: $ python script.py <circuit path> <gid> <report> <result path>
#############################################################################
address = read_config_string("braynsHostAndPort")
circuitPath = read_config_string("circuitPath")
GID = int(read_config_string("cellGID"))
report = read_config_string("report")

############################################################################
# Optional params, can be fixed
############################################################################
frameCachePath = read_config_string("framesOutputDirectory")
generationResolution = read_config_string("resolution")
radMult = float(read_config_string("radiusMultiplier"))

# Temprary to make bluepy work on my personal computer
localCircuitPath = circuitPath#"/home/nadir/Desktop/TestDataInstall/share/BBPTestData/circuitBuilding_1000neurons/BlueConfig"

# =========================================================================================================0


#####################################################
# INITIALIZATION
#####################################################
print(f"Contacting brayns on {address}...")
brayns = Client(address)
print("Connected successfuly!")
ce = CircuitExplorer(brayns)
print("Loading circuit:", localCircuitPath)
circuit = Circuit(localCircuitPath)
print("Circuit loaded successfuly!")

ap = brayns.get_application_parameters()
brayns.set_application_parameters(engine=ap["engine"],
                                  image_stream_fps=ap["image_stream_fps"],
                                  jpeg_compression=ap["jpeg_compression"],
                                  viewport=generationResolution)

#####################################################
# COMPUTE FOCUS POINTS
#####################################################
minBounds = [9999999.9] * 3
maxBounds = [-9999999.9] * 3

somaPoints = list()
apicalDendritePoints = list()
basalDendiritePoints = list()
axonsPoints = list()

def updateBounds(p, minBound, maxBound):
    x = p[0]
    y = p[1]
    z = p[2]

    if x < minBound[0]:
        minBound[0] = x
    elif x > maxBound[0]:
        maxBound[0] = x

    if y < minBound[1]:
        minBound[1] = y
    elif y > maxBound[1]:
        maxBound[1] = y

    if z < minBound[2]:
        minBound[2] = z
    elif z > maxBound[2]:
        maxBound[2] = z

for section in circuit.morph.get(GID, True).sections:
    points = section.points
    for p in points:
        x = p[0]
        y = p[1]
        z = p[2]

        updateBounds(p, minBounds, maxBounds)

        if section.type == NeuriteType.soma:
            somaPoints.append([x, y, z])
        elif section.type == NeuriteType.apical_dendrite:
            apicalDendritePoints.append([x, y, z])
        elif section.type == NeuriteType.axon:
            axonsPoints.append([x, y, z])
        elif section.type == NeuriteType.basal_dendrite:
            basalDendiritePoints.append([x, y, z])

#print("Morphology bounds: Min " + str(minBounds) + " Max " + str(maxBounds) + "\n")

minBoundSoma = [99999999.9] * 3
maxBoundSoma = [-99999999.9] * 3
if len(somaPoints) > 0:
    for p in somaPoints:
        updateBounds(p, minBoundSoma, maxBoundSoma)
else:
    print("No soma specific bounds")
    minBoundSoma = minBounds.copy()
    maxBoundSoma = maxBounds.copy()


minBoundADend = [99999999.9] * 3
maxBoundADend = [-99999999.9] * 3
if len(apicalDendritePoints) > 0:
    for p in apicalDendritePoints:
        updateBounds(p, minBoundADend, maxBoundADend)
else:
    print("No apical dendrite specific bounds")
    minBoundADend = minBounds.copy()
    maxBoundADend = maxBounds.copy()

minBoundAxon = [99999999.9] * 3
maxBoundAxon = [-99999999.9] * 3
if len(axonsPoints) > 0:
    for p in axonsPoints:
        updateBounds(p, minBoundAxon, maxBoundAxon)
else:
    print("No axon specific bounds")
    minBoundAxon = minBounds.copy()
    maxBoundAxon = maxBounds.copy()

minBoundBDend = [99999999.9] * 3
maxBoundBDend = [-99999999.9] * 3
if len(basalDendiritePoints):
    for p in basalDendiritePoints:
        updateBounds(p, minBoundBDend, maxBoundBDend)
else:
    print("No basal dendrite specific bounds")
    minBoundBDend = minBounds.copy()
    maxBoundBDend = maxBounds.copy()


#####################################################
# LOAD CIRCUIT
#####################################################

print("Removing all models of the current scene...")
brayns.get_scene()
if len(brayns.scene.models) > 0:
    toRemove = list()
    for m in brayns.scene.models:
        toRemove.append(m["id"])
    brayns.remove_model(toRemove)

print("Loading Model...")
print("    path:", json.dumps(circuitPath))
print("    gids:", json.dumps(GID))
print("    radius_multiplier:", json.dumps(radMult))

# r = ce.load_circuit(path=circuitPath,
#                 circuit_color_scheme=CircuitExplorer.CIRCUIT_COLOR_SCHEME_NEURON_BY_ID,
#                 density=100.0,
#                 gids=[GID],
#                 targets=["mini50"],
#                 report="voltages",
#                 mesh_filename_pattern="mesh_{gid}.obj",
#                 load_soma=True,
#                 load_axon=True,
#                 load_dendrite=True,
#                 load_apical_dendrite=True,
#                 use_sdf=True,
#                 radius_multiplier=radMult)

add_model_params = {
  "path": "/gpfs/bbp.cscs.ch/project/proj42/simulations/CA1.O1.20191017/full_comportment/BlueConfig",
  "loader_name": "Advanced circuit loader (Experimental)",
  "loader_properties": {
    "000_db_connection_string": "",
    "001_density": 1,
    "002_random_seed": 0,
    "010_targets": "",
    "011_gids": str(GID),
    "012_pre_neuron": "",
    "013_post_neuron": "",
    "020_report": "AllCompartmentsVoltage",
    "021_report_type": "Voltages from file",
    "022_user_data_type": "Simulation offset",
    "023_synchronous_mode": True,
    "024_spike_transition_time": 1,
    "030_circuit_color_scheme": "By id",
    "040_mesh_folder": "",
    "041_mesh_filename_pattern": "mesh_{gid}.obj",
    "042_mesh_transformation": False,
    "050_radius_multiplier": radMult,
    "051_radius_correction": 0,
    "052_section_type_soma": True,
    "053_section_type_axon": True,
    "054_section_type_dendrite": True,
    "055_section_type_apical_dendrite": True,
    "060_use_sdf_geometry": True,
    "061_dampen_branch_thickness_changerate": True,
    "070_realistic_soma": False,
    "071_metaballs_samples_from_soma": 5,
    "072_metaballs_grid_size": 20,
    "073_metaballs_threshold": 1,
    "080_morphology_color_scheme": "None",
    "090_morphology_quality": "High",
    "091_max_distance_to_soma": 1000000,
    "100_cell_clipping": False,
    "101_areas_of_interest": 0,
    "110_synapse_radius": 0,
    "111_load_afferent_synapses": False,
    "112_load_efferent_synapses": False
  }
}
print("Loading in progress...")
result = brayns.rockets_client.request("add-model", add_model_params)
print("Loaded successfuly!")

modelLoaded = False
while not modelLoaded:
    # Forces model update
    brayns.get_model_properties(id=result["id"])

    if len(brayns.scene.models) < 1:
        continue

    # Get information about the model
    model = brayns.scene.models[0]
    aabb_min = model['bounds']['min']
    aabb_max = model['bounds']['max']

    aabb_diag = [0, 0, 0]
    for k in range(3):
        aabb_diag[k] = aabb_max[k] - aabb_min[k]

    # Compute camera height according to model size
    height = math.sqrt(aabb_diag[0]*aabb_diag[0] + aabb_diag[1]*aabb_diag[1] + aabb_diag[2]*aabb_diag[2])
    print("Camera height:", height)
    if math.isinf(height):
        # Model is not yet committed to the 3D scene (still loading...)
        time.sleep(1)
    else:
        modelLoaded = True

time.sleep(1)

#####################################################
# FOCUS CAMERA
#####################################################

def boundsCenter(minB, maxB):
    target = [0] * 3
    for i in range(3):
        target[i] = (minB[i] + maxB[i]) * 0.5
    return target

def focusCamera(minBound, maxBound):
    cam = brayns.get_camera()
    camParams = brayns.get_camera_params()

    target = boundsCenter(minBound, maxBound)

    modelYlen = maxBound[1] - minBound[1]
    fov = math.radians(camParams["fovy"] * 0.5)
    hipoLen = (modelYlen * 0.5) / math.sin(fov)
    dist = hipoLen * math.cos(fov)

    pos = target.copy()
    pos[2] = pos[2] + dist

    print("Focusing camera...")
    brayns.set_camera(current = cam["current"],
                      orientation = [0,0,0,1],
                      target=target,
                      position=pos,
                      types=cam["types"])
    print("Camera focused successfuly!")

focus = FOCUS_FULL_MORPHOLOGY
if focus == FOCUS_FULL_MORPHOLOGY:
    focusCamera(minBounds, maxBounds)
elif focus == FOCUS_SOMA:
    focusCamera(minBoundSoma, maxBoundSoma)
elif focus == FOCUS_AXONS:
    focusCamera(minBoundAxon, maxBoundAxon)
elif focus == FOCUS_APICAL_DENDRITE:
    focusCamera(minBoundADend, maxBoundADend)
elif focus == FOCUS_BASAL_DENDRITE:
    focusCamera(minBoundBDend, maxBoundBDend)

#####################################################
# PROJECT POINTS OF INTEREST IN THE 2D PLANE
#####################################################

def projectCenterPoint(point):
    cam = brayns.get_camera()
    camParams = brayns.get_camera_params()

    # Camera position
    eye = cam["position"].copy()
    final_point = [
        point[0] - eye[0],
        point[1] - eye[1],
        point[2] - eye[2]
    ]
    # fov
    fov = camParams["fovy"]
    tan = math.tan(fov * math.pi / 180)
    scale = 1 / (tan * abs(final_point[2]))
    return [x * scale for x in final_point[:2]]

projSoma = projectCenterPoint(boundsCenter(minBoundSoma, maxBoundSoma))
projADend = projectCenterPoint(boundsCenter(minBoundADend, maxBoundADend))
projBDend = projectCenterPoint(boundsCenter(minBoundBDend, maxBoundBDend))
projAxons = projectCenterPoint(boundsCenter(minBoundAxon, maxBoundAxon))

print("Soma:", projSoma)

# f = open(resultPath+"/projections.txt", "a")
# f.write("soma="+str(projSoma)+"\n")
# f.write("adend="+str(projADend)+"\n")
# f.write("bdend="+str(projBDend)+"\n")
# f.write("axon="+str(projAxons)+"\n")
# f.flush()
# f.close()

#####################################################
# GENERATE THE FRAMES
#####################################################

animParams = brayns.get_animation_parameters()
frame_count = animParams["frame_count"]
start = config["start"]
if start == None:
    start = 0
stop = config["stop"]
if stop == None:
    stop = frame_count
elif stop < 0:
    stop = frame_count + stop

animFrames = [i for i in range(start, stop)]

cam = brayns.get_camera()
camParams = brayns.get_camera_params()

base = [cam["position"], [0,0,-1], [0,1,0], camParams["aperture_radius"], camParams["focus_distance"]]
camDefines = list()
for i in range(len(animFrames)):
        camDefines.append(base)

print(f"Exporting frames {start}-{stop} to disk...")
print("    path:", frameCachePath)
print("    frames count:", len(animFrames))
ce.export_frames_to_disk(path=frameCachePath,
                         animation_frames=animFrames,
                         camera_definitions=camDefines)
print("Looking for progression...")
progress = 0.0
while progress < 1.0:
    print(f"    Progress: {int(progress * 100)}%")
    progress = ce.get_export_frames_progress()["progress"]
    time.sleep(1)
print("Frames exported successfuly!")

#####################################################
# GENERATE THE MOVIE
#####################################################


# ce.make_movie(output_movie_path=resultPath + "/scripttest_radius_"+str(radMult)+".mp4",
#               fps_rate=30,
#               frames_folder_path=frameCachePath)
