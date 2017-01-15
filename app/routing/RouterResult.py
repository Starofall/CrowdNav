
class RouterResult:
    """ defines the result of our customRouter """
    def __init__(self, tuple,isVictim):
        # is this a victim route
        self.isVictim = isVictim
        # the list of nodes to drive to
        self.nodeList = tuple[0]
        # meta information for the route
        self.meta = tuple[1]
        # the route as list of edgeIDs
        self.route = map(lambda x: x['edgeID'], self.meta)  # type: list[str]
        # the cost for this route per edge
        self.costs = tuple[2]
        # the total cost for this route
        self.totalCost = tuple[3]
        #self.isVitimRoute = True

    def __str__(self):
        return "Routing(" + str(self.route) + "," + str(self.totalCost) + ")"
