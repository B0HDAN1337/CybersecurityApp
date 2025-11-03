from datetime import datetime, timedelta

class SessionManager:

    def __init__(self, timeout_minutes):
        self.timeout = timedelta(minutes=timeout_minutes)
        self.start_time = None
        self.username = None

    def start_session(self, username):
        self.username = username
        self.start_time = datetime.now()

    def end_session(self):
        self.username = None
        self.start_time = None

    def check_session(self):
        if not self.start_time:
            return False
        return datetime.now() - self.start_time <self.timeout

    
    