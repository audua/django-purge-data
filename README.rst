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
.. highlight:: html
	<html><head></head><h5>To purge <i><strong>all</strong></i> data of a given model from python manage.py, run:</h5><html>
.. highlight:: none

.. code-block:: python
	#  this command will purge all data for mymodel model in myapp app.
	python manage.py purge_data myapp.mymodel --all   #  or equivalently
	python manage.py purge_data myapp.mymodel -a
.. code-block:: none

Note that the name of the app is case-sensitive and that you can use `--all` or `-a` interchangibly

.. highlight:: html
	<html><head></head><h5>To purge data of a given model based on a filter, run:</h5><html>
.. highlight:: none

.. code-block:: python
	#  for example, to purge data older than 6 months on a model with a DateTimeField or DateField called `created_date`, run:
	python manage.py purge_data myapp.mymodel --filter created_date__lte=180
.. code-block:: none

The date item is passed a number because it makes more sense to purge data continously based on number of days rather than by a specific date.

All django filters work about the same. For example you can do
.. code-block:: python
	python manage.py purge_data myapp.mymodel --filter field_name__in=[first_value, second_value.....] # or
	python manage.py purge_data myapp.mymodel --filter created_date__lte='2012-04-12'
.. code-block:: none

Schedule purge data
--------------------
.. highlight:: html
	To schedule purgedata to run periodically, you need to add the schedule at the bottom of the <html><head></head><i><strong>purgedata/celeryconfig.py file</strong></i></html>
.. highlight:: none
.. code-block:: python
	add_schedule('purge-sample-data', 'purgedata.tasks.purge_data', '60.0', ('myapp.mymodel', '--filter=created_date__lte=180'))
.. code-block:: none

.. highlight:: html
	<html><head></head><i><strong>purge-sample-data</strong></i></html> is the beat_schedule, you can name it whatever you want within reason
	<html><head></head><i><strong>purgedata.tasks.purge_data</strong></i></html> is the name of the task you want to run
	<html><head></head><i><strong>60.0</strong></i></html> how often you want to run it. In this case every minute (60.0 seconds)
.. highlight:: none

The remaining arguments have been explained in the Management command section above
.. highlight:: html
If instead of hard coding<html><head></head><i><strong>60.0</strong></i></html>seconds you wanted to use crontab 
to purge data say for example every day at <html><head></head><i><strong>6:00 am and 6:00 pm</strong></i></html>, you need to set an environment variable and define the crontab values there. 
.. highlight:: none
For example, you can define an environment variable like this:
.. code-block:: python
	PURGE_MYMODEL_DATA_SCHEDULE = '0 6,18' # for 6:00 am and 6:00 pm and then add the schedule thusly:
	add_schedule('purge-mymodel-data', 'purgedata.tasks.purge_data', 'PURGE_MYMODEL_DATA_SCHEDULE', ('purgedata.mymodel', '--filter=created_date__lte=180'))
.. code-block:: none

