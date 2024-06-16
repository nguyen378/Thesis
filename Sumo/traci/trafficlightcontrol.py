import traci

class TrafficLightControl:
    def __init__(self, trafficlight_id):
        self.trafficlight_id = trafficlight_id
        self.phase_vehicle_counts = {}

        
    def create_phases_3(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 3
        phases = [
            traci.trafficlight.Phase(time_1, "GGGGGgrr", 0, 0, [1,2,3]),  # Green for first 3 lanes
            traci.trafficlight.Phase(5, "Gyyyyyrr"),  # Yellow for first 3 lanes
            traci.trafficlight.Phase(time_2, "GrrrrrGG"),  # Green for next 3 lanes
            traci.trafficlight.Phase(5, "Grrrrryy")    # Yellow for next 3 lanes
        ]
        return phases
    def create_phases_4(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 4
        phases = [
            traci.trafficlight.Phase(time_1, "rrrrGGGgrrrrGGGg", 0, 0, [1,2,3]),  # Green for first 4 lanes
            traci.trafficlight.Phase(5, "rrrryyyyrrrryyyy"),  # Yellow for first 4 lanes
            traci.trafficlight.Phase(time_2, "GGGgrrrrGGGgrrrr"),  # Green for next 4 lanes
            traci.trafficlight.Phase(5, "yyyyrrrryyyyrrrr")    # Yellow for next 4 lanes
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
    