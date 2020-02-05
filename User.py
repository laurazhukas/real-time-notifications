class User:

    def __init__(self, first_name : str, last_name : str, distance_units = 'metric'):
        self.first_name = first_name
        self.last_name = last_name
        self.units = distance_units # API default for units is 'metric' other option is 'imperial'
        self.events = [] # store a list of event objects