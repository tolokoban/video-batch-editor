from brayns import Client as BraynsClient

class Brayns:
    def __init__(self, host):
        self.client = BraynsClient(host)

    def add_model(self, params):
        return self.client.rockets_client.request(
            "add-model",
            params)

api = Brayns("r2i0n29.bbp.epfl.ch:21552")

result = api.add_model({
    "path": "/gpfs/bbp.cscs.ch/project/proj42/simulations/CA1.O1.20191017/full_comportment/BlueConfig",
    "loader_name": "Advanced circuit loader (Experimental)",
    "loader_properties": {
        "000_db_connection_string": "",
        "001_density": 1,
        "002_random_seed": 0,
        "010_targets": "",
        "011_gids": "841",
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
        "050_radius_multiplier": 3,
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
})

print(result)
