import traci

class TrafficLightControl:
    def __init__(self, trafficlight_id):
        self.trafficlight_id = trafficlight_id
        self.vehicle_entry_times = {}   
        self.phase_vehicle_counts = {}     

    def calculate_waiting_time(self):
        """Calculate the waiting time for a specific traffic light by summing up the waiting times of all controlled lanes."""
        # Fetch all lanes controlled by the traffic light
        controlled_lanes = traci.trafficlight.getControlledLanes(self.trafficlight_id)
        
        # Calculate total waiting time by summing the waiting time of each lane
        total_waiting_time = 0
        for lane in controlled_lanes:
            lane_waiting_time = traci.lane.getWaitingTime(lane)
            total_waiting_time += lane_waiting_time
            # Optionally, log waiting time for each lane if needed for debug or analysis
            # print(f"Lane {lane}: Waiting Time = {lane_waiting_time}s")
        
        return total_waiting_time

    def calculate_travel_time(self):
        """Calculate the total travel time through the junction for vehicles."""
        travel_times = []
        controlled_lanes = traci.trafficlight.getControlledLanes(self.trafficlight_id)
        
        for lane in controlled_lanes:
            vehicles = traci.lane.getLastStepVehicleIDs(lane)
            for vehicle in vehicles:
                if vehicle not in self.vehicle_entry_times:
                    # Record the entry time of the vehicle into the junction area
                    self.vehicle_entry_times[vehicle] = traci.simulation.getTime()
                else:
                    # Calculate travel time if the vehicle has exited the junction
                    if traci.vehicle.getRoadID(vehicle) not in controlled_lanes:
                        entry_time = self.vehicle_entry_times.pop(vehicle, None)
                        if entry_time is not None:
                            travel_time = traci.simulation.getTime() - entry_time
                            travel_times.append(travel_time)
        
        total_travel_time = sum(travel_times)
        return total_travel_time
    
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
            traci.trafficlight.Phase(time_1, "rrGGGGGg", time_1, time_1, [1,2,3]),  # Green for first 3 lanes
            traci.trafficlight.Phase(3, "rrryyyyy"),  # Yellow for first 3 lanes
            traci.trafficlight.Phase(time_2, "GGrrrrrr"),  # Green for next 3 lanes
            traci.trafficlight.Phase(3, "yyrrrrrr")    # Yellow for next 3 lanes
        ]
        return phases
    def create_phases_4(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 4
        phases = [
            traci.trafficlight.Phase(time_1, "GGGgrrrrGGGgrrrr", 0, 0, [1,2,3]),  # Green for first 4 lanes
            traci.trafficlight.Phase(3, "yyyyrrrryyyyrrrr"),  # Yellow for first 4 lanes
            traci.trafficlight.Phase(time_2, "rrrrGGGgrrrrGGGg"),  # Green for next 4 lanes
            traci.trafficlight.Phase(3, "rrrryyyyrrrryyyy")    # Yellow for next 4 lanes
        ]
        return phases
    def create_phases_5(self, time_1, time_2, time_3, time_4):
        # Tạo chu kỳ đèn giao thông mới của ngã 5
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrrGGGGgrrrrrGGGggrrrrr"),  
            traci.trafficlight.Phase(3, "rrrrryyyygrrrrryyyggrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrGrrrrrrrrGGrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrryrrrrrrrryyrrrrr"),  
            traci.trafficlight.Phase(time_4, "rrrrrrrrrrGGGGGGrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrryyyyyyrrrrrrrrr"),  
            traci.trafficlight.Phase(time_3, "GGGGGGrrrrrrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(3, "Gyyyyyrrrrrrrrrrrrrrrrrrr"),    
            traci.trafficlight.Phase(time_2, "GrrrrrrrrrrrrrrrrrrrGGGGG"),  
            traci.trafficlight.Phase(3 , "yrrrrrrrrrrrrrrrrrrryyyyy")   
        ]
        return phases
    def create_phases_6(self, time_1, time_2, time_3):
        # Tạo chu kỳ đèn giao thông mới của ngã 6
        phases = [
            traci.trafficlight.Phase(time_1, "GGGGggrrrrrrrrrrrrGGGGggrrrrrrrrrrrr", time_1, time_1, [1,2,3]),  
            traci.trafficlight.Phase(3, "yyyyggrrrrrrrrrrrryyyyggrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrGGrrrrrrrrrrrrrrrrGGrrrrrrrrrrrr"),
            traci.trafficlight.Phase(3, "rrrryyrrrrrrrrrrrrrrrryyrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(time_3, "rrrrrrrrrrrrGGGGggrrrrrrrrrrrrGGGGgg"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyyyggrrrrrrrrrrrryyyygg"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrrrrrGGrrrrrrrrrrrrrrrrGG"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrrrryyrrrrrrrrrrrrrrrryy"),    
            traci.trafficlight.Phase(time_2, "rrrrrrGGGGggrrrrrrrrrrrrGGGGggrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrryyyyggrrrrrrrrrrrryyyyggrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrGGrrrrrrrrrrrrrrrrGGrrrrrr"),  
            traci.trafficlight.Phase(3 , "rrrrrrrrrryyrrrrrrrrrrrrrrrryyrrrrrr")   
        ]
        return phases
    def create_phases_7(self, time_1, time_2, time_3, time_4):
        # Tạo chu kỳ đèn giao thông mới của ngã 7
        phases = [
            traci.trafficlight.Phase(time_2, "rrrrrrrGGGGGggrrrrrrrrrrrrrrGGGGggggrrrrrrrrrrrrrr", time_1, time_1, [1,2,3]),  
            traci.trafficlight.Phase(3, "rrrrrrryyyyyggrrrrrrrrrrrrrryyyyggggrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrGGrrrrrrrrrrrrrrrrrrGGGGrrrrrrrrrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrryyrrrrrrrrrrrrrrrrrryyyyrrrrrrrrrrrrrr"),  
            traci.trafficlight.Phase(time_4, "rrrrrrrrrrrrrrrrrrrrrGGGGGggrrrrrrrrrrrrrrrGGGGggg"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrrrrrrrrryyyyyggrrrrrrrrrrrrrrryyyyggg"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrrrrrrrrrrrrrrrGGrrrrrrrrrrrrrrrrrrrGGG"),  
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrrrrrrrrrrrrrryyrrrrrrrrrrrrrrrrrrryyy"),    
            traci.trafficlight.Phase(time_3, "rrrrrrrrrrrrrrGGGGGggrrrrrrrrrrrrrrrGGGGgggrrrrrrr"),
            traci.trafficlight.Phase(3, "rrrrrrrrrrrrrryyyyyggrrrrrrrrrrrrrrryyyygggrrrrrrr"),  
            traci.trafficlight.Phase(6, "rrrrrrrrrrrrrrrrrrrGGrrrrrrrrrrrrrrrrrrrGGGrrrrrrr"),  
            traci.trafficlight.Phase(3 , "rrrrrrrrrrrrrrrrrrryyrrrrrrrrrrrrrrrrrrryyyrrrrrrr"),
            traci.trafficlight.Phase(time_1, "GGGGGGGGrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"),
            traci.trafficlight.Phase(3, "yyyyyyyGrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
    
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
        self.phase_vehicle_counts[current_phase] += vehicles

    def calculate_y_crit(self, sat_flow):
        """Calculate y_crit using collected vehicle counts and saturation flow rate."""
        y_crit = []
        for _, count in self.phase_vehicle_counts.items():
            flow_ratio = count / sat_flow
            y_crit.append(flow_ratio)
        return max(y_crit) if y_crit else 0.01  # Avoid division by zero in Webster's formula
