FROM elasticsearch:6.4.2
COPY start.sh /root

COPY elasticsearch.sh /etc/init.d/elasticsearch.sh
RUN chmod +x /etc/init.d/elasticsearch.sh


ENTRYPOINT ["/bin/bash", "/root/start.sh"]
