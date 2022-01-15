FROM python:3.9.6-alpine3.14 AS compile-image

# Copy pip requiremetns file to container
COPY requirements.txt /requirements.txt

RUN python3 -m ensurepip
RUN pip install --upgrade pip setuptools --no-cache-dir

##Libraries needed
RUN apk --no-cache add --virtual build-dependencies build-base libffi-dev openssl-dev libxslt-dev libxml2-dev 

RUN python3 -m venv /opt/.venv --system-site-packages

# Make sure we use the virtualenv:
ENV PATH="/opt/.venv/bin:$PATH"

# install requs
RUN pip3 install --no-cache-dir -r requirements.txt 

# Final image
FROM python:3.9.6-alpine3.14

RUN apk --no-cache add tzdata \
 && cp /usr/share/zoneinfo/Europe/Helsinki /etc/localtime \
 && echo "Europe/Helsinki" >  /etc/timezone \
 && apk --no-cache del tzdata && apk update --no-cache && apk --no-cache upgrade

# create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

#Install app
ARG APP_PATH=/app
RUN mkdir ${APP_PATH}

# copy venv from compile-image
COPY --from=compile-image /opt/.venv ${APP_PATH}/.venv


# create input folder and rights to write
RUN mkdir ${APP_PATH}/input
RUN chown -R appuser:appgroup /${APP_PATH}/input


COPY src/*.py ${APP_PATH}/


COPY src/*.pem ${APP_PATH}

# use non-root user
USER appuser

# Make sure we use the virtualenv:
ENV PATH="${APP_PATH}/.venv/bin:$PATH"

WORKDIR /app

CMD ["python", "/app/main.py"]