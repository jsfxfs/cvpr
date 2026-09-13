## AOP的实现？

> 我们通过设计的例子来引出动态代理，进而引出Spring AOP基于动态代理的织入，以及AspectJ基于静态代理的织入。

### 初步思路：动态代理

> 我们这里设计一个案例：如果我们需要将某个方法执行的前后都加上记录日志的功能，比如UserService的所有方法执行都会记录日志。

- **为什么基于OOP（比如继承）没法解决这种需求**？

我们看下，常见的钩子方式

```java
public void execMethod() {
   beforeMethod();

   exec();

   afterMethod();
}

abstract void exec();

private void beforeMethod() {
   System.out.println("before method");
}
private void afterMethod() {
   System.out.println("after method");
}
```

显然你可以看到，OOP/钩子模式关注类和方法层次的结构，而对于动态的切面行为，是无法做到扩展和解耦的。

- **紧接着，我们想到了动态代理**

我们通过设计UserService的例子：

User

```java
package tech.pdai.springframework.entity;

/**
 * @author pdai
 */
public class User {

    /**
     * user's name.
     */
    private String name;

    /**
     * user's age.
     */
    private int age;

    /**
     * init.
     *
     * @param name name
     * @param age  age
     */
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```

IUserService

```java
package tech.pdai.springframework.service;

import tech.pdai.springframework.entity.User;

import java.util.List;

/**
 * @author pdai
 */
public interface IUserService {

    /**
     * find user list.
     *
     * @return user list
     */
    List<User> findUserList();

    /**
     * add user
     */
    void addUser();
}
```

UserServiceImpl

```java
package tech.pdai.springframework.service;

import tech.pdai.springframework.entity.User;

import java.util.Collections;
import java.util.List;

/**
 * @author pdai
 */
public class UserServiceImpl implements IUserService {

    /**
     * find user list.
     *
     * @return user list
     */
    @Override
    public List<User> findUserList() {
        return Collections.singletonList(new User("pdai", 18));
    }

    /**
     * add user
     */
    @Override
    public void addUser() {
        // do something
    }

}
```

我们通过JDK动态代理，来对Target类（这里是IUserService)的方法进行拦截。

```java
package tech.pdai.springframework.proxy;

import tech.pdai.springframework.service.IUserService;
import tech.pdai.springframework.service.UserServiceImpl;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.util.Arrays;

/**
 * This class is for proxy demo.
 *
 * @author pdai
 */
public class UserLogProxy {

    /**
     * proxy target
     */
    private IUserService target;

    /**
     * init.
     *
     * @param target target
     */
    public UserLogProxy(UserServiceImpl target) {
        super();
        this.target = target;
    }

    /**
     * get proxy.
     *
     * @return proxy target
     */
    public IUserService getLoggingProxy() {
        IUserService proxy;
        ClassLoader loader = target.getClass().getClassLoader();
        Class[] interfaces = new Class[]{IUserService.class};
        InvocationHandler h = new InvocationHandler() {
            /**
             * proxy: 代理对象。 一般不使用该对象 method: 正在被调用的方法 args: 调用方法传入的参数
             */
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                String methodName = method.getName();
                // log - before method
                System.out.println("[before] execute method: " + methodName);

                // call method
                Object result = null;
                try {
                    // 前置通知
                    result = method.invoke(target, args);
                    // 返回通知, 可以访问到方法的返回值
                } catch (NullPointerException e) {
                    e.printStackTrace();
                    // 异常通知, 可以访问到方法出现的异常
                }
                // 后置通知. 因为方法可以能会出异常, 所以访问不到方法的返回值

                // log - after method
                System.out.println("[after] execute method: " + methodName + ", return value: " + result);
                return result;
            }
        };
        /**
         * loader: 代理对象使用的类加载器.
         * interfaces: 指定代理对象的类型. 即代理代理对象中可以有哪些方法.
         * h: 当具体调用代理对象的方法时, 应该如何进行响应, 实际上就是调用 InvocationHandler 的 invoke 方法
         */
        proxy = (IUserService) Proxy.newProxyInstance(loader, interfaces, h);
        return proxy;
    }

}
```

测试

```java
import tech.pdai.springframework.proxy.UserLogProxy;
import tech.pdai.springframework.service.IUserService;
import tech.pdai.springframework.service.UserServiceImpl;

/**
 * This class is for proxy demo interface.
 *
 * @author pdai
 */
public class ProxyDemo {

    /**
     * main interface.
     *
     * @param args args
     */
    public static void main(String[] args) {
        // proxy
        IUserService userService = new UserLogProxy(new UserServiceImpl()).getLoggingProxy();

        // call methods
        userService.findUserList();
        userService.addUser();
    }
}
```

测试结果

![](https://www.pdai.tech/images/spring/springframework/spring-framework-aop-1.png)

- **其二, 我们想到了还通过注解的方式编译时织入**

为什么会想到这种方式呢？如果你清楚Lombok, 以及 MapStruct等工具原理，你就会理解可以通过注解方式实现编译时将代码逻辑织入的。你可以通过如下的文章回顾相关知识：

1. [Java 基础 - 注解机制详解](../java/basic/java-basic-x-annotation.md)
2. [常用开发库 - Lombok工具库详解](../develop/package/dev-package-x-lombok.md)
3. [常用开发库 - MapStruct工具库详解](../develop/package/dev-package-x-mapstruct.md)

通过上述的例子和思路，基本能够帮助你铺垫理解AOP实现原理的主要思路，在此基础上我们将进一步去理解。

### Spring AOP的实现思路

### AspectJ的实现思路