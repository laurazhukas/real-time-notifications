class Event:

    def __init__(self, event_name : str, destination : str, origin : str, time : int, buffer_time : int):
        self.name = event_name
        self.destination_address = destination # address user needs to get to
        self.origin_address = origin # the address the user starts at
        self.time = time # datetime object with the desired arrival time
        # convert buffer_time into seconds
        self.buffer = buffer_time*60 # number of seconds a person requires to get ready (before leaving for destination)
        self.travel_time = None # the usually travel time between destination/origin updated by api

    