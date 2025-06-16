FROM rayproject/ray:2.23.0-cpu

COPY build/requirements.txt .
RUN pip install -r requirements.txt

#RUN --mount=type=cache,target=/root/.cache/uv \
#    cat /root/.cache/uv/test.txt

WORKDIR /app
COPY ./src ./src
COPY main.py .