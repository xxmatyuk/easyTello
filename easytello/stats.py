from datetime import datetime

class Stats:
    def __init_(self, command, id):
        self.command = command
        self.response = None
        self.id = id

        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None

    def add_response(self, response):
        self.response = response
        self.end_time = datetime
        self.duration = (self.end_time-self.start_time).total_seconds()

    def got_response(self):
        if self.response is None:
            return False
        else:
            return True

    def get_response(self):
        return self.response
