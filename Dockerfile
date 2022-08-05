FROM python:3

WORKDIR /19179422_CarDealership
ADD . /19179422_CarDealership

COPY requirements.txt /tmp/requirements.txt
RUN pip install numpy --use-deprecated=legacy-resolver
RUN pip install matplotlib --use-deprecated=legacy-resolver
RUN pip install -r /tmp/requirements.txt
RUN pip install pymongo
RUN pip install pymongo[srv]

EXPOSE 5000

CMD [ "python", "wsgi.py" ]