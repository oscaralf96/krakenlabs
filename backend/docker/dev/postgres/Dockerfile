FROM postgres:15-bullseye


COPY ./docker/dev/postgres/maintenance /usr/dev/bin/maintenance

RUN chmod +x /usr/dev/bin/maintenance/*

RUN mv /usr/dev/bin/maintenance/* /usr/dev/bin \
  && rmdir /usr/dev/bin/maintenance