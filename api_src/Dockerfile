FROM ubi8/openjdk-8:1.14-14.1675788284 as API_BUILD
COPY --chown=jboss:jboss . /opt/api/
WORKDIR /opt/api/
RUN  ls
RUN mvn package

FROM ubi8/openjdk-8:1.14-14.1675788284 as api-info
COPY --from=API_BUILD --chown=jboss:jboss /opt/api/target/poc-0.0.1-SNAPSHOT.jar /opt/api/api-info.jar
EXPOSE 8088
ENTRYPOINT ["java","-jar","/opt/api/api-info.jar"]
# RUN mvnw package

# FROM  registry.redhat.io/ubi8/openjdk-8

# COPY target/poc-0.0.1-SNAPSHOT.jar app.jar
# EXPOSE 8088

# ENTRYPOINT ["java","-jar","/app.jar"]
