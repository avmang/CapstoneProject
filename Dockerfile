FROM eclipse-temurin:17-jdk AS build

WORKDIR /build

RUN apt-get update && apt-get install -y maven

COPY pom.xml .
COPY src ./src

RUN mvn clean install -DskipTests

FROM eclipse-temurin:17-jre AS runtime 

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser

WORKDIR /build

COPY --from=build /build/target/spring-petclinic-*.jar app.jar

RUN chown appuser:appgroup app.jar

USER appuser

RUN chmod 500 app.jar

EXPOSE 8080

CMD ["java", "-jar", "app.jar"]