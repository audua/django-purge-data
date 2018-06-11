Installation
-------------
1. Make sure you have RabbitMQ installed and running.

	Go to this link to get the RabbitMQ for your system:
	https://www.rabbitmq.com/download.html
	
2. If you don't want to use the defaults values, once RabbitMQ is installed and running, go ahead and issue the following commands for linux (For Windows, you will need to run CMD as administrator and ignore the ``sudo``)::
	
		$ sudo rabbitmqctl add_user myuser mypassword
		$ sudo rabbitmqctl add_vhost myvhost
		$ sudo rabbitmqctl set_user_tags myuser mytag
		$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
	
	Substitute in appropriate values for myuser, mypassword, mytag and myvhost above.
	
	For more reading, go to this link:
	http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html

3. Add **purgedata** and **django_celery_results** to your INSTALLED_APPS setting like this::

		INSTALLED_APPS = [
			...
			'purgedata',
			'django_celery_results',
		]

4. Install the requirements from the requirements.txt file::

		`pip install -r requirements.txt`

3. Run ``celery -A purgedata worker -l info`` to start the celery worker. Celery 4.0 is not stable on Windows. To run celery 4.0 on Windows, you will need to either::
	
	`pip install gevent` and run 
	`celery -A purgedata worker --pool=gevent -l info` if you want concurrency for your tasks. If you don't want to install gevent, you can run
	`celery -A purgedata worker --pool=solo -l info` but this allows only a single threaded execution pool

4. Run ``celery -A purgedata beat`` to start the celery beat service. This will allow your periodic tasks to run.
	Note: You can run ``celery -A purgedata worker -B -l info`` to run both the worker and beat in development (Not supported on Windows)
	
5. Your scheduled tasks should be up and running