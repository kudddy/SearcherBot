nohup /opt/bitnami/scripts/memcached/run.sh &
# /opt/bitnami/scripts/memcached/run.sh
nohup python3 sheduller.py &
# python3 sheduller.py
exec gunicorn -w 1 -b :8080 main:app
