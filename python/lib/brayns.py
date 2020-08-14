import json
import lib.style
from brayns import Client, CircuitExplorer

class Brayns:
    def __init__(self, config):
        self.config = config
        host_and_port = config["braynsHostAndPort"]
        self.connect(host_and_port)
        self.exec("set-application-parameters", {
            "viewport": config["resolution"]
        })

    def connect(self, host_and_port):
        try:
            print(lib.style.info("Connecting to Brayns service on ", host_and_port))
            self.brayns = Client(host_and_port)
        except Exception as ex:
            raise Exception(f"Unable to contact Brayns on {host_and_port}:\n{str(ex)}")

    def exec(self, name, params=None):
        try:
            if params == None:
                return self.brayns.rockets_client.request(name)
            return self.brayns.rockets_client.request(name, params)
        except Exception as ex:
            raise Exception(f"""An error occured in a Brayns' function:
  Entrypoint: {name}
  Parameters: {json.dumps(params, indent=4)}
  Error:      {str(ex)}""")

    def add_model(self, circuit, report, gid):
        add_model_params = {
          "path": circuit,
          "loader_name": "Advanced circuit loader (Experimental)",
          "loader_properties": {
            "000_db_connection_string": "",
            "001_density": 1,
            "002_random_seed": 0,
            "010_targets": "",
            "011_gids": str(gid),
            "012_pre_neuron": "",
            "013_post_neuron": "",
            "020_report": report,
            "021_report_type": "Voltages from file",
            "022_user_data_type": "Simulation offset",
            "023_synchronous_mode": True,
            "024_spike_transition_time": 1,
            "030_circuit_color_scheme": "By id",
            "040_mesh_folder": "",
            "041_mesh_filename_pattern": "mesh_{gid}.obj",
            "042_mesh_transformation": False,
            "050_radius_multiplier": self.config["somaScale"],
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
        print(lib.style.att("    Loading circuit", circuit))
        model = self.exec("add-model", add_model_params)
        print(lib.style.att("    Model's ID", model["id"]))
        return model

    def get_last_simulation_step(self):
        anim_params = self.exec("get-animation-parameters", {})
        return anim_params["frame_count"] - 1

    def get_camera_frame(self):
        camera = self.exec("get-camera", {})
        camera_params = self.exec("get-camera-params", {})
        return [
            camera["position"],
            [0, 0, -1],
            [0, 1, 0],
            camera_params["aperture_radius"],
            camera_params["focus_distance"]
        ]

    def get_progress(self):
        plugin = CircuitExplorer(self.brayns)
        result = plugin.get_export_frames_progress()
        return result["progress"]

    def look_at(self, target, distance):
        print(lib.style.att("        Look at:", { "target": target, "distance": distance }))
        position = [
            target[0],
            target[1],
            target[2] + distance
        ]
        self.exec("set-camera", {
            "current": "perspective",
            "orientation": [0,0,0,1],
            "target": target,
            "position": position
        })

    def reset(self):
        print("    Reseting the scene")
        self.brayns.get_scene()
        if len(self.brayns.scene.models) > 0:
            toRemove = list()
            for model in self.brayns.scene.models:
                toRemove.append(model["id"])
            print(lib.style.att("        Models to remove", toRemove))
            self.brayns.remove_model(toRemove)
