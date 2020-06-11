import apscheduler

sched = apscheduler.schedulers

@sched.scheduled_job('interval', minutes='1')
def scheduled_job():
    print('timer')

sched.start()
