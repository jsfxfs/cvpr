# SpringBoot接口 - 如何参数校验国际化

> 上文我们学习了如何对SpringBoot接口进行参数校验，但是如果需要有国际化的信息（比如返回校验结果有中英文），应该如何优雅处理呢？@pdai

## 什么是国际化

软件的国际化：软件开发时，要使它能同时应对世界不同地区和国家的访问，并针对不同地区和国家的访问，提供相应的、符合来访者阅读习惯的页面或数据。国际化又称为 i18n：internationalization

## 实现案例

> 这里实现一个案例: 语言切换和国际化（中英文）验证信息。

### 定义资源文件

在Resources下添加如下：

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-4.png)

填写名称和资源语言类型

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-3.png)

添加中英文对应的message

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-5.png)

### 使用message

```java
@Data
@Builder
@ApiModel(value = "User", subTypes = {AddressParam.class})
public class UserParam implements Serializable {

    private static final long serialVersionUID = 1L;

    @NotEmpty(message = "{user.msg.userId.notEmpty}") // 这里
    private String userId;
```

### 中英文切换拦截

由于默认是拦截request参数获取locale参数来实现的切换语言，这里我们可以改下，优先从header中获取，如果没有获取到再从request参数中获取。

```java
package tech.pdai.springboot.validation.i18n.config;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import lombok.extern.slf4j.Slf4j;
import org.springframework.lang.NonNull;
import org.springframework.util.ObjectUtils;
import org.springframework.web.servlet.LocaleResolver;
import org.springframework.web.servlet.i18n.LocaleChangeInterceptor;
import org.springframework.web.servlet.support.RequestContextUtils;

/**
 * custom locale change interceptor.
 *
 * @author pdai
 */
@Slf4j
public class CustomLocaleChangeInterceptor extends LocaleChangeInterceptor {

    /**
     * try to get locale from header, if not exist then get it from request parameter.
     *
     * @param request  request
     * @param response response
     * @param handler  handler
     * @return bool
     * @throws ServletException ServletException
     */
    @Override
    public boolean preHandle(HttpServletRequest request, @NonNull HttpServletResponse response, @NonNull Object handler) throws ServletException {
        String newLocale = request.getHeader(getParamName());
        if (newLocale!=null) {
            if (checkHttpMethods(request.getMethod())) {
                LocaleResolver localeResolver = RequestContextUtils.getLocaleResolver(request);
                if (localeResolver==null) {
                    throw new IllegalStateException("No LocaleResolver found: not in a DispatcherServlet request?");
                }
                try {
                    localeResolver.setLocale(request, response, parseLocaleValue(newLocale));
                } catch (IllegalArgumentException ex) {
                    if (isIgnoreInvalidLocale()) {
                        log.debug("Ignoring invalid locale value [" + newLocale + "]: " + ex.getMessage());
                    } else {
                        throw ex;
                    }
                }
            }
            return true;
        } else {
            return super.preHandle(request, response, handler);
        }
    }

    private boolean checkHttpMethods(String currentMethod) {
        String[] configuredMethods = getHttpMethods();
        if (ObjectUtils.isEmpty(configuredMethods)) {
            return true;
        }
        for (String configuredMethod : configuredMethods) {
            if (configuredMethod.equalsIgnoreCase(currentMethod)) {
                return true;
            }
        }
        return false;
    }
}
```

初始化相关配置

```java
package tech.pdai.springboot.validation.i18n.config;

import java.util.Locale;

import lombok.RequiredArgsConstructor;
import org.springframework.boot.validation.MessageInterpolatorFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.support.ResourceBundleMessageSource;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;
import org.springframework.web.servlet.LocaleResolver;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import org.springframework.web.servlet.i18n.LocaleChangeInterceptor;
import org.springframework.web.servlet.i18n.SessionLocaleResolver;

/**
 * This class is for web config.
 *
 * @author pdai
 */
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    /**
     * lang param name in header, default to 'locale'.
     */
    private static final String LANGUAGE_PARAM_NAME = LocaleChangeInterceptor.DEFAULT_PARAM_NAME;

    /**
     * message source.
     */
    private final ResourceBundleMessageSource resourceBundleMessageSource;

    /**
     * default locale.
     *
     * @return locale resolver
     */
    @Bean
    public LocaleResolver localeResolver() {
        SessionLocaleResolver localeResolver = new SessionLocaleResolver();
        localeResolver.setDefaultLocale(Locale.SIMPLIFIED_CHINESE);
        return localeResolver;
    }

    /**
     * local validator factory bean.
     *
     * @return LocalValidatorFactoryBean
     */
    @Bean
    public LocalValidatorFactoryBean localValidatorFactoryBean() {
        LocalValidatorFactoryBean factoryBean = new LocalValidatorFactoryBean();
        MessageInterpolatorFactory interpolatorFactory = new MessageInterpolatorFactory();
        factoryBean.setMessageInterpolator(interpolatorFactory.getObject());
        factoryBean.setValidationMessageSource(resourceBundleMessageSource);
        return factoryBean;
    }

    /**
     * locale change interceptor.
     *
     * @return LocaleChangeInterceptor
     */
    @Bean
    public LocaleChangeInterceptor localeChangeInterceptor() {
        LocaleChangeInterceptor interceptor = new CustomLocaleChangeInterceptor();
        interceptor.setParamName(LANGUAGE_PARAM_NAME);
        return interceptor;
    }

    /**
     * register locale change interceptor.
     *
     * @param registry registry
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localeChangeInterceptor());
    }
}
```

### 校验

- **设置语言是中文**

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-7.png)

查看校验结果

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-6.png)

- **设置语言是英文**

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-8.png)

查看校验结果

![](https://www.pdai.tech/images/spring/springboot/springboot-interface-param-9.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos