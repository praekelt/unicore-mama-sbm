# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Preakelt Foundation dev@praekelt.com

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ trusty main universe" >> /etc/apt/sources.list

# Add the praekelt resources URL
RUN echo "deb http://repo:4b1ec522503c942a364de702deaf1402@apt.praekelt.com/qa/ trusty main" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Copy the application folder inside the container
ADD /mamasbm /mamasbm

# Install the mama sbm app
RUN apt-get install -y unicore-mama-sbm --force-yes

# Expose ports
EXPOSE 8000

# Set the default directory where CMD will execute
WORKDIR /var/praekelt/unicore-mama-sbm/mamasbm

# Run database migrations
CMD /var/praekelt/python/bin/alembic upgrade head

# Set the default command to execute
# when creating a new container
CMD /var/praekelt/python/bin/gunicorn --paste production.ini --chdir .
