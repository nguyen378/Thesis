import traci

class TrafficLightControl:
    def __init__(self, trafficlight_id):
        self.trafficlight_id = trafficlight_id
        
    def create_phases_3(self, time_1, time_2):
        # Tạo chu kỳ đèn giao thông mới của ngã 3
        phases = [
            traci.trafficlight.Phase(time_1, "GGGGGgrr", 0, 0, [1,2,3]),  # Green for first 3 lanes
            traci.trafficlight.Phase(5, "Gyyyyyrr"),  # Yellow for first 3 lanes
            traci.trafficlight.Phase(time_2, "GrrrrrGG"),  # Green for next 3 lanes
            traci.trafficlight.Phase(5, "Grrrrryy")    # Yellow for next 3 lanes
        ]
        return phases
    def set_traffic_light_cycle(self, phases):
        """Thiết lập chu kỳ đèn giao thông mới cho nút giao được xác định bởi tls_id."""
        # Thiết lập kế hoạch đèn giao thông (program)
        program = traci.trafficlight.Logic("custom_program", 0, 0, phases)
        print(program)
        print("Chinh chu ky den")
        traci.trafficlight.setProgramLogic(self.trafficlight_id, program)
        traci.trafficlight.setPhase(self.trafficlight_id, 0)
        