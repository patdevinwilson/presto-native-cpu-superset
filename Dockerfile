FROM apache/superset:latest
RUN pip install psycopg2-binary pyhive presto-python-client