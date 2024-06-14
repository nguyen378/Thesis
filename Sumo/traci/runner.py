import os
import sys
import optparse
import random
from ultralytics import YOLOv10


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

def capture_screen():
    """Chụp màn hình từ 3 vị trí khác nhau"""
    # Chụp màn hình tại vị trí 1 (ví dụ: vùng bên trái)
    screenshot = ImageGrab.grab(bbox=(400, 130, 1450, 980))  # Tọa độ (0, 0) là góc trên bên trái
    return screenshot
def detect_objects(model, screenshot):
    # Tính toán trọng số dựa trên số lượng vật thể phát hiện được từ mô hình YOLOv10.
    
    # Nhận diện vật thể từ 3 vị trí khác nhau
    results = model(screenshot, conf=0.3, iou=0.5, verbose=False)
    class_detections_values = []
    for k, v in model.names.items():
        class_detections_values.append(results[0].boxes.cls.tolist().count(k))
    # create dictionary of objects detected per class
    classes_detected = dict(zip(model.names.values(), class_detections_values))
    
    weight = (classes_detected['Bus']*3 + classes_detected['Car'] + classes_detected['Motor']*0.75 + classes_detected['Truck']*1.5)
    return weight
def create_phases_3(time_1, time_2):
    # Tạo chu kỳ đèn giao thông mới của ngã 3
    phases = [
        traci.trafficlight.Phase(time_1, "GGGGGgrr"),  # Green for first 3 lanes
        traci.trafficlight.Phase(5, "Gyyyyyrr"),  # Yellow for first 3 lanes
        traci.trafficlight.Phase(time_2, "GrrrrrGG"),  # Green for next 3 lanes
        traci.trafficlight.Phase(5, "Grrrrryy")    # Yellow for next 3 lanes
    ]
    return phases
def set_traffic_light_cycle(tls_id, phases):
    """Thiết lập chu kỳ đèn giao thông mới cho nút giao được xác định bởi tls_id."""
    # Thiết lập kế hoạch đèn giao thông (program)
    program = traci.trafficlight.Logic("custom_program", 0, 1, phases)
    traci.trafficlight.setProgramLogic(tls_id, program)

def run():
    """execute the TraCI control loop"""
    step = 0
    red_light_time = None
    # Load mô hình YOLOv5
    model = YOLOv10('F:\\Project\\Thesis\\Thesis\\ModelVehicleDetect\\best.pt')

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print(traci.trafficlight.getPhase("J28"))
        if red_light_time == 2:
            # phân loại mật độ giao thông
            screen = capture_screen()
            weight = detect_objects(model, screen)
            phases = create_phases_3()
            print(phases)
            if(weight < 12):
                
                set_traffic_light_cycle('J28', phases)
                print('vang')
            elif (weight <30):
                set_traffic_light_cycle('J28', phases) 
                print('dong')
            else:
                set_traffic_light_cycle('J28', phases)
                print('vang')
        
        if traci.trafficlight.getPhase("J28") == 0:
            # Nếu đèn giao thông là đèn đỏ
            if red_light_time is None:
                print(traci.trafficlight.getNextSwitch("J28") - traci.simulation.getTime())
                # Nếu red_light_time chưa được thiết lập, thiết lập bằng thời gian của đèn đỏ
                red_light_time = traci.trafficlight.getNextSwitch("J28") - traci.simulation.getTime()
            elif red_light_time > 2:
                print(traci.trafficlight.getNextSwitch("J28") - traci.simulation.getTime())
                # Nếu red_light_time lớn hơn 2, cập nhật lại red_light_time
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
