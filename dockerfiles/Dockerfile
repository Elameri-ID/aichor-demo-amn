FROM python:3.8-slim

RUN pip install tensorboardX boto3
RUN ls /
WORKDIR /app
COPY ./src ./src
COPY main.py . 


#RUN --mount=type=cache,target=/root/.cache/uv \
 #   echo "CACHE TEST Aymen 3 $(date)" > /root/.cache/uv/test3.txt && \
 #   cat /root/.cache/uv/test3.txt && \
 #   cat /root/.cache/uv/test2.txt