from pygit2 import clone_repository
from flask import Flask
from datetime import datetime
from os import listdir
from os.path import isdir
from simples3 import S3Bucket
import time, math, os, json
import boto
import boto.s3
from boto.s3.key import Key
import os.path
import sys
import shutil
from flask.ext.mysql import MySQL
import logging

# set the log location #
logging.basicConfig(filename='cron.log')

# custom imports made here #

from models import *

###################
# begin functions #
###################

def check():

	print "This is it! It's on!"
	x = get_backup_o_f()

	if x == 'on':	
		print 'Jobs On!'
		logging.debug('Jobs on!')
		backup_schedule()

	elif x == 'off':
		print 'Jobs Off!'
		logging.debug('Backups are turned off! - ' + str(datetime.datetime.now()))
	else:
		print "Turn backups on to return backup schedule."

check()