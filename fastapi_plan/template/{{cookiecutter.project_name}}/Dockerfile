FROM nginx/unit:1.23.0-python3.9

# Our Debian with Python and Nginx for python apps.
# See https://hub.docker.com/r/nginx/unit/
ENV PYTHONUNBUFFERED 1

COPY ./app/initial.sh /docker-entrypoint.d/initial.sh
COPY ./config/config.json /docker-entrypoint.d/config.json

# Ok, this is something we get thanks to the Nginx Unit Image.
# We don't need to call stuff like
# curl -X PUT --data-binary @config.json --unix-socket \
#       /path/to/control.unit.sock http://localhost/config/
# to set our configuration
# Becouse as stated in docs https://unit.nginx.org/installation/#docker-images,
# configuration snippets are
# uploaded as to the config section of Unit’s configuration
# That means we only have to copy our config.json file to the folder
# /docker-entrypoint.d/

RUN mkdir build

# We create folder named build for our app.
WORKDIR /build

COPY ./app ./app
COPY ./pytest.ini .
COPY ./aerich.ini .
COPY ./requirements.txt .
COPY ./.env .

# We copy our app folder to the /build

RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

# OK, that looks strange but here's a explanation from Nginx docs
# https://unit.nginx.org/howto/docker/:

# """ PIP isn't installed by default, so we install it first.
# Next, we install the requirements, remove PIP, and perform image cleanup. """

# Note we use /build/requirements.txt since this is our file
