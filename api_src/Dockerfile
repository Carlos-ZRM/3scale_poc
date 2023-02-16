FROM openjdk-8 as API_BUILD
COPY --chown=jboss:jboss . /opt/api/
WORKDIR /opt/api/
RUN mvn package

FROM openjdk-8 as api-info
COPY --from=API_BUILD --chown=jboss:jboss /opt/api/target/poc-0.0.1-SNAPSHOT.jar /opt/api/api-info.jar
EXPOSE 8088
ENTRYPOINT ["java","-jar","/opt/api/api-info.jar"]
# RUN mvnw package

# FROM  registry.redhat.io/ubi8/openjdk-8

# COPY target/poc-0.0.1-SNAPSHOT.jar app.jar
# EXPOSE 8088

# ENTRYPOINT ["java","-jar","/app.jar"]
