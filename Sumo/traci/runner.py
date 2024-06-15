import os
import sys
import optparse
import random


from capture import Capture 
from detect import Detect
from trafficlightcontrol import TrafficLightControl
import traci._lane

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

import time
from PIL import ImageGrab


def run():
    """execute the TraCI control loop"""
    step = 0
    red_light_time = None
    dt = Detect()
    cp = Capture()
    tlc = TrafficLightControl("J28")
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        total_time = 0
        if red_light_time == 2:
            print("Chup hinh doi pha")
            # phân loại mật độ giao thông
            screen = cp.capture_screen()
            result = dt.predict(screen)
            weight = dt.calculate_weight(result)
            if weight == 0:
                weight = 1
            if(weight < 12):
                total_time = 32 *2
                print('vang')
            elif (weight <30):
                total_time = 45 *2
                print('it')
            else:
                total_time = 60 *2
                print('dong')

        horizontal_road_image, vertical_road_image = cp.capture_road3T(screen)
        horizontal_result = dt.predict( horizontal_road_image)
        vertical_result = dt.predict( vertical_road_image)
        horizontal_weight = dt.calculate_weight(horizontal_result)
        vertical_weight = dt.calculate_weight(vertical_result)
        
        time1 = round((horizontal_weight /weight) * total_time)
        time2 = round((vertical_weight /weight) * total_time)
        phases = tlc.create_phases_3(time1, time2)
        tlc.set_traffic_light_cycle( phases)
        print("ngang:", str(horizontal_weight) +' '+ str(time1), "doc", str(vertical_weight) +' '+ str(time2))
        
        if traci.trafficlight.getPhase("J28") == 3:
            # Nếu đèn giao thông là đèn đỏ
            if red_light_time is None or red_light_time > 2:
                print(traci.trafficlight.getNextSwitch("J28") - traci.simulation.getTime())
                red_light_time = traci.trafficlight.getNextSwitch("J28") - traci.simulation.getTime()
        else:
            # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
            red_light_time = None

        step += 1
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
        
    traci.start([sumoBinary, "-c", "F:\Project\Thesis\Thesis\Sumo/traci/new/new.sumocfg"])
    run()
