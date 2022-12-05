##### Python Build Imgae #####

FROM python:3.7-slim-buster

LABEL maintainer="25530573+max533@users.noreply.github.com"

ENV PYTHONUNBUFFERED 1

RUN echo "deb http://opensource.nchc.org.tw/debian/ buster main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ buster-proposed-updates main" >> /etc/apt/sources.list

# To avoid execute with root permission, it create reporter user and group
RUN addgroup reporter \
  && adduser --gecos "" --ingroup reporter reporter

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install --no-install-recommends -y cron=3.0pl1-134+deb10u1 \
  # cleaning up unused files
  && rm -rf /etc/cron.*/* \
  # add crontab shell script
  && echo '30 8 * * 1-5 /bin/bash /app/compose/health_report_cron.sh > /proc/1/fd/1 2>&1' >> /etc/cron.d/report_cron \
  # apply crontab shell script
  && crontab -u reporter /etc/cron.d/report_cron \
  # change cron bin permission
  && chmod u+s /usr/sbin/cron

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY ./compose/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod u+x /docker-entrypoint.sh \
  && chown reporter /docker-entrypoint.sh

# Set source code to app home directoty
COPY --chown=reporter:reporter . /app

RUN chmod u+x /app/compose/start \
  && chmod u+x /app/compose/health_report_cron.sh

ENV APP_HOME=/app

ENTRYPOINT [ "/docker-entrypoint.sh" ]

USER reporter

WORKDIR ${APP_HOME}
