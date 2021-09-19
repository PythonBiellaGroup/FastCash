FROM postgres:13.2

RUN mkdir -p /project/backup/
RUN mkdir -p /project/query/


#COPY backup/propaganda.sql /project/backup/
#COPY init.sql /docker-entrypoint-initdb.d/

# install python

# launch postgres
CMD ["postgres"]