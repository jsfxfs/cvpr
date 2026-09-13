# SpringBoot应用部署 - 使用Docker Compose对容器编排管理

> 如果docker容器是相互依赖的（比如SpringBoot容器依赖另外一个MySQL的数据库容器），那就需要对容器进行编排。本文主要介绍基于Docker Compose的简单容器化编排SpringBoot应用。

## Docker Compose编排管理

> 本例子主要介绍基于SpringBoot + MySQL的应用基于Docker Compose的编排。

### SpringBoot应用准备

> 主要在如下文章的基础上，基于Docker Compose编排部署。

- [SpringBoot集成MySQL - 基于JPA的封装](-SpringBoot集成MySQL - 基于JPA的封装.md)
  - 在实际开发中，最为常见的是基于数据库的CRUD封装等，比如SpringBoot集成MySQL数据库，常用的方式有JPA和MyBatis； 本文主要介绍基于JPA方式的基础封装思路。

### DockerCompose编排

> DockerCompose编排配置如下

- 整体的文件结构

PS: 注意红色的字

![](https://www.pdai.tech/images/spring/springboot/springboot-x-docker-27.png)

- Docker Compose 配置文件

PS：参数可以设置成环境变量注入进来

```yaml
version: "3.1"

services:
  db-mysql:
    image: mysql:8.0.28
    container_name: mysql8
    restart: always
    privileged: true
    volumes:
      # files
      - /usr/local/docker/mysql/files/:/var/lib/mysql-files/
#      # conf
#      - /usr/local/docker/mysql/conf/:/etc/mysql/conf.d/
#      # data
#      - /usr/local/docker/mysql/data/:/var/lib/mysql/
#      # log
#      - /usr/local/docker/mysql/logs/:/var/log/
      # init db by order
      - ./db/:/docker-entrypoint-initdb.d/
    environment:
      TZ : Asia/Shanghai
      MYSQL_ROOT_PASSWORD: bfXa4Pt2lUUScy8jakXf
      MYSQL_DATABASE: test_db
      MYSQL_USER: pdai
      MYSQL_PASSWORD: sdqiireasgadklkklk
    ports:
      - 13306:3306
    command:
      --authentication_policy=mysql_native_password
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_general_ci
      --explicit_defaults_for_timestamp=true
      --lower_case_table_names=1
    networks:
      - internal
  service-app:
    image: springboot-demo-mysql8-jpa
    container_name: springboot-demo-mysql8-jpa
    environment:
      # profile
#      SPRING_PROFILES_ACTIVE: prod
      # or
      SPRING_DATASOURCE_URL: jdbc:mysql://db-mysql:3306/test_db?useSSL=false&autoReconnect=true&characterEncoding=utf8
      SPRING_DATASOURCE_USERNAME: pdai
      SPRING_DATASOURCE_PASSWORD: sdqiireasgadklkklk
    depends_on:
      - db-mysql
    ports:
      - 18080:8080
    networks:
      - internal

networks:
  internal:
    name: internal
```

- SQL

PS: 如果需要有time_zone字段，请参考[Github](https://github.com/docker-library/mysql/issues/229)

```sql
use test_db;

--
-- Table structure for table `tb_role`
--

DROP TABLE IF EXISTS `tb_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `role_key` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_role`
--

LOCK TABLES `tb_role` WRITE;
/*!40000 ALTER TABLE `tb_role` DISABLE KEYS */;
INSERT INTO `tb_role` VALUES (1,'admin','admin','admin','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `phone_number` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (1,'pdai','dfasdf','suzhou.daipeng@gmail.com',1212121213,'afsdfsaf','2021-09-08 17:09:15','2021-09-08 17:09:15');
/*!40000 ALTER TABLE `tb_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_role`
--

DROP TABLE IF EXISTS `tb_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_role`
--

LOCK TABLES `tb_user_role` WRITE;
/*!40000 ALTER TABLE `tb_user_role` DISABLE KEYS */;
INSERT INTO `tb_user_role` VALUES (1,1);
/*!40000 ALTER TABLE `tb_user_role` ENABLE KEYS */;
UNLOCK TABLES;
```

### 测试和校验

通过docker-compose up启动，启动后的日志如下：

```bash
pdai@MacBook-Pro resources % docker-compose up                                                  
Starting mysql8 ... done
Starting springboot-demo-mysql8-jpa ... done
Attaching to mysql8, springboot-demo-mysql8-jpa
mysql8         | 2022-04-20 11:25:49+08:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.28-1debian10 started.
mysql8         | 2022-04-20 11:25:49+08:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
mysql8         | 2022-04-20 11:25:49+08:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.28-1debian10 started.
mysql8         | 2022-04-20T03:25:49.555053Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.28) starting as process 1
mysql8         | 2022-04-20T03:25:49.563364Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
mysql8         | 2022-04-20T03:25:49.832470Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
mysql8         | 2022-04-20T03:25:49.935130Z 0 [System] [MY-010229] [Server] Starting XA crash recovery...
mysql8         | 2022-04-20T03:25:49.943755Z 0 [System] [MY-010232] [Server] XA crash recovery finished.
mysql8         | 2022-04-20T03:25:50.011665Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
mysql8         | 2022-04-20T03:25:50.011719Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
mysql8         | 2022-04-20T03:25:50.013067Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
mysql8         | 2022-04-20T03:25:50.028686Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
mysql8         | 2022-04-20T03:25:50.028772Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.28'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
springboot-demo-mysql8-jpa | 
springboot-demo-mysql8-jpa |   .   ____          _            __ _ _
springboot-demo-mysql8-jpa |  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
springboot-demo-mysql8-jpa | ( ( )___ | '_ | '_| | '_ \/ _` | \ \ \ \
springboot-demo-mysql8-jpa |  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
springboot-demo-mysql8-jpa |   '  |____| .__|_| |_|_| |___, | / / / /
springboot-demo-mysql8-jpa |  =========|_|==============|___/=/_/_/_/
springboot-demo-mysql8-jpa |  :: Spring Boot ::                (v2.5.3)
springboot-demo-mysql8-jpa | 
springboot-demo-mysql8-jpa | 2022-04-20 03:25:50.475  INFO 1 --- [           main] t.p.s.mysql8.jpa.dockercompose.App       : Starting App v1.0-SNAPSHOT using Java 1.8.0_322 on 468363ab8772 with PID 1 (/app.jar started by root in /)
springboot-demo-mysql8-jpa | 2022-04-20 03:25:50.477  INFO 1 --- [           main] t.p.s.mysql8.jpa.dockercompose.App       : The following profiles are active: prod
springboot-demo-mysql8-jpa | 2022-04-20 03:25:51.482  INFO 1 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
springboot-demo-mysql8-jpa | 2022-04-20 03:25:51.557  INFO 1 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 66 ms. Found 2 JPA repository interfaces.
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.135  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.148  INFO 1 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.148  INFO 1 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/9.0.50]
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.203  INFO 1 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.203  INFO 1 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 1682 ms
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.353  INFO 1 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.593  INFO 1 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Start completed.
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.638  INFO 1 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.694  INFO 1 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 5.4.32.Final
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.824  INFO 1 --- [           main] o.hibernate.annotations.common.Version   : HCANN000001: Hibernate Commons Annotations {5.1.2.Final}
springboot-demo-mysql8-jpa | 2022-04-20 03:25:52.941  INFO 1 --- [           main] org.hibernate.dialect.Dialect            : HHH000400: Using dialect: org.hibernate.dialect.MySQLDialect
springboot-demo-mysql8-jpa | 2022-04-20 03:25:53.541  INFO 1 --- [           main] o.h.e.t.j.p.i.JtaPlatformInitiator       : HHH000490: Using JtaPlatform implementation: [org.hibernate.engine.transaction.jta.platform.internal.NoJtaPlatform]
springboot-demo-mysql8-jpa | 2022-04-20 03:25:53.550  INFO 1 --- [           main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'
springboot-demo-mysql8-jpa | 2022-04-20 03:25:54.665  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
springboot-demo-mysql8-jpa | 2022-04-20 03:25:54.930  INFO 1 --- [           main] t.p.s.mysql8.jpa.dockercompose.App       : Started App in 4.854 seconds (JVM running for 5.267)
```

- 查看mysql db是否正确创建

（注意：也可以不开放端口，通过服务名进行内部网络通信）

```bash
pdai@MacBook-Pro conf % docker exec -it mysql8 /bin/bash  
root@028760cee140:/# mysql -u pdai -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.28 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| test_db            |
+--------------------+
2 rows in set (0.00 sec)

mysql> use test_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+-------------------+
| Tables_in_test_db |
+-------------------+
| tb_role           |
| tb_user           |
| tb_user_role      |
+-------------------+
3 rows in set (0.00 sec)

mysql>
```

- 访问服务

通过对外端口18080进行访问

![](https://www.pdai.tech/images/spring/springboot/springboot-x-docker-26.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos