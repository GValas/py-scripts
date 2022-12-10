FROM python:3.11
WORKDIR /workspace
ADD requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 12001