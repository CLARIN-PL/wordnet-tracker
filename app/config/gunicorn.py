# -*- coding: utf-8 -*-

bind = '0.0.0.0:5000'
workers = 5
timeout = 1000
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'

errorlog = '-'
loglevel= 'debug'
