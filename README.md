# CrowdNav

![Banner](https://raw.githubusercontent.com/Starofall/CrowdNav/master/banner.PNG)


### Description
CrowdNav is a simulation based on SUMO and TraCI that implements a custom router
that can be configured using kafka messages or local JSON config on the fly while the simulation is running.
Also runtime data is send to a kafka queue to allow stream processing and logger locally to CSV.

### Minimal Setup
* Download the CrowdNav code
* Run `python setup.py install` to download all dependencies 
* Install [SUMO](http://sumo.dlr.de) & set env var SUMO_HOME
* Install [Kafka](https://kafka.apache.org/) and set kafkaHost in Config.py
* Run `python run.py`

### Operational Modes

* Normal mode (`python run.py`) with UI to Debug the application. Runs forever.
* Parallel mode (`python parallel.py n`) to let n processes of SUMO spawn for faster data generation.
  Stops after 10k ticks and reports values.
  
### Further customization

* Runtime variables are in the knobs.json file and will only be used if `kafkaUpdates = True
` is set to false in `Config.py`. Else the tool uses Kafka for value changes.
* To disable the UI in normal mode, change the `sumoUseGUI = True` value in `Config.py` to false.

### Notes

* To let the system stabalize, no message is sent to kafka or CSV in the first 1000 ticks .