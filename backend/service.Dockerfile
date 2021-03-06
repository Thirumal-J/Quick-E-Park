FROM python:latest
RUN apt-get update  
WORKDIR /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt
# COPY start-service.sh /backend/start-service.sh
# EXPOSE 4001-4004
# RUN ["chmod", "+x", "/backend/start-service.sh"]
# ENTRYPOINT ["/backend/start-service.sh"]