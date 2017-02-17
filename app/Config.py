#
# Config file for SUMOS
#

# should use kafka for config changes (else it uses json file)
kafkaUpdates = True

# the kafka host we want to send our messages to
kafkaHost = "kafka:9092"

# the topic we send the kafka messages to
kafkaTopicTrips = "crowd-nav-trips"
kafkaTopicPerformance = "crowd-nav-performance"
kafkaTopicRouting = "crowd-nav-routing"

# where we recieve system changes
kafkaCommandsTopic = "crowd-nav-commands"

# True if we want to use the SUMO GUI (always of in parallel mode)
sumoUseGUI = True  # False

# The network config (links to the net) we use for our simulation
sumoConfig = "./app/map/eichstaedt.sumo.cfg"

# The network net we use for our simulation
sumoNet = "./app/map/eichstaedt.net.xml"

# the total number of cars we use in our simulation
totalCarCounter = 600

# percentage of cars that are smart
smartCarPercentage = 0.1

# runtime dependent variable
processID = 0
parallelMode = False
