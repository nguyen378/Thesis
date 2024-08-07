import os
import sys
import optparse


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

    # Constrain the cycle time within minimum and maximum bounds
    if C > c_max:
        C = c_max
    elif C < c_min:
        C = c_min

    return C
   
def get_edge(tlc):
    """Retrieve the number of edges connected to a given traffic light junction."""
    # Retrieve all links connected to the junction
    links = traci.trafficlight.getControlledLinks(tlc.trafficlight_id)
    
    # Initialize a set to store unique edges
    edges = set()
    
    # Loop through each tuple of links (each can contain multiple links if there are several signal groups)
    for link_tuple in links:
        for link in link_tuple:
            # Each link is a tuple (incomingEdge, outgoingEdge, viaLane)
            incoming_edge, outgoing_edge, _ = link
            edges.add(incoming_edge)
            edges.add(outgoing_edge)
    
    # Return the number of unique edges
    return len(edges)

def get_traffic_light_phases(tls_id):
    """Retrieve the number of phases for a specified traffic light controller."""
    # Retrieve the traffic light logic
    logic = traci.trafficlight.getAllProgramLogics(tls_id)
    
    # Get the first logic if multiple are defined
    if logic:
        traffic_light_logic = logic[0]  # Assume the first logic is what we want
        phases = traffic_light_logic.getPhases()
        return len(phases)
    return 0  # Return 0 if no logic is found
def get_traffic_light_id(lane_number):
    traffic_light_id = ''
    if lane_number == 3:
        traffic_light_id = 'J7'
    elif lane_number == 4:
        traffic_light_id = 'J9'
    elif lane_number == 5:
        traffic_light_id = 'J10'
    elif lane_number == 6:
        traffic_light_id = 'J17'
    elif lane_number == 7:
        traffic_light_id = 'J14'
    return traffic_light_id

def run(lane_number):
    """execute the TraCI control loop"""
    traffic_light_id = get_traffic_light_id(lane_number)
    step = 0
    total_waiting_time = 0
    total_travel_time = 0
    red_light_time = None
    last_phase = -1
    dt = Detect()
    cp = Capture()
    tlc = TrafficLightControl(traffic_light_id) #J7 = 3, J9 = 4, J10 = 5, J17 = 6, J14 = 7
    num_ways = get_edge(tlc) / 4
    sat_flow = 1800  # Saturation flow rate in vehicles per hour | Default = 1800
    L = 5  # Lost time (red + yellow) in seconds, adjust as necessary
    

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        # current_phase = traci.trafficlight.getPhase(tlc.trafficlight_id)
        # num_phases = get_traffic_light_phases(tlc.trafficlight_id)  # Lấy số lượng giai đoạn

        # if current_phase != last_phase:
        #     # Kiểm tra nếu current_phase là giai đoạn cuối cùng
        #     if current_phase == num_phases - 1:
        #         # Xử lý đặc biệt cho giai đoạn cuối cùng
        #         pass  # Thêm logic xử lý ở đây nếu cần
        #     else:
        #         tlc.update_vehicle_counts(current_phase)
        #     last_phase = current_phase

        # if red_light_time == 2:
        #     print("\nChup hinh doi pha")
        #     # phân loại mật độ giao thông
        #     screen = cp.capture_screen()
        #     result = dt.predict(screen)
        #     weight = dt.calculate_weight(result)

        #     if weight == 0:
        #         weight = 1
            
        #     if(weight < 18 * num_ways/4):
        #         c_min = 20  # Minimum cycle length in seconds
        #         c_max = 15*num_ways  # Maximum cycle length in seconds
        #         print('vang')
        #     elif (weight < 39 * num_ways/4):
        #         c_min = 40
        #         c_max = 20*num_ways
        #         print('it')
        #     else:
        #         c_min = 60
        #         c_max = 25*num_ways
        #         print('dong')

        #     if num_ways == 3:       #ngã 3
        #         y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
        #         total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
        #         print("Total time: ",total_time, "y_crit_value: ", y_crit_value)

        #         horizontal_road_image, vertical_road_image = cp.capture_road3T(screen)
        #         horizontal_result = dt.predict( horizontal_road_image)
        #         vertical_result = dt.predict( vertical_road_image)
        #         horizontal_weight = dt.calculate_weight(horizontal_result)
        #         vertical_weight = dt.calculate_weight(vertical_result)
                
        #         time1 = round((horizontal_weight /weight) * total_time)
        #         time2 = round((vertical_weight /weight) * total_time)
        #         phases = tlc.create_phases_3(time1, time2)
        #         tlc.set_traffic_light_cycle( phases)

        #         print("Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "Doc", str(vertical_weight) +' time doc:'+ str(time2))
                            
        #     elif num_ways == 4:         #Ngã 4
        #         y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
        #         total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
        #         print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                

        #         horizontal_road_image, vertical_road_image = cp.capture_road4(screen)
        #         horizontal_result = dt.predict( horizontal_road_image)
        #         vertical_result = dt.predict( vertical_road_image)
        #         horizontal_weight = dt.calculate_weight(horizontal_result)
        #         vertical_weight = dt.calculate_weight(vertical_result)
                
        #         time2 = round((horizontal_weight /weight) * total_time)
        #         time1 = round((vertical_weight /weight) * total_time)
        #         phases = tlc.create_phases_4(time1, time2)
        #         tlc.set_traffic_light_cycle( phases)

        #         print("Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "Doc", str(vertical_weight) +' time doc:'+ str(time2))

        #     elif num_ways == 5:
        #         y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
        #         total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
        #         print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                
        #         X_road_image, Y_road_image, Z_road_image, W_road_image = cp.capture_road5(screen)
        #         X_result = dt.predict( X_road_image)
        #         Y_result = dt.predict( Y_road_image)
        #         Z_result = dt.predict( Z_road_image)
        #         W_result = dt.predict( W_road_image)
        #         X_weight = dt.calculate_weight(X_result)
        #         Y_weight = dt.calculate_weight(Y_result)
        #         Z_weight = dt.calculate_weight(Z_result)
        #         W_weight = dt.calculate_weight(W_result)
                
        #         time1 = round((X_weight /weight) * total_time)
        #         time2 = round((Y_weight /weight) * total_time)
        #         time3 = round((Z_weight /weight) * total_time)
        #         time4 = round((W_weight /weight) * total_time)
        #         phases =tlc.create_phases_5(time1, time2, time3, time4)
        #         tlc.set_traffic_light_cycle( phases)


        #     elif num_ways == 6:
        #         y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
        #         total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
        #         print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                
        #         image_1, image_2, image_3 = cp.capture_road6(screen)
        #         image_1_result = dt.predict( image_1)
        #         image_2_result = dt.predict( image_2)
        #         image_3_result = dt.predict( image_3)
        #         image_1_weight = dt.calculate_weight(image_1_result)
        #         image_2_weight = dt.calculate_weight(image_2_result)
        #         image_3_weight = dt.calculate_weight(image_3_result)
                
        #         time1 = round((image_1_weight /weight) * total_time)
        #         time2 = round((image_2_weight /weight) * total_time)
        #         time3 = round((image_3_weight /weight) * total_time)
        #         phases =tlc.create_phases_6(time1, time2, time3)
        #         tlc.set_traffic_light_cycle( phases)
                
        #         print("Image 1:", str(image_1_weight) +' time 1:'+ str(time1), "Image 2", str(image_2_weight) +' time 2:'+ str(time2), "Image 3", str(image_3_weight) +' time 3:'+ str(time3))


        #     elif num_ways == 7:
        #         y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Consider using dynamic saturation flow values
        #         total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
        #         print("Total time: ",total_time, "y_crit_value: ", y_crit_value)
                
        #         image_1, image_2, image_3, image_4 = cp.capture_road7(screen)
        #         image_1_result = dt.predict( image_1)
        #         image_2_result = dt.predict( image_2)
        #         image_3_result = dt.predict( image_3)
        #         image_4_result = dt.predict( image_4)
        #         image_1_weight = dt.calculate_weight(image_1_result)
        #         image_2_weight = dt.calculate_weight(image_2_result)
        #         image_3_weight = dt.calculate_weight(image_3_result)
        #         image_4_weight = dt.calculate_weight(image_4_result)
                    
        #         time1 = round((image_1_weight /weight) * total_time)
        #         time2 = round((image_2_weight /weight) * total_time)
        #         time3 = round((image_3_weight /weight) * total_time)
        #         time4 = round((image_4_weight /weight) * total_time)
        #         phases =tlc.create_phases_7(time1, time2, time3, time4)
        #         tlc.set_traffic_light_cycle( phases)
                    
        #         print("Image 1:", str(image_1_weight) +' time 1:'+ str(time1), "Image 2", str(image_2_weight) +' time 2:'+ str(time2), "Image 3", str(image_3_weight) +' time 3:'+ str(time3), "Image 4", str(image_4_weight) +' time 4:'+ str(time4))

        # if num_ways == 3 or num_ways == 4:
        #     if traci.trafficlight.getPhase(tlc.trafficlight_id) == 3:
        #         # Nếu đèn giao thông là đèn đỏ
        #         if red_light_time is None or red_light_time > 2:
        #             print(traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime())
        #             print( "Next switch: ", traci.trafficlight.getNextSwitch(tlc.trafficlight_id))
        #             print( "Current time: ", traci.simulation.getTime())
        #             red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
        #     else:
        #         # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
        #         red_light_time = None
        # elif num_ways == 5:
        #     if traci.trafficlight.getPhase(tlc.trafficlight_id) == 9:
        #         # Nếu đèn giao thông là đèn đỏ
        #         if red_light_time is None or red_light_time > 2:
        #             print(traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime())
        #             red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
        #     else:
        #         # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
        #         red_light_time = None
        # elif num_ways == 6:
        #     if traci.trafficlight.getPhase(tlc.trafficlight_id) == 11:
        #         # Nếu đèn giao thông là đèn đỏ
        #         if red_light_time is None or red_light_time > 2:
        #             print(traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime())
        #             red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
        #     else:
        #         # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
        #         red_light_time = None
        # elif num_ways == 7:
        #     if traci.trafficlight.getPhase(tlc.trafficlight_id) == 13:
        #         # Nếu đèn giao thông là đèn đỏ
        #         if red_light_time is None or red_light_time > 2:
        #             print(traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime())
        #             red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
        #     else:
        #         # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
        #         red_light_time = None
        if (step >= 600 and step <= 3600):
            total_travel_time += tlc.calculate_travel_time()
            total_waiting_time += tlc.calculate_waiting_time()

            average_waiting_time = total_waiting_time / step
            average_travel_time = total_travel_time / step

            print("Step: ", step, "Average waiting time: ", average_waiting_time)
            print("Step: ", step, "Average travel time: ", average_travel_time)
        step += 1
        
    traci.close()
    sys.stdout.flush()



def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def get_path_road(lane_number):
    """Retrieve the path of a specific lane."""
    path_road = ''
    if lane_number == 3:
        path_road = 'Sumo\\traci\\map3\\map3.sumocfg'
    elif lane_number == 4:
        path_road = 'Sumo\\traci\\map4\\map4.sumocfg'
    elif lane_number == 5:
        path_road = 'Sumo\\traci\\map5\\map5.sumocfg'
    elif lane_number == 6:
        path_road = 'Sumo\\traci\\map6\\map6.sumocfg'
    elif lane_number == 7:
        path_road = 'Sumo\\traci\\map7\\map7.sumocfg'
    return path_road

if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    lane_number = 5
    path_road = get_path_road(lane_number)
    traci.start([sumoBinary, "-c", path_road])
    run(lane_number)
