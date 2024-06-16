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


def websters(y_crit, L, c_min, c_max, num_phases):
    """Calculate the optimal cycle length using Webster's formula."""
    Y = sum(y_crit)
    if Y > 0.85:
        Y = 0.85
    elif Y == 0.0:
        Y = 0.01

    # Compute the cycle time
    C = int(((1.5 * L*num_phases) + 5) / (1.0 - Y))
    print("C = ", C)

    # Constrain the cycle time within minimum and maximum bounds
    if C > c_max:
        C = c_max
    elif C < c_min:
        C = c_min

    return C


def run():
    """execute the TraCI control loop"""
    step = 0
    red_light_time = None
    dt = Detect()
    cp = Capture()
    lane = 4
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        if lane == 3:
            #ngã 3
            trafficlight_id = "J28"
            tlc = TrafficLightControl(trafficlight_id)
            current_phase = traci.trafficlight.getPhase(trafficlight_id)
            if red_light_time == 2:
                print("Chup hinh doi pha")
                # phân loại mật độ giao thông
                screen = cp.capture_screen()
                result = dt.predict(screen)
                weight = dt.calculate_weight(result)
                if weight == 0:
                    weight = 1
                
                if(weight < 12):
                    c_min = 20  # Minimum cycle length in seconds
                    c_max = 32*2  # Maximum cycle length in seconds
                    print('vang')
                elif (weight <30):
                    c_min = 20
                    c_max = 45*2 
                    print('it')
                else:
                    c_min = 20
                    c_max = 60*2 
                    print('dong')

                # Calculate y_crit using the updated vehicle counts
                sat_flow = 1500  # Saturation flow rate in vehicles per hour | Default = 1800
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
                L = 5  # Lost time (red + yellow) in seconds, adjust as necessary
                total_time = websters(y_crit_value, L, c_min, c_max, num_phases = 4)
                print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                

                horizontal_road_image, vertical_road_image = cp.capture_road3T(screen)
                horizontal_result = dt.predict( horizontal_road_image)
                vertical_result = dt.predict( vertical_road_image)
                horizontal_weight = dt.calculate_weight(horizontal_result)
                vertical_weight = dt.calculate_weight(vertical_result)
                
                time1 = round((horizontal_weight /weight) * total_time)
                time2 = round((vertical_weight /weight) * total_time)
                phases = tlc.create_phases_3(time1, time2)
                tlc.set_traffic_light_cycle( phases)

                print("Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "Doc", str(vertical_weight) +' time doc:'+ str(time2))
            
            if traci.trafficlight.getPhase(trafficlight_id) == 3:
                # Update vehicle counts for the current phase
                tlc.update_vehicle_counts(current_phase)
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    print(traci.trafficlight.getNextSwitch(trafficlight_id) - traci.simulation.getTime())
                    red_light_time = traci.trafficlight.getNextSwitch(trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
                red_light_time = None
                # Update vehicle counts for the current phase
                tlc.update_vehicle_counts(current_phase)
        elif lane == 4:
            # ngã 4
            trafficlight_id = "J15"
            tlc = TrafficLightControl(trafficlight_id)
            current_phase = traci.trafficlight.getPhase(trafficlight_id)
            if red_light_time == 2:
                print("Chup hinh doi pha")
                # phân loại mật độ giao thông
                screen = cp.capture_screen()
                result = dt.predict(screen)
                weight = dt.calculate_weight(result)
                if weight == 0:
                    weight = 1
                if(weight < 12):
                    c_min = 20  # Minimum cycle length in seconds
                    c_max = 32*2  # Maximum cycle length in seconds
                    print('vang')
                elif (weight <30):
                    c_min = 20
                    c_max = 45*2 
                    print('it')
                else:
                    c_min = 20
                    c_max = 60*2 
                    print('dong')

                # Calculate y_crit using the updated vehicle counts
                sat_flow = 1500  # Saturation flow rate in vehicles per hour | Default = 1800
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
                L = 5  # Lost time (red + yellow) in seconds, adjust as necessary
                total_time = websters(y_crit_value, L, c_min, c_max, num_phases = 4)
                print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                horizontal_road_image, vertical_road_image = cp.capture_road3T(screen)
                horizontal_result = dt.predict( horizontal_road_image)
                vertical_result = dt.predict( vertical_road_image)
                horizontal_weight = dt.calculate_weight(horizontal_result)
                vertical_weight = dt.calculate_weight(vertical_result)
                
                time1 = round((horizontal_weight /weight) * total_time)
                time2 = round((vertical_weight /weight) * total_time)
                phases = tlc.create_phases_4(time1, time2)
                tlc.set_traffic_light_cycle( phases)

                print("Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "Doc", str(vertical_weight) +' time doc:'+ str(time2))
            
            if traci.trafficlight.getPhase(trafficlight_id) == 3:
                # Update vehicle counts for the current phase
                tlc.update_vehicle_counts(current_phase)
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    print(traci.trafficlight.getNextSwitch(trafficlight_id) - traci.simulation.getTime())
                    red_light_time = traci.trafficlight.getNextSwitch(trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
                red_light_time = None
                # Update vehicle counts for the current phase
                tlc.update_vehicle_counts(current_phase)
        elif lane == 5:
            # ngã 5
            return
        elif lane == 6:
            #nga 6
            return
        elif lane == 7:
            # nga 7
            return     
 

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
        
    traci.start([sumoBinary, "-c", "Sumo\\traci\\new\\new.sumocfg"])
    run()
