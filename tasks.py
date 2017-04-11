#from flask_apscheduler import APScheduler
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler

from models import *
from app import *

scheduler = APScheduler()

class Config(object):
	JOBS = [
		{
			'id': 'job1',
			'func': '__main__:check',
			'args': (),
			'trigger': 'interval',
			'minutes': 15
		},
		{
			'id': 'job2',
			'func': '__main__:check',
			'args': (),
			'trigger': 'interval',
			'minutes': 30
		},
		{
			'id': 'job3',
			'func': '__main__:check',
			'args': (),
			'trigger': 'interval',
			'minutes': 45
		}
	]

	SCHEDULER_API_ENABLED = True

def check():

	print "This is it! It's on!"
	x = get_backup_o_f()

	if x == 'on':
		#scheduler.add_job(backup_schedule(), days_of_week='0-6', time=8, id='1')
		#scheduler.add_job(backup_schedule(), days_of_week='0-6', time=13, id='2')
		#scheduler.add_job(backup_schedule(), days_of_week='0-6', time=18, id='3')
		#scheduler.print_jobs()
		print 'Jobs On!'
	elif x == 'off':
		scheduler.remove_job('job1')
		scheduler.remove_job('job2')
		scheduler.remove_job('job3')
		scheduler.print_jobs()
		print 'Removed all jobs'
	else:
		print "Turn backups on to return backup schedule."

def job1(a, b):
	print(str(a) + ' ' + str(b))

#def backup_sched():

#	x = get_backup_o_f()
#	
#	if x == 'on':
#		c = get_backup_c()
#		if c == '1':

#@sched.scheduled_job('cron', days_of_week='mon-sun', time=8)
#@sched.scheduled_job('cron', days_of_week='mon-sun', time=13)
#@sched.scheduled_job('cron', days_of_week='mon-sun', time=18)