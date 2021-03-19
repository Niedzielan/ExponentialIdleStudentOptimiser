FROM python:3.8
COPY requirements.txt ./requirements.txt
COPY main.py ./main.py
COPY static/ ./static/
COPY StudentOptimiser.py ./StudentOptimiser.py
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]