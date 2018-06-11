Installation
-----------
1. Make sure you have RabbitMQ installed and running.
	Go to this link to get the RabbitMQ for your system:
	https://www.rabbitmq.com/download.html
	
2. If you don't want to use the defaults values, once RabbitMQ is installed and running, 
	go ahead and issue the following commands for linux (For Windows, you will need to run CMD as administrator and ignore the 'sudo's)
	
	$ sudo rabbitmqctl add_user myuser mypassword
	$ sudo rabbitmqctl add_vhost myvhost
	$ sudo rabbitmqctl set_user_tags myuser mytag
	$ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
	
	Substitute in appropriate values for myuser, mypassword, mytag and myvhost above.
	
	For more reading, go to this link:
	http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html

3. Add "purgedata" and "django_celery_results" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        'purgedata',
		'django_celery_results',
    ]

4. Install the requirements from the requirements.txt file

    pip install -r requirements.txt

3. Run `celery -A purgedata worker -l info` to start the celery worker and celery.
	celery 4.0 is not stable on Windows. You will need to either `pip install gevent` and run 
	`celery -A purgedata worker --pool=gevent -l info` for multiple workers or if you don't want to install gevent
	`celery -A purgedata worker --pool=solo -l info`

4. Run `celery -A purgedata beat` to start the celery beat service that will allow scheduling
	Note: You can run `celery -A purgedata worker -B -l info` to run both the worker and beat in development (Not supported on Windows)
	
5. Your scheduled tasks schedules should be up and running