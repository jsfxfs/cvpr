# SpringBoot应用部署 - 打包成war部署

> 前文我们知道SpringBoot web项目默认打包成jar部署是非常方便的，那什么样的场景下还会打包成war呢？本文主要介绍SpringBoot应用打包成war包的示例。@pdai

## 概述

> 前文我们知道SpringBoot web项目默认打包成jar部署是非常方便的，那什么样的场景下还会打包成war呢？

这主要是由于在早期没有SpringBoot时，一些老的项目已经通过Tomcat独立部署war包，并构建了相应的部署体系和闭环。而且对于老的成熟的项目不期望在投入精力去升级和改造，只需要最小大家的保证运行稳定，为了投入和产出的平衡。

在这种情况下，如果有一些必要性的更新（比如高危漏洞的修复），需要编译成war包。

## 打包成war

> 这里以一个Helloworld项目（[SpringBoot入门 - 创建第一个Hello world工程](springboot-x-hello-world.md)）为例打包成war。

### 将pom中packaging设置为war类型

默认是jar类型，需要添加或者改成war类型

```xml
<groupId>tech.pdai</groupId>
<artifactId>103-springboot-demo-helloworld-build-war</artifactId>
<packaging>war</packaging>
<version>1.0-SNAPSHOT</version>
```

### 移除内嵌的Tomcat，并增加servlet-api的依赖包

因为默认内嵌了tomcat，所以需要移除；并增加servlet-api相关的包。

![](https://www.pdai.tech/images/spring/springboot/springboot-x-war-1.png)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <artifactId>spring-boot-starter-tomcat</artifactId>
            <groupId>org.springframework.boot</groupId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <scope>provided</scope>
</dependency>
```

### 启动类继承SpringBootServletInitialize

修改项目默认启动方式，启动类继承SpringBootServletInitializer类并重写configure()方法

![](https://www.pdai.tech/images/spring/springboot/springboot-x-war-2.png)

完整代码如下

```java
/**
 * @author pdai
 */
@SpringBootApplication
@RestController
public class SpringBootHelloWorldApplication extends SpringBootServletInitializer {

    /**
     * main interface.
     *
     * @param args args
     */
    public static void main(String[] args) {
        SpringApplication.run(SpringBootHelloWorldApplication.class, args);
    }

    /**
     * hello world.
     *
     * @return hello
     */
    @GetMapping("/hello")
    public ResponseEntity<String> hello() {
        return new ResponseEntity<>("hello world", HttpStatus.OK);
    }

    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder builder) {
        return builder.sources(SpringBootHelloWorldApplication.class);
    }
}
```

### maven打包成war的插件

使用maven-war-plugin插件进行打包

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <version>3.3.1</version>
    <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
    </configuration>
</plugin>
```

### 打包测试

通过maven 进行打包测试

![](https://www.pdai.tech/images/spring/springboot/springboot-x-war-3.png)

## 进一步理解

> 通过几个问题进一步理解。

### 如何将三方jar打包进来？

> 在项目中我们经常需要使用第三方的Jar，比如某些SDK，这些SDK没有直接发布到公开的maven仓库中，这种情况下如何使用这些三方JAR呢？

请参看：[SpringBoot应用部署 - 使用第三方JAR包](springboot-x-deploy-jar-3rd.md)

### 如何打包成jar包呢？

请参看：[SpringBoot应用部署 - 打包成jar部署](springboot-x-deploy-jar.md)

### 如何打包成docker镜像呢？

请参看：[SpringBoot应用部署 - 打包成docker镜像](springboot-x-deploy-docker.md)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos