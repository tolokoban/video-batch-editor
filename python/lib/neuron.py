import lib.geom
from bluepy.v2 import Circuit
from neurom.core.types import NeuriteType


class Neuron:
    def __init__(self, circuitPath, gid):
        circuit = Circuit(circuitPath)
        soma_bounds = lib.geom.Bounds()
        apical_dendrites_bounds = lib.geom.Bounds()
        basal_dendrites_bounds = lib.geom.Bounds()
        axon_bounds = lib.geom.Bounds()
        sections = circuit.morph.get(gid, True).sections
        for section in sections:
            points = section.points
            for point in points:
                if section.type == NeuriteType.soma:
                    soma_bounds.add(point)
                elif section.type == NeuriteType.apical_dendrite:
                    apical_dendrites_bounds.add(point)
                elif section.type == NeuriteType.axon:
                    axon_bounds.add(point)
                elif section.type == NeuriteType.basal_dendrite:
                    basal_dendrites_bounds.add(point)
        self.soma_center = soma_bounds.center()
        self.apical_dendrites_center = apical_dendrites_bounds.center()
        self.basal_dendrites_center = basal_dendrites_bounds.center()
        self.axon_center = axon_bounds.center()
