FROM mysql:5.6

COPY mysql.sh /etc/init.d/mysql.sh
RUN chmod +x /etc/init.d/mysql.sh
COPY start.sh /root

ENTRYPOINT ["/bin/bash", "/root/start.sh"]
EXPOSE 3306
