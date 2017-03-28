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

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hugbug4401'
app.config['MYSQL_DATABASE_DB'] = 'repos_1'
app.config['MYSQL_DATABASE_HOST'] = 'github-v1.ck0wcz8ygfoy.us-west-2.rds.amazonaws.com'
mysql.init_app(app)

# boto connection
def create_AWS_conn():

	t = 'id'
	ID = get_AWS_Credentials(t)
	t = 'sk'
	SK = get_AWS_Credentials(t)

	s3_conn = boto.connect_s3(ID[0], SK[0])
	return s3_conn

# AWS Credentials
def get_AWS_Credentials(t):

	conn = mysql.connect()
	cursor = conn.cursor()

	SID = 1;

	if t == 'id':
		cursor.execute("SELECT atid FROM Settings WHERE SID = (%s);", SID)
		ID = cursor.fetchone()
		return ID
	elif t == 'sk':
		cursor.execute("SELECT atsk FROM Settings WHERE SID = (%s);", SID)
		SK = cursor.fetchone()
		return SK

# upload single or multipart to AWS S3
def upload_to_S3(bucket_name, z_path, a_name):
	AWS_ACCESS_KEY_ID = 'AKIAIEF4H55FISD3AM3A'
	AWS_ACCESS_KEY_SECRET = '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'

	conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY_SECRET)

	bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

	file = z_path
	print "Uploading %s to Amazon S3 Bucket %s" % (file, bucket_name)

	def percent_cb(complete, total):
		sys.stdout.write('.')
		sys.stdout.flush()

	k = Key(bucket)
	k.key = a_name
	k.set_contents_from_filename(file, cb=percent_cb, num_cb=10)

# big file upload and all
def upload_file(s3, bucketname, file_path):

        b = s3.get_bucket(bucketname)

        filename = os.path.basename(file_path)
        k = b.new_key(filename)

        mp = b.initiate_multipart_upload(filename)

        source_size = os.stat(file_path).st_size
        bytes_per_chunk = 5000*1024*1024
        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

        for i in range(chunks_count):
                offset = i * bytes_per_chunk
                remaining_bytes = source_size - offset
                bytes = min([bytes_per_chunk, remaining_bytes])
                part_num = i + 1

                print "uploading part " + str(part_num) + " of " + str(chunks_count)

                with open(file_path, 'r') as fp:
                        fp.seek(offset)
                        mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)

        if len(mp.get_all_parts()) == chunks_count:
                mp.complete_upload()
                print "upload_file done"
        else:
                mp.cancel_upload()
                print "upload_file failed"

# clone_repo function (at) #
def clone_repo(at, url, name):

	conn = mysql.connect()
	cursor = conn.cursor()

	r_at = at
	r_url = 'https://' + r_at + ':x-oauth-basic@' + url[8:]
	r_name = name
	_dT = str(datetime.now())

	path = '/home/ubuntu/.clones/' + r_name
	s3_path = path + ' | ' + _dT

	cursor.execute("INSERT INTO Repos1 (_at, _uri, _datetime, _name) VALUES (%s, %s, %s, %s);", (r_at, r_url, _dT, r_name))
	x = cursor.fetchone()
	conn.commit()
	conn.close()

	a_name = _dT + '_' + r_name
	z_path = '/home/ubuntu/.clones/' + a_name

	repo = clone_repository(r_url, path)
	print "Repo Cloned!"
	time.sleep(5)
	print "Finished sleep!"
	shutil.make_archive(z_path, 'zip', '/home/ubuntu/.clones', path)
	print "zipped : " + a_name
	s3 = create_AWS_conn()

	upload = upload_file(s3, 'testhowiesee', z_path + '.zip')
	print "Done Uploading!"

	a = shutil.rmtree('/home/ubuntu/.clones/' + name)
	print a
	b = os.remove('/home/ubuntu/.clones/' + a_name + '.zip')
	print b

	return  json.dumps({'success': True, 'Message': 'Added ' + r_name + ' to scheduled backups!'}), 200, {'ContentType': 'application/json'}


# get All (MYSQL) #

def get_all_Repos():

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT * FROM Repos1;")
	x = cursor.fetchall()
	conn.commit()
	conn.close()
	return x

def get_distinct_Repos():

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT DISTINCT _name FROM Repos1 ORDER BY _datetime DESC LIMIT 6;")
	x = cursor.fetchall()
	conn.commit()
	conn.close()
	return x

def get_last_date(name):

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT _datetime FROM Repos1 WHERE _name = %s ORDER BY _datetime DESC LIMIT 1;", name)
	x = cursor.fetchone()
	conn.commit()
	conn.close()
	return x

# sec login
def get_login_credentials(username, password):
	# Create MySQL connection #

	if username == 'chrism' and password == 'I love ADD!':
		return True
	elif username == 'howiesee' and password == 'I love ADD!':
		return True
	else:
		return False

	# end return of boolean #

# update or add settings

#########################
### INTERNAL FUNCS ######
#########################

def get_backup_c():

	conn = mysql.connect()
	cursor = conn.cursor()

	SID = 1

	cursor.execute("SELECT buf FROM Settings WHERE SID = (%s);", SID)
	conn.commit()
	x = cursor.fetchone()
	conn.close()
	return x[0]

def get_backup_o_f():

	conn = mysql.connect()
	cursor = conn.cursor()

	SID = 1

	cursor.execute("SELECT backups FROM Settings WHERE SID = (%s);", SID)
	conn.commit()
	x = cursor.fetchone()
	conn.close()
	return x[0]

def get_upload_values(RID):

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT _uri FROM Repos1 WHERE RID = (%s);", RID)
	a = cursor.fetchone()
	cursor.execute("SELECT _name FROM Repos1 WHERE RID = (%s);", RID)
	b = cursor.fetchone()
	conn.commit()
	return [a, b]

# the massive loop
def backup_schedule():

	data = ID_check()
	#print data
	for i in data:
		a = get_upload_values(i)
		print a[0][0]
		print a[1][0]
		path = '/home/ubuntu/.clones/' + a[1][0]
		_dT = str(datetime.now())
		a_name = _dT + '_' + a[1][0]
		z_path = '/home/ubuntu/.clones/' + a_name
		b = clone_repository(a[0][0], path)
		print "Repo Cloned!"
		time.sleep(5)
		print "Finished sleep!"
		shutil.make_archive(z_path, 'zip', '/home/ubuntu/.clones', path)
		print "zipped : " + a_name
		s3 = create_AWS_conn()

		upload = upload_file(s3, 'testhowiesee', z_path + '.zip')
		print "Done Uploading!"

		c = shutil.rmtree('/home/ubuntu/.clones/' + a[1][0])
		print c
		d = os.remove('/home/ubuntu/.clones/' + a_name + '.zip')
		print d

#########################
#### Check Functions ####
#########################

# records
def ID_check():

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute("SELECT RID FROM Repos1;")
	conn.commit()
	x = cursor.fetchall()
	conn.close()
	return x

# ATID
def atid_check(atid, SID):

	conn = mysql.connect()
	cursor = conn.cursor()

	print len(atid)
	if len(atid) > 0:
		cursor.execute("UPDATE Settings SET atid = %s WHERE SID = %s;", (atid, SID))
		conn.commit()
		x = 'Access Token ID'
		conn.close()
		return x
	elif len(atid) is 0 or None:
		pass
		return "Nothing to do."
	else:
		return "ERR Access Token ID in SQL."

# ATSK
def atsk_check(atsk, SID):

	conn = mysql.connect()
	cursor = conn.cursor()

	print len(atsk)
	if len(atsk) > 0:
		cursor.execute("UPDATE Settings SET atsk = %s WHERE SID = %s;", (atsk, SID))
		conn.commit()
		x = 'Access Token Secret Key'
		conn.close()
		return x
	elif len(atsk) is 0 or None:
		pass
		return "Nothing to do."
	else:
		return "ERR Access Token Secret Key in SQL."

# BUF
def buf_check(buf, SID):

	conn = mysql.connect()
	cursor = conn.cursor()

	print len(buf)
	if len(buf) > 0:
		cursor.execute("UPDATE Settings SET buf = %s WHERE SID = %s;", (buf, SID))
		conn.commit()
		x = 'Backup Freq.'
		conn.close()
		return x
	elif len(buf) is 0 or None:
		pass
		return "Nothing to do."
	else:
		return "ERR Backup Frequency in SQL."

# BACKUPS
def backup_check(backups, SID):

	conn = mysql.connect()
	cursor = conn.cursor()

	print len(backups)
	if len(backups) > 0:
		cursor.execute("UPDATE Settings SET backups = %s WHERE SID = %s;", (backups, SID))
		conn.commit()
		x = 'Backup Switch'
		conn.close()
		return x
	elif len(backups) is 0 or None:
		pass
		return "Nothing to do."
	else:
		return "ERR Backups Switch in SQL."

##############################
### CONTEXT PROCESSORS #######
##############################

def get_Settings_data():

	conn = mysql.connect()
	cursor = conn.cursor()

	SID = 1

	cursor.execute("SELECT * FROM Settings WHERE SID = %s;", SID)
	x = cursor.fetchone()
	conn.close()
	return x

def action_Settings(atid, atsk, buf, backups):

	SID = 1;
	_atid = atid
	_atsk = atsk
	_buf = buf
	_backups = backups

	c_atid = atid_check(_atid, SID)
	c_atsk = atsk_check(_atsk, SID)
	c_buf = buf_check(_buf, SID)
	c_backup = backup_check(_backups, SID)

	return {"ATID": c_atid, "ATSK": c_atsk, "BUF": c_buf, "BACKUPS": c_backup}
	




