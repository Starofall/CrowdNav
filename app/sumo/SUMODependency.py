# we need to import python modules from the $SUMO_HOME/tools directory
import os
import sys

from colorama import Fore


# checks for SUMO and adds the SUMO_HOME directory to the list of dependencies
def checkDeps():
    try:
        sys.path.append(os.environ.get("SUMO_HOME"))  # tutorial in docs
        from sumolib import checkBinary
    except ImportError:
        sys.exit("please declare environment variable 'SUMO_HOME' as the root directory"
                 " of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")