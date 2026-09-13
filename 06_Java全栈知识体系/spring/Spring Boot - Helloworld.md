# Spring Boot - Helloworld

> 使用Intelli IDEA写一个SpringBoot的HelloWorld。 @pdai

## 创建 SpringBoot Web 应用

- 选择 Spring Initialize

![](https://www.pdai.tech/images/spring/springboot-helloworld-1.png)

- 填写 GAV三元组

![](https://www.pdai.tech/images/spring/springboot-helloworld-2.png)

- 选择初始化模块

![](https://www.pdai.tech/images/spring/springboot-helloworld-3.png)

- 项目名

![](https://www.pdai.tech/images/spring/springboot-helloworld-4.png)

## 初始化后内容

- README.md

![](https://www.pdai.tech/images/spring/springboot-helloworld-5.png)

- .gitignore

```json
HELP.md
target/
!.mvn/wrapper/maven-wrapper.jar
!**/src/main/**
!**/src/test/**

## STS ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache

## IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr

## NetBeans ###
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/
build/

## VS Code ###
.vscode/
```

- pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.1.7.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
    <groupId>com.pdai</groupId>
    <artifactId>springboot-helloworld</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <name>springboot-helloworld</name>
    <description>Demo project for Spring Boot</description>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

# 示例源码

https://github.com/realpdai/springboot-helloworld-demo