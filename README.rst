=====
purgedata
=====

Purgedata is a simple Django app to delete stale data that has been on the database for a long time. 
Old data can be purged by scheduling. For example purgedata can be set to continously monitor and purge
data older than 6 months. 
Using the celery crontab, you can set purgedata to monitor every minute, every hour,
every week and any combination of these and delete data older than a given period of time.
You can also use the command-line tool to purge data.

Installation
------------
For Celery and RabbitMQ, see the installation documentation in the "docs" directory.
To use purgedata, you must make the purgedata package available on your python path. Drop the purgedata app into your project directory


Management command
-------------------
To purge data of a given model from python manage.py, run:


	#  this command will purge all data for mymodel model in myapp app.
	python manage.py purge_data myapp.mymodel --all   #  or equivalently
	python manage.py purge_data myapp.mymodel -a

Note that the name of the app is case-sensitive and that you can use `--all` or `-a` interchangibly
To purge data of a given model based on a filter, run:
	#  for example, to purge data older than 6 months on a model with a DateTimeField or DateField called `created_date`, run:
	python manage.py purge_data myapp.mymodel --filter created_date__lte=180

The date item is passed a number because it makes more sense to purge data continously based on number of days rather than by a specific date.

All django filters work about the same. For example you can do
	python manage.py purge_data myapp.mymodel --filter field_name__in=[first_value, second_value.....] # or
	python manage.py purge_data myapp.mymodel --filter created_date__lte='2012-04-12'

Schedule purge data
--------------------
	#  To schedule purgedata to run periodically, you need to add the schedule at the bottom of the purgedata/celeryconfig.py file
	add_schedule('purge-sample-data', 'purgedata.tasks.purge_data', '60.0', ('myapp.mymodel', '--filter=created_date__lte=180'))

	purge-sample-data is the beat_schedule, you can name it whatever you want within reason
	purgedata.tasks.purge_data is the name of the task you want to run
	60.0 how often you want to run it. In this case every minute (60.0 seconds)

The remaining arguments have been explained in the Management command section above

If instead of hard coding 60.0seconds you wanted to use crontab to purge data say for example every day at 6:00 am and 6:00 pm, 
you need to set an environment variable and define the crontab values there. 
For example, you can define an environment variable like this:

	PURGE_MYMODEL_DATA_SCHEDULE = '0 6,18' # for 6:00 am and 6:00 pm and then add the schedule thusly:
	add_schedule('purge-mymodel-data', 'purgedata.tasks.purge_data', 'PURGE_MYMODEL_DATA_SCHEDULE', ('purgedata.mymodel', '--filter=created_date__lte=180'))


