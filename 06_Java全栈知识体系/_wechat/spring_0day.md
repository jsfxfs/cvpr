# 【重磅】Spring官方确认：SpringFramework在JDK9+上存在RCE极危漏洞，堪比Log4J漏洞

> Spring官方发布申明：Spring Framework存在远程代码执行漏洞（CVE-2022-22965），在 JDK 9 及以上版本环境下，远程攻击者可利用该漏洞写入恶意代码导致远程代码执行漏洞。鉴于**此漏洞影响范围极大**，建议开发者尽快做好自查，及时更新至最新版本或采取缓解措施。

## 事情的起源

> 3月29日国内有安全团队发现SpringFramework存在RCE（远程代码执行）漏洞，此漏洞不亚于Log4J漏洞造成的影响。

朋友圈也开始调侃

![](https://www.pdai.tech/images/cve-spring-4.png)

但是相关的原始信息均被删除了， 我猜测，删除信息的原因是可能受上次Log4J漏洞阿里团队没有将相关漏洞报告给国家单位被批评有关，所以撤掉了相关信息。

![](https://www.pdai.tech/images/cve-spring-3.png)

现在，Spring官方终于发布此次漏洞的申明和解决方式

![](https://www.pdai.tech/images/cve-spring-1.png)

紧接着，国内一些安全团队也正式证实了相关漏洞的存在，并公布了CVE号码（虽然我还没有查到这个CVE码）

![](https://www.pdai.tech/images/cve-spring-2.png)

## 如何排查是否受漏洞影响

> 如何去排查项目是否受该漏洞影响呢？

### 我的Spring项目是否受此漏洞影响？

> 官方发布的申明中，如果你的当前项目满足如下条件，表示项目受此漏洞的影响：

- JDK 9及以上版本
- 采用Apache Tomcat作为Servlet容器
- 采用WAR包部署方式 (PS: 虽然官方申明是写WAR包方式，实际上JAR包方式依然存在受此漏洞影响的可能)
- 有使用spring-webmvc或者spring-webflux的依赖

### 如何去排查是否中招？

> 结合官方的申明，如何去排查是否受此漏洞影响呢？

1. **JDK版本号排查**

执行“java -version"命令查看运行的JDK版本，如果版本号小于等于8，则不受此漏洞影响。

```bash
java -version
```

2. **Spring Framework排査**

如果项目以**war包形式部署**，按照如下的步骤进行判断。

- 解压war包：将war文件的后级修改成 .zip文件。
- 在解压缩目录下搜索是否存在spring-beans-\*.jar格式的文件（例如spring-beans-5.3.16.jar），如存在则说明业务系统使用了 Spring框架进行开发。
- 如果spring-beans-\*.jar文件不存在，则在解压缩目录下搜索CachedlntrospectionResults.class文件是否存在，如存在则说明业务系统使用了 Spring框架进行开发。

如果项目以**jar包形式**运行，按照如下的步骤进行判断。

- 解压jar包：将jar文件的后缀修改成zip，解压zip 文件。
- 在解压缩目录下搜索是否存在spring-beans-\*.jar格式的jar文件（例如spring-beans-5.3.16.jar），如存在则说明业务系统使用了 Spring框架进行开发。
- 如果spring-beans-\*.jar文件不存在，则在解压缩目录下搜索CachedIntrospectionResults.class文件是否存在，如果存在则说明业务系统使用了 Spring框架进行开发。

3. **综合判断**

在完成以上两个步骤排査后，同时满足以下三个条件可确定受此漏洞影响：

- JDK版本 >= 9；
- 使用Spring框架或衍生框架，同时通过Tomcat进行部署；
- 项目中Web接口使用JavaBean对象作为参数。

## 漏洞处理措施

> 如果项目受此漏洞影响，应该采取什么措施呢？@pdai

### 版本升级

> 目前，Spring官方已发布漏洞修复版本，请用户及时更新至最新版本。

https://github.com/spring-projects/spring-framework/tags

安全版本：

1. Spring Framework == 5.3.18

```xml
<properties>
    <spring-framework.version>5.3.18</spring-framework.version>
</properties>
```

2. Spring Framework == 5.2.20

```xml
<properties>
    <spring-framework.version>5.2.20</spring-framework.version>
</properties>
```

### 漏洞缓解

> 对于无法升级版本的用户，建议采用以下两个临时方案进行防护。

1. **WAF 防护**

在网络防护设备上，根据实际部署业务的流量情况，对 "class.module.\*" 字符串添加过滤规则，在部署过滤规则后，对业务运行情况进行测试，避免产生额外影响。

注意：其中流量特征 "class.module.\*" 对大小写不敏感。

2. **临时修复措施**

需同时按以下两个步骤进行漏洞的临时修复：

- 在应用中全局搜索@InitBinder注解，着看方法体内是否调用`dataBinder.setDisallowedFields`方法，如果发现此代码片段的引入，则在原来的黑名单中添加 `{ " class.module.*"}`。

注意：如果此代码片段使用较多，需要每个地方都追加。

- 在应用系统的项目包下新建以下全局类，并保证这个类被Spring加载到（推荐在Controller所在的包中添加），完成类添加后，需对项目进行重新编译打包和功能验证测试，并重新发布项目。

```java
@ControllerAdvice
@Order(Ordered.LOWEST_PRECEDENCE)
public class BinderControllerAdvice {

    @InitBinder
    public void setAllowedFields(WebDataBinder dataBinder) {
         String[] denylist = new String[]{"class.*", "Class.*", "*.class.*", "*.Class.*"};
         dataBinder.setDisallowedFields(denylist);
    }

}
```

3. **更安全的措施**

> To apply the workaround in a more fail-safe way, applications could extend RequestMappingHandlerAdapter to update the WebDataBinder at the end after all other initialization. In order to do that, a Spring Boot application can declare a WebMvcRegistrations bean (Spring MVC) or a WebFluxRegistrations bean (Spring WebFlux).

官方建议继承RequestMappingHandlerAdapter来在所有其它初始化结束后更新WebDataBinder。如果是Spring Boot的应用，可以在WebMvcRegistrations中配置，官方还给了一个Spring MVC例子：

```java
package car.app;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.web.servlet.WebMvcRegistrations;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.ServletRequestDataBinder;
import org.springframework.web.context.request.NativeWebRequest;
import org.springframework.web.method.annotation.InitBinderDataBinderFactory;
import org.springframework.web.method.support.InvocableHandlerMethod;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter;
import org.springframework.web.servlet.mvc.method.annotation.ServletRequestDataBinderFactory;


@SpringBootApplication
public class MyApp {


	public static void main(String[] args) {
		SpringApplication.run(CarApp.class, args);
	}


	@Bean
	public WebMvcRegistrations mvcRegistrations() {
		return new WebMvcRegistrations() {
			@Override
			public RequestMappingHandlerAdapter getRequestMappingHandlerAdapter() {
				return new ExtendedRequestMappingHandlerAdapter();
			}
		};
	}


	private static class ExtendedRequestMappingHandlerAdapter extends RequestMappingHandlerAdapter {

		@Override
		protected InitBinderDataBinderFactory createDataBinderFactory(List<InvocableHandlerMethod> methods) {

			return new ServletRequestDataBinderFactory(methods, getWebBindingInitializer()) {

				@Override
				protected ServletRequestDataBinder createBinderInstance(
						Object target, String name, NativeWebRequest request) throws Exception {
					
					ServletRequestDataBinder binder = super.createBinderInstance(target, name, request);
					String[] fields = binder.getDisallowedFields();
					List<String> fieldList = new ArrayList<>(fields != null ? Arrays.asList(fields) : Collections.emptyList());
					fieldList.addAll(Arrays.asList("class.*", "Class.*", "*.class.*", "*.Class.*"));
					binder.setDisallowedFields(fieldList.toArray(new String[] {}));
					return binder;
				}
			};
		}
	}
}
```