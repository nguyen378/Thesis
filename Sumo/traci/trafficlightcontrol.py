import traci

class TrafficLightControl:
    def __init__(self, trafficlight_id):
        self.trafficlight_id = trafficlight_id
        self.phase_vehicle_counts = {}
    def update_traffic_light(self, trafficlight_id, time_1, time_2, time_3=None, time_4=None, time_5=None):
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
            
    def create_phases(self, num_intersections, time_1, time_2, time_3=None, time_4=None, time_5=None):
        if num_intersections == 3:
            return self.create_phases_3(time_1, time_2)
        elif num_intersections == 4:
            return self.create_phases_4(time_1, time_2)
        elif num_intersections == 5:
            return self.create_phases_5(time_1, time_2, time_3, time_4, time_5)
        elif num_intersections == 6:
            return self.create_phases_6(time_1, time_2, time_3)
        elif num_intersections == 7:
            return self.create_phases_7(time_1, time_2, time_3, time_4)
        else:
            raise ValueError("Invalid number of intersections")
        
    def create_phases_3(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 3
        phases = [
            traci.trafficlight.Phase(time_1, "GGGGGgrr", time_1, time_1, [1,2,3]),  # Green for first 3 lanes
            traci.trafficlight.Phase(3, "Gyyyyyrr"),  # Yellow for first 3 lanes
            traci.trafficlight.Phase(time_2, "GrrrrrGG"),  # Green for next 3 lanes
            traci.trafficlight.Phase(3, "Grrrrryy")    # Yellow for next 3 lanes
        ]
        return phases
    def create_phases_4(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 4
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrGGGgrrrrGGGg", time_1, time_1, [1,2,3]),  # Green for first 4 lanes
            traci.trafficlight.Phase(3, "rrrryyyyrrrryyyy"),  # Yellow for first 4 lanes
            traci.trafficlight.Phase(time_2, "GGGgrrrrGGGgrrrr"),  # Green for next 4 lanes
            traci.trafficlight.Phase(3, "yyyyrrrryyyyrrrr")    # Yellow for next 4 lanes
        ]
        return phases
    def create_phases_5(self, time_1, time_2, time_3, time_4):
        # Tạo chu kỳ đèn giao thông mới của ngã 5
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrrGGGGgrrrrrGGGggrrrrr"),  
            traci.trafficlight.Phase(3, "rrrrryyyygrrrrryyyggrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrGrrrrrrrrGGrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrryrrrrrrrryyrrrrr"),  
            traci.trafficlight.Phase(time_2, "GrrrrrrrrrrrrrrrrrrrGGGGG"),  
            traci.trafficlight.Phase(3, "yrrrrrrrrrrrrrrrrrrryyyyy"),  
            traci.trafficlight.Phase(time_3, "rrrrrrrrrrGGGGGGrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrryyyyyyrrrrrrrrr"),    
            traci.trafficlight.Phase(time_4, "GGGGGGrrrrrrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(3 , "yyyyyGrrrrrrrrrrrrrrrrrrr")   
        ]
        return phases
    def create_phases_6(self, time_1, time_2, time_3):
        # Tạo chu kỳ đèn giao thông mới của ngã 6
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrrrrrrrrrGGGGggrrrrrrrrrrrrGGGGgg", time_1, time_1, [1,2,3]),  
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyyggrrrrrrrrrrrryyyygg"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrrrrrGGrrrrrrrrrrrrrrrrGG"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrrrryyrrrrrrrrrrrrrrrryy"),  
            traci.trafficlight.Phase(time_2, "GGGGggrrrrrrrrrrrrGGGGggrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "yyyyggrrrrrrrrrrrryyyyggrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrGGrrrrrrrrrrrrrrrrGGrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "rrrryyrrrrrrrrrrrrrrrryyrrrrrrrrrrrr"),    
            traci.trafficlight.Phase(time_3, "rrrrrrggGGggrrrrrrrrrrrrGGGgggrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrggyyggrrrrrrrrrrrryyygggrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrggrrGGrrrrrrrrrrrrrrrGGgrrrrrr"),  
            traci.trafficlight.Phase(3 , "rrrrrryyrryyrrrrrrrrrrrrrrryyyrrrrrr")   
        ]
        return phases
    def create_phases_7(self, time_1, time_2, time_3, time_4):
        # Tạo chu kỳ đèn giao thông mới của ngã 7
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrrrrGGGGGggrrrrrrrrrrrrrrrGGGGgggrrrrrrrrrrrrrr", time_1, time_1, [1,2,3]),  
            traci.trafficlight.Phase(3, "rrrrrrryyyyyggrrrrrrrrrrrrrrryyyygggrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrGGrrrrrrrrrrrrrrrrrrrGGGrrrrrrrrrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyrrrrrrrrrrrrrrrrrrryyyrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(time_2, "GrrrGGGGGggrrrrrrrrrrrrrrrGGGGgggrrrrrrrrrrrrrrrrrrrrrrrGGrrrrrGGGrrrrr"),  
            traci.trafficlight.Phase(3, "yyyyyggrrrrrrrrrrrrrrryyyygggrrrrrrrrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrGGrrrrrrrrrrrrrrrrrrrGGGrrrrrrrrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "rrrrryyrrrrrrrrrrrrrrrrrrryyyrrrrrrrrrrrrrrrrrrrrr"),    
            traci.trafficlight.Phase(time_3, "rrrrrrrrrrrrrrGGGGggggrrrrrrrrrrrrrrrrrrrrrgggGGgg"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrryyyyggggrrrrrrrrrrrrrrrrrrrrrgggyygg"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrrrrrrrGGggrrrrrrrrrrrrrrrrrrrrrgggrrGG"),  
            traci.trafficlight.Phase(3 , "rrrrrrrrrrrrrrrrrryyyyrrrrrrrrrrrrrrrrrrrrrgyyrryy"),
            traci.trafficlight.Phase(time_4, "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrGGGGGGGGrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrryyyyyyyyrrrrrr")
    
        ]
        return phases
    
    def set_traffic_light_cycle(self, phases):
        """Thiết lập chu kỳ đèn giao thông mới cho nút giao được xác định bởi tls_id."""
        # Thiết lập kế hoạch đèn giao thông (program)
        program = traci.trafficlight.Logic("custom_program", 0, 0, phases)
        traci.trafficlight.setProgramLogic(self.trafficlight_id, program)
        traci.trafficlight.setPhase(self.trafficlight_id, 0)

        
    def update_vehicle_counts(self, current_phase):
        """Update vehicle counts for the current green phase."""
        if current_phase not in self.phase_vehicle_counts:
            self.phase_vehicle_counts[current_phase] = 0
        # Retrieve the number of vehicles that have passed during the green phase
        lane_id = traci.trafficlight.getControlledLanes(self.trafficlight_id)[current_phase]
        vehicles = traci.lane.getLastStepVehicleNumber(lane_id)
        print("Lane id: ", lane_id, "Vehicle: ", vehicles)
        self.phase_vehicle_counts[current_phase] += vehicles

    def calculate_y_crit(self, sat_flow):
        """Calculate y_crit using collected vehicle counts and saturation flow rate."""
        y_crit = []
        for _, count in self.phase_vehicle_counts.items():
            flow_ratio = count / sat_flow
            y_crit.append(flow_ratio)
        return max(y_crit) if y_crit else 0.01  # Avoid division by zero in Webster's formula
    