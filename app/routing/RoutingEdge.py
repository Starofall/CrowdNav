from app.Util import addToAverage


class RoutingEdge:
    """ a wrapper we use to add information to an edge that we use for routing """

    # how important old data can be at maximum (x times old + 1 times new value)
    edgeAverageInfluence = 140

    def __init__(self, edge):
        """ init the edge based on a SUMO edge """
        # the edgeID
        self.id = edge.getID()
        # the number of lanes
        self.lanes = edge.getLanes()
        # the maximum speed on this edge
        self.maxSpeed = edge.getSpeed()
        # the length in meter on this edge
        self.length = edge.getLength()
        # the node this edge is from
        self.fromNode = edge.getFromNode()
        # the node this edge is to
        self.toNode = edge.getToNode()
        # the ID of the fromNode
        self.fromNodeID = edge.getFromNode().getID()
        # the ID of the toNode
        self.toNodeID = edge.getToNode().getID()
        # the theoretical duration for this edgeb based on speed and length
        self.predictedDuration = self.length / self.maxSpeed
        # averages for the duration measured in the simulation
        self.averageDuration = self.predictedDuration
        # how many averageDurations are already measured
        self.averageDurationCounter = 0
        # when did we get the last infromation
        self.lastDurationUpdateTick = 0

    def applyEdgeDurationToAverage(self, duration, tick):
        """ adds a duration to drive on this edge to the calculation """
        # VARIANTE 1
        # # if a hugh traffic happened some time ago, the new values should be more important
        oldDataInfluence = max(1, self.edgeAverageInfluence - (tick - self.lastDurationUpdateTick))
        # # self.averageDurationCounter += 1 -- not used
        self.averageDuration = addToAverage(oldDataInfluence, self.averageDuration, duration)
        # # print(str(oldDataInfluence))
        self.lastDurationUpdateTick = tick

        # VARIANTE 2
        # self.averageDurationCounter += 1
        # self.averageDuration = addToAverage(self.averageDurationCounter, self.averageDuration, duration)
        # self.lastDurationUpdateTick = tick

    def __str__(self):
        return "Edge(" + self.fromNode.getID() \
               + "," + self.toNode.getID() \
               + "," + str(len(self.lanes)) \
               + "," + str(self.maxSpeed) \
               + "," + str(self.length) + ")"
