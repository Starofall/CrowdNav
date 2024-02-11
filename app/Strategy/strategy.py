import traci
import csv
from statistics import mean

##need to implement this onto upisas

class CrowdNavAdaptationStrategy:
    def __init__(self, rerouting_threshold=0.4):
        self.rerouting_threshold = rerouting_threshold
        self.edge_density = {}

    def monitor(self):
        #this should be retrived from the endpoints
        for edge_id in traci.edge.getIDList():
            vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)
            density = len(vehicle_ids)
            self.edge_density[edge_id] = density

    def analyze(self):
        overloaded_streets = []
        for edge_id, density in self.edge_density.items():
            mean_density = mean(density)
            if mean_density > self.rerouting_threshold:
                overloaded_streets.append(edge_id)
        return overloaded_streets

    def plan(self, overloaded_streets):
        avoid_streets_signal = []
        for _ in range(traci.simulation.getDeltaT()):
            signal_value = 0 if traci.simulation.getCurrentEdgeID() in overloaded_streets else 1
            avoid_streets_signal.append(signal_value)
        return avoid_streets_signal

    def execute(self, avoid_streets_signal):
        if 0 in avoid_streets_signal:
            print("Sending signal to avoid overloaded streets!")
            with open('signal.target', 'w') as signal_file:
                signal_writer = csv.writer(signal_file, dialect='excel')
                signal_writer.writerow(avoid_streets_signal)

    def update_knowledge_base(self):
        # You can update the knowledge base based on the feedback from the simulation.
        # This might involve adjusting thresholds, exploring different rerouting strategies, or updating other parameters.
        pass


# Example usage
strategy = CrowdNavAdaptationStrategy()
strategy.run_strategy()
