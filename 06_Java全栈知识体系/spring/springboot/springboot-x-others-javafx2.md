# ▶SpringBoot集成JavaFX2 - JavaFX 2.0应用

> 很多人对Java开发native程序第一反应还停留在暗灰色单一风格的Java GUI界面，开发方式还停留在AWT或者Swing。本文主要基于SpringBoot和JavaFX开发一个Demo给你展示Java Native应用可以做到什么样的程度。当然JavaFX 2.0没有流行起来也是有原因的，而且目前native的选择很多，前端是个框架都会搞个native... @pdai

## 技术背景

- Springboot 请参考SpringBoot章节
- JavaFX 2.0 请参考(fxml,css,controller)

[2.1.6.12 Java8 JavaFx](../../java/java8/java8-javafx.md)

## Demo介绍

- Loader

![](https://www.pdai.tech/images/spring/springboot-javafx-app-1.png)

- 和WEB一样风格的GUI

![](https://www.pdai.tech/images/spring/springboot-javafx-app-2.png)

- Popup

![](https://www.pdai.tech/images/spring/springboot-javafx-app-3.png)

- Webview

![](https://www.pdai.tech/images/spring/springboot-javafx-app-4.png)

- Theme

![](https://www.pdai.tech/images/spring/springboot-javafx-app-5.png)

- Message/Configuration...

![](https://www.pdai.tech/images/spring/springboot-javafx-app-6.png)

- FullScreen/Max/Min/Close

> 包括全屏是基于JavaFX的一个组件，不是原生。

![](https://www.pdai.tech/images/spring/springboot-javafx-app-7.png)

## 如何部署

> 收到几个开发问如何进行运行和部署，统一回复下：

- 安装jar到本地的maven库

![](https://www.pdai.tech/images/spring/springboot-javafx-app-10.png)

具体执行maven安装的脚本如下（这里D:\git\github\springboot-javafx-app-demo是我本地的项目目录，需要改成你自己的）：

```bash
mvn install:install-file -DgroupId=gn -DartifactId=GNCalendar -Dversion=v1.0 -Dpackaging=jar -Dfile=D:\git\github\springboot-javafx-app-demo\lib\GNCalendar-1.0-alpha.jar

mvn install:install-file -DgroupId=gn -DartifactId=GNButton -Dversion=v1.1.0 -Dpackaging=jar -Dfile=D:\git\github\springboot-javafx-app-demo\lib\GNButton-1.1.0.jar

mvn install:install-file -DgroupId=gn -DartifactId=GNCarousel -Dversion=v2.1.5 -Dpackaging=jar -Dfile=D:\git\github\springboot-javafx-app-demo\lib\GNCarousel-2.1.5.jar

mvn install:install-file -DgroupId=gn -DartifactId=GNDecorator -Dversion=v2.1.2-alpha -Dpackaging=jar -Dfile=D:\git\github\springboot-javafx-app-demo\lib\GNDecorator-2.1.2-alpha.jar

mvn install:install-file -DgroupId=gn -DartifactId=GNAvatarView -Dversion=v1.0-rc -Dpackaging=jar -Dfile=D:\git\github\springboot-javafx-app-demo\lib\GNAvatarView-1.0-rc.jar
```

在这里执行：

![](https://www.pdai.tech/images/spring/springboot-javafx-app-8.png)

- 编译的maven插件

![](https://www.pdai.tech/images/spring/springboot-javafx-app-9.png)

- pom.xml如下

```java
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
	<modelVersion>4.0.0</modelVersion>
	<parent>
		<groupId>org.springframework.boot</groupId>
		<artifactId>spring-boot-starter-parent</artifactId>
		<version>2.1.4.RELEASE</version>
		<relativePath /> <!-- lookup parent from repository -->
	</parent>
	<groupId>com.example</groupId>
	<artifactId>spring-fx-app</artifactId>
	<version>0.0.1-SNAPSHOT</version>
	<name>spring-fx-app</name>
	<description>Demo project for Spring Boot</description>

	<properties>
		<java.version>1.8</java.version>
	</properties>

	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter</artifactId>
		</dependency>

		<!-- mvn install:install-file -DgroupId=gn -DartifactId=GNAvatarView -Dversion=v1.0-rc -Dpackaging=jar -Dfile=D:\git\github\springb
oot-javafx-app-demo\lib\GNAvatarView-1.0-rc.jar
-->
		<dependency>
			<groupId>gn</groupId>
			<artifactId>GNAvatarView</artifactId>
			<version>v1.0-rc</version>
		</dependency>
		<dependency>
			<groupId>gn</groupId>
			<artifactId>GNButton</artifactId>
			<version>v1.1.0</version>
		</dependency>
		<dependency>
			<groupId>gn</groupId>
			<artifactId>GNCalendar</artifactId>
			<version>v1.0</version>
		</dependency>
		<dependency>
			<groupId>gn</groupId>
			<artifactId>GNCarousel</artifactId>
			<version>v2.1.5</version>
		</dependency>
		<dependency>
			<groupId>gn</groupId>
			<artifactId>GNDecorator</artifactId>
			<version>v2.1.2-alpha</version>
		</dependency>

		<!-- https://mvnrepository.com/artifact/io.github.typhon0/AnimateFX -->
		<dependency>
			<groupId>io.github.typhon0</groupId>
			<artifactId>AnimateFX</artifactId>
			<version>1.2.1</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/org.controlsfx/controlsfx -->
		<dependency>
			<groupId>org.controlsfx</groupId>
			<artifactId>controlsfx</artifactId>
			<version>8.40.14</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/de.jensd/fontawesomefx -->
		<dependency>
			<groupId>de.jensd</groupId>
			<artifactId>fontawesomefx</artifactId>
			<version>8.9</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/com.jfoenix/jfoenix -->
		<dependency>
			<groupId>com.jfoenix</groupId>
			<artifactId>jfoenix</artifactId>
			<version>8.0.7</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/eu.hansolo/tilesfx -->
		<dependency>
			<groupId>eu.hansolo</groupId>
			<artifactId>tilesfx</artifactId>
			<version>1.6.5</version>
		</dependency>
		<!-- https://mvnrepository.com/artifact/eu.hansolo/colors -->
		<dependency>
			<groupId>eu.hansolo</groupId>
			<artifactId>colors</artifactId>
			<version>1.4</version>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>
	</dependencies>

	<build>
		<plugins>
<!--			<plugin>-->
<!--				<groupId>org.springframework.boot</groupId>-->
<!--				<artifactId>spring-boot-maven-plugin</artifactId>-->
<!--			</plugin>-->

				<plugin>
					<groupId>com.zenjava</groupId>
					<artifactId>javafx-maven-plugin</artifactId>
					<version>8.8.3</version>
					<configuration>
						<vendor>pdai</vendor>
						<mainClass>com.pdai.javafx.app.SpringFxAppApplication</mainClass>
						<allPermissions>true</allPermissions>
					</configuration>
				</plugin>
		</plugins>
	</build>

</project>
```

- 以jar运行为例：

```bash
D:\git\github\springboot-javafx-app-demo>java -jar D:\git\github\springboot-javafx-app-demo\target\jfx\native\spring-fx-app-0.0.1-SNAPSHOT\app\spring-fx-app-0.0.1-SNAPSHOT-jfx.jar

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |___, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v2.1.4.RELEASE)

2020-07-01 06:27:46.091  INFO 144952 --- [onPool-worker-1] o.s.boot.SpringApplication               : Starting application on pdai with PID 144952 (started by pdai in D:\git\github\springboot-javafx-app-demo)
2020-07-01 06:27:46.099  INFO 144952 --- [onPool-worker-1] o.s.boot.SpringApplication               : No active profile set, falling back to default profiles: default
2020-07-01 06:27:47.099  INFO 144952 --- [onPool-worker-1] o.s.boot.SpringApplication               : Started application in 1.784 seconds (JVM running for 2.838)
2020-07-01 06:27:47.163  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:51.932  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:53.084  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:54.166  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:54.207  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:54.263  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:54.322  WARN 144952 --- [JavaFX-Launcher] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:56.569  WARN 144952 --- [lication Thread] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:56.590  WARN 144952 --- [lication Thread] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:56.694  WARN 144952 --- [lication Thread] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
2020-07-01 06:27:56.707  WARN 144952 --- [lication Thread] javafx                                   : Loading FXML document with JavaFX API of version 8.0.171 by JavaF
X runtime of version 8.0.65
```

## 示例代码

@See https://github.com/realpdai/springboot-javafx-app-demo