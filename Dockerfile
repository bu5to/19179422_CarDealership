FROM python:3

WORKDIR /19179422_CarDealership
ADD . /19179422_CarDealership

COPY requirements.txt /tmp/requirements.txt
RUN pip install numpy --use-deprecated=legacy-resolver
RUN pip install matplotlib --use-deprecated=legacy-resolver
RUN pip install -r /tmp/requirements.txt
RUN pip install pymongo
RUN pip install pymongo[srv]
ENV MONGO_CLIENT=mongodb+srv://19179422:soft7011@cluster0.whl83.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
ENV DATABASE_URL=postgresql://irfthlqtvpqjek:35496e5703ba65a8c9fe2a2075e9d4395a7aa6e29ccc710c8f3966ea4eea7ba5@ec2-99-81-16-126.eu-west-1.compute.amazonaws.com:5432/d6iso2pc6h1bkj

EXPOSE 5000
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
CMD [ "python", "wsgi.py" ]
