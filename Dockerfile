FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install --upgrade pip; apk add build-base; pip install numpy
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "server.py", "--search", "olympics", "--limit", "10", "--interval", "100"]