FROM mongo:3.6-stretch

COPY mongod.conf /etc/mongod.conf

COPY mongodb.sh /etc/init.d/mongodb.sh
RUN chmod +x /etc/init.d/mongodb.sh

COPY start.sh /root

ENTRYPOINT ["/bin/bash", "/root/start.sh"]
