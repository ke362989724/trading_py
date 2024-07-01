import schedule 

class Schedule:
    def every_day(self, job):
        return schedule.every().day.at("13:00").do(job)