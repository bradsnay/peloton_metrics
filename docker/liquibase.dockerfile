FROM liquibase:latest

ADD ./liquibase /liquibase/changelog

RUN echo "changelogFile=./changelog/changelog.xml" > /liquibase/liquibase.properties
RUN echo "liquibase.command.url=jdbc:postgresql://postgres:5432/peloton_metrics" >> /liquibase/liquibase.properties

USER root

RUN --mount=type=secret,id=postgres_user \
    echo "liquibase.command.username: $(cat /run/secrets/postgres_user)" >> /liquibase/liquibase.properties
RUN --mount=type=secret,id=postgres_root_pw \
    echo "liquibase.command.password: $(cat /run/secrets/postgres_root_pw)" >> /liquibase/liquibase.properties

USER liquibase
