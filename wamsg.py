import datetime

class WAMSG:
    def __init__(self, date, time, sender, text=None, attachment=None):
        self.date = date
        self.time = time
        self.sender = sender
        self.text = text
        self.attachment = attachment