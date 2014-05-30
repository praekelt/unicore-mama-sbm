# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Preakelt Foundation dev@praekelt.com

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip python-virtualenv

# Copy the application folder inside the container
RUN git clone https://github.com/praekelt/unicore-mama-sbm.git

#Install dependencies
WORKDIR /unicore-mama-sbm
RUN git pull
RUN virtualenv ve
RUN ve/bin/pip install -r requirements.pip


# Set the default directory where CMD will execute
WORKDIR /unicore-mama-sbm/mamasbm

# Run database migrations
CMD ../ve/bin/alembic upgrade head

# Expose ports
EXPOSE 8000

# Set the default command to execute
# when creating a new container
CMD ../ve/bin/gunicorn --paste production.ini --chdir .
