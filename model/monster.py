class Monster:
    mon_name: str = None
    frame: str = None
    
    # Init with monBranch json data
    def __init__(self, json_data):
        self.mon_map_id: str = str(json_data['MonMapID'])
        self.mon_id: str = str(json_data['MonID'])
        self.is_alive: bool = int(json_data['intState']) > 0
        self.current_hp: int = json_data['intHP']
        self.max_hp: int = json_data['intHPMax']