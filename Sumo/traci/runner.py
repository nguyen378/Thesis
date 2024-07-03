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
    """Tính toán độ dài chu kỳ tối ưu bằng công thức Webster."""
    Y = sum(y_crit)
    if Y > 0.85:
        Y = 0.85
    elif Y == 0.0:
        Y = 0.01

    # Tính toán thời gian chu kỳ
    C = int(((1.5 * L*num_phases) + 5) / (1.0 - Y))

    # Giới hạn thời gian chu kỳ trong khoảng giới hạn tối thiểu và tối đa
    if C > c_max:
        C = c_max
    elif C < c_min:
        C = c_min

    return C
   
def get_edge(tlc):
    """Truy xuất số cạnh kết nối với một giao lộ đèn giao thông cụ thể."""
    # Truy xuất tất cả các liên kết kết nối với giao lộ
    links = traci.trafficlight.getControlledLinks(tlc.trafficlight_id)
    
    # Khởi tạo một tập hợp để lưu trữ các cạnh duy nhất
    edges = set()
    
    # Duyệt qua mỗi cặp liên kết (mỗi cặp có thể chứa nhiều liên kết nếu có nhiều nhóm tín hiệu)
    for link_tuple in links:
        for link in link_tuple:
            # Mỗi liên kết là một tuple (incomingEdge, outgoingEdge, viaLane)
            incoming_edge, outgoing_edge, _ = link
            edges.add(incoming_edge)
            edges.add(outgoing_edge)
    
    # Trả về số lượng cạnh duy nhất
    return len(edges)

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
    red_light_time = None
    dt = Detect() # Tạo đối tượng Detect
    cp = Capture() # Tạo đối tượng Capture
    tlc = TrafficLightControl(traffic_light_id) # Tạo TrafficLightControl theo ID 
                                        # (J7 = ngã 3, J9 = ngã 4, J10 = 5, J17 = 6, J14 = 7)
    num_ways = get_edge(tlc) / 4
    sat_flow = 1800  # Dòng xe tối đa | Mặc định = 1800
    L = 5  # Thời gian mất mát trung bình | Mặc định = 5
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        if red_light_time == 2:            
            screen = cp.capture_screen() # Chụp ảnh màn hình
            result = dt.predict(screen) # Phát hiện và đếm số lượng các loại xe
            weight = dt.calculate_weight(result) # Tính toán trọng số

            if weight == 0: # Tránh trường hợp chia cho 0
                weight = 1
            
            # Set thời gian chu kỳ đèn lớn và nhỏ nhất dựa vào mật độ giao thông
            if(weight < 18 * num_ways/4):
                c_min = 20  # Thời gian chu kỳ tối thiểu
                c_max = 15*num_ways  # Thời gian chu kỳ tối đa
                print('vang')
            elif (weight < 39 * num_ways/4):
                c_min = 40
                c_max = 20*num_ways
                print('it')
            else:
                c_min = 60
                c_max = 25*num_ways
                print('dong')

            if num_ways == 3:       #ngã 3
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Tính giá trị y_crit
                total_time = websters(y_crit_value, L, c_min, c_max, num_ways) # Tính toán thời gian chu kỳ tối ưu

                horizontal_road_image, vertical_road_image = cp.capture_road3T(screen) # Chụp ảnh các tuyến

                horizontal_result = dt.predict( horizontal_road_image) # Phát hiện và đếm số lượng xe cho các ngã
                vertical_result = dt.predict( vertical_road_image) # Phát hiện và đếm số lượng xe cho các ngã
                
                horizontal_weight = dt.calculate_weight(horizontal_result) # Tính toán trọng số cho các ngã
                vertical_weight = dt.calculate_weight(vertical_result) # Tính toán trọng số cho các ngã

                time1 = round((horizontal_weight /weight) * total_time) # Phân chia thời gian đèn giao thông
                time2 = round((vertical_weight /weight) * total_time) # Phân chia thời gian đèn giao thông

                phases = tlc.create_phases_3(time1, time2) # Tạo chu kỳ đèn giao thông
                tlc.set_traffic_light_cycle( phases) # Set chu kỳ đèn giao thông

                print("Weight Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "--- Weight Doc", str(vertical_weight) +' time doc:'+ str(time2))
                            
            elif num_ways == 4:         #Ngã 4
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # tính giá trị y_crit
                total_time = websters(y_crit_value, L, c_min, c_max, num_ways) # Tính toán thời gian chu kỳ tối ưu
                

                horizontal_road_image, vertical_road_image = cp.capture_road4(screen)
                horizontal_result = dt.predict( horizontal_road_image)
                vertical_result = dt.predict( vertical_road_image)
                horizontal_weight = dt.calculate_weight(horizontal_result)
                vertical_weight = dt.calculate_weight(vertical_result)
                
                time2 = round((horizontal_weight /weight) * total_time)
                time1 = round((vertical_weight /weight) * total_time)
                phases = tlc.create_phases_4(time1, time2)
                tlc.set_traffic_light_cycle( phases)

                print("Weight Ngang:", str(horizontal_weight) +' time ngang:'+ str(time1), "--- Weight Doc", str(vertical_weight) +' time doc:'+ str(time2))

            elif num_ways == 5:
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]
                total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
                
                # Chụp ảnh các tuyến
                X_road_image, Y_road_image, Z_road_image, W_road_image = cp.capture_road5(screen)
                X_result = dt.predict( X_road_image)
                Y_result = dt.predict( Y_road_image)
                Z_result = dt.predict( Z_road_image)
                W_result = dt.predict( W_road_image)
                X_weight = dt.calculate_weight(X_result)
                Y_weight = dt.calculate_weight(Y_result)
                Z_weight = dt.calculate_weight(Z_result)
                W_weight = dt.calculate_weight(W_result)
                
                time1 = round((X_weight /weight) * total_time)
                time2 = round((Y_weight /weight) * total_time)
                time3 = round((Z_weight /weight) * total_time)
                time4 = round((W_weight /weight) * total_time)
                phases =tlc.create_phases_5(time1, time2, time3, time4)
                tlc.set_traffic_light_cycle( phases)

            elif num_ways == 6:
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]
                total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
                
                image_1, image_2, image_3 = cp.capture_road6(screen)
                image_1_result = dt.predict( image_1)
                image_2_result = dt.predict( image_2)
                image_3_result = dt.predict( image_3)
                image_1_weight = dt.calculate_weight(image_1_result)
                image_2_weight = dt.calculate_weight(image_2_result)
                image_3_weight = dt.calculate_weight(image_3_result)
                
                time1 = round((image_1_weight /weight) * total_time)
                time2 = round((image_2_weight /weight) * total_time)
                time3 = round((image_3_weight /weight) * total_time)
                phases =tlc.create_phases_6(time1, time2, time3)
                tlc.set_traffic_light_cycle( phases)
                
                print("Image 1:", str(image_1_weight) +' time 1:'+ str(time1), "Image 2", str(image_2_weight) +' time 2:'+ str(time2), "Image 3", str(image_3_weight) +' time 3:'+ str(time3))

            elif num_ways == 7:
                y_crit_value = [tlc.calculate_y_crit(sat_flow)]  # Tính giá trị y_crit
                total_time = websters(y_crit_value, L, c_min, c_max, num_ways)
                
                image_1, image_2, image_3, image_4 = cp.capture_road7(screen)
                image_1_result = dt.predict( image_1)
                image_2_result = dt.predict( image_2)
                image_3_result = dt.predict( image_3)
                image_4_result = dt.predict( image_4)
                image_1_weight = dt.calculate_weight(image_1_result)
                image_2_weight = dt.calculate_weight(image_2_result)
                image_3_weight = dt.calculate_weight(image_3_result)
                image_4_weight = dt.calculate_weight(image_4_result)
                    
                time1 = round((image_1_weight /weight) * total_time)
                time2 = round((image_2_weight /weight) * total_time)
                time3 = round((image_3_weight /weight) * total_time)
                time4 = round((image_4_weight /weight) * total_time)
                phases =tlc.create_phases_7(time1, time2, time3, time4)
                tlc.set_traffic_light_cycle( phases)
                    
                print("Image 1:", str(image_1_weight) +' time 1:'+ str(time1), "Image 2", str(image_2_weight) +' time 2:'+ str(time2), "Image 3", str(image_3_weight) +' time 3:'+ str(time3), "Image 4", str(image_4_weight) +' time 4:'+ str(time4))

        if num_ways == 3 or num_ways == 4:
            if traci.trafficlight.getPhase(tlc.trafficlight_id) == 3:
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    # Set thời gian đèn đỏ
                    red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ thì không xử lý
                red_light_time = None

        elif num_ways == 5:
            if traci.trafficlight.getPhase(tlc.trafficlight_id) == 9:
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
                red_light_time = None
        elif num_ways == 6:
            if traci.trafficlight.getPhase(tlc.trafficlight_id) == 11:
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
                red_light_time = None
        elif num_ways == 7:
            if traci.trafficlight.getPhase(tlc.trafficlight_id) == 13:
                # Nếu đèn giao thông là đèn đỏ
                if red_light_time is None or red_light_time > 2:
                    red_light_time = traci.trafficlight.getNextSwitch(tlc.trafficlight_id) - traci.simulation.getTime()
            else:
                # Nếu đèn giao thông không phải là đèn đỏ, đặt lại red_light_time
                red_light_time = None

        if (step >= 600 and step <= 3600):
            total_travel_time += tlc.calculate_travel_time()
            average_waiting_time = total_waiting_time / step

            print("Step: ", step, "Average waiting time: ", average_waiting_time)
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
    lane_number = 4
    path_road = get_path_road(lane_number)
    traci.start([sumoBinary, "-c", path_road])
    run(lane_number)
