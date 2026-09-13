# ▶SpringBoot接口 - 如何统一接口封装

> 在以SpringBoot开发Restful接口时，统一返回方便前端进行开发和封装，以及出现时给出响应编码和信息。@pdai

## RESTful API接口?

- **什么是 REST**？

Representational State Transfer，翻译是“表现层状态转化”。可以总结为一句话：**REST 是所有 Web 应用都应该遵守的架构设计指导原则**。

面向资源是 REST 最明显的特征，对于同一个资源的一组不同的操作。资源是服务器上一个可命名的抽象概念，资源是以名词为核心来组织的，首先关注的是名词。REST 要求，必须通过统一的接口来对资源执行各种操作。对于每个资源只能执行一组有限的操作。

- **什么是 RESTful API**？

**符合 REST 设计标准的 API**，即 RESTful API。REST 架构设计，遵循的各项标准和准则，就是 HTTP 协议的表现，换句话说，HTTP 协议就是属于 REST 架构的设计模式。比如，无状态，请求-响应。

Restful相关文档可以参考 <https://restfulapi.net/>

## 为什么要统一封装接口

> 现在大多数项目采用前后分离的模式进行开发，统一返回方便前端进行开发和封装，以及出现时给出响应编码和信息。

以查询某个用户接口而言，如果没有封装, 返回结果如下

```json
{
  "userId": 1,
  "userName": "赵一"
}
```

如果封装了，返回正常的结果如下：

```json
{
  "timestamp": 11111111111,
  "status": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "userName": "赵一"
  }
}
```

异常返回结果如下：

```json
{
  "timestamp": 11111111111,
  "status": 10001,
  "message": "User not exist",
  "data": null
}
```

## 实现案例

> 如何实现上面的封装呢？

### 状态码封装

这里以常见的状态码为例，包含responseCode 和 description两个属性。

如果还有其它业务状态码，也可以放到这个类中。

```java
/**
 * @author pdai
 */
@Getter
@AllArgsConstructor
public enum ResponseStatus {

    SUCCESS("200", "success"),
    FAIL("500", "failed"),

    HTTP_STATUS_200("200", "ok"),
    HTTP_STATUS_400("400", "request error"),
    HTTP_STATUS_401("401", "no authentication"),
    HTTP_STATUS_403("403", "no authorities"),
    HTTP_STATUS_500("500", "server error");

    public static final List<ResponseStatus> HTTP_STATUS_ALL = Collections.unmodifiableList(
            Arrays.asList(HTTP_STATUS_200, HTTP_STATUS_400, HTTP_STATUS_401, HTTP_STATUS_403, HTTP_STATUS_500
            ));

    /**
     * response code
     */
    private final String responseCode;

    /**
     * description.
     */
    private final String description;

}
```

### 返回内容封装

包含公共的接口返回时间，状态status, 消息message， 以及数据data。

考虑到数据的序列化（比如在网络上传输），这里data有时候还会extends Serializable。

```java
@Data
@Builder
public class ResponseResult<T> {

    /**
     * response timestamp.
     */
    private long timestamp;

    /**
     * response code, 200 -> OK.
     */
    private String status;

    /**
     * response message.
     */
    private String message;

    /**
     * response data.
     */
    private T data;

    /**
     * response success result wrapper.
     *
     * @param <T> type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> success() {
        return success(null);
    }

    /**
     * response success result wrapper.
     *
     * @param data response data
     * @param <T>  type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> success(T data) {
        return ResponseResult.<T>builder().data(data)
                .message(ResponseStatus.SUCCESS.getDescription())
                .status(ResponseStatus.SUCCESS.getResponseCode())
                .timestamp(System.currentTimeMillis())
                .build();
    }

    /**
     * response error result wrapper.
     *
     * @param message error message
     * @param <T>     type of data class
     * @return response result
     */
    public static <T extends Serializable> ResponseResult<T> fail(String message) {
        return fail(null, message);
    }

    /**
     * response error result wrapper.
     *
     * @param data    response data
     * @param message error message
     * @param <T>     type of data class
     * @return response result
     */
    public static <T> ResponseResult<T> fail(T data, String message) {
        return ResponseResult.<T>builder().data(data)
                .message(message)
                .status(ResponseStatus.FAIL.getResponseCode())
                .timestamp(System.currentTimeMillis())
                .build();
    }

}
```

### 接口返回时调用

在接口返回时调用, 以用户接口为例

```java
/**
 * @author pdai
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private IUserService userService;

    /**
     * @param user user param
     * @return user
     */
    @ApiOperation("Add/Edit User")
    @PostMapping("add")
    public ResponseResult<User> add(User user) {
        if (user.getId()==null || !userService.exists(user.getId())) {
            user.setCreateTime(LocalDateTime.now());
            user.setUpdateTime(LocalDateTime.now());
            userService.save(user);
        } else {
            user.setUpdateTime(LocalDateTime.now());
            userService.update(user);
        }
        return ResponseResult.success(userService.find(user.getId()));
    }


    /**
     * @return user list
     */
    @ApiOperation("Query User One")
    @GetMapping("edit/{userId}")
    public ResponseResult<User> edit(@PathVariable("userId") Long userId) {
        return ResponseResult.success(userService.find(userId));
    }
}
```

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos