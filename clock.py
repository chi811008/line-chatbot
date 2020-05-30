from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes='1')
def scheduled_job():
    print('timer')

sched.start()
