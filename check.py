from crontab import CronTab

# custom imports made here #
from models import *

user_cron = CronTab(user='www-data')

