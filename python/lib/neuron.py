import lib.geom
from bluepy.v2 import Circuit, Simulation
from neurom.core.types import NeuriteType


class Neuron:
    def __init__(self, circuit_path, report, gid, spike_duration):
        """Get needed info about a neuron

        Params:
            * circuit_path
            * report: report's name (most of the time, its "somas")
            * gid: Cell ID
            * spike_duration: Spike's event duration in seconds.

        Self attributes:
            * soma_center
            * apical_dendrites_center
            * basal_dendrites_center
            * axon_center

            * simulation_start
            * simulation_end
            * step_duration: Time between two steps in seconds.
        """
        circuit = Circuit(circuit_path)
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

        simulation = Simulation(circuit_path)
        reportObj = simulation.report(report)
        reportStart = reportObj.meta['start_time']
        reportEnd = reportObj.meta['end_time']
        reportDt = reportObj.meta['time_step']
        cellSpikeReport = simulation.spikes.get_gid(gid)

        self.step_duration = reportDt
        if len(cellSpikeReports) == 0:
            self.simulation_start = reportStart
            self.simulation_end = reportEnd
        else:
            recordStart = max(reportStart, cellSpikeReport[0] - spike_duration / 2)
            recordEnd = min(reportEnd, cellSpikeReport[0] + spike_duration / 2)
            self.simulation_start = int(math.floor(recordStart / reportDt))
            self.simulation_end = int(math.floor(recordEnd / reportDt))
