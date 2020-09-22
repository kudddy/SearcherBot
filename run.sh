nohup /opt/bitnami/scripts/memcached/run.sh &
# /opt/bitnami/scripts/memcached/run.sh
nohup python3 sheduller.py &
# python3 sheduller.py
exec gunicorn -w 2 -b :8080 main:app
