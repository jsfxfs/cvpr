# SpringBoot集成文件 - 集成POI-tl之基于模板的Word导出

> 前文我们介绍了通过Apache POI通过来导出word的例子；那如果是word模板方式，有没有开源库通过模板方式导出word呢？poi-tl是一个基于Apache POI的Word模板引擎，也是一个免费开源的Java类库，你可以非常方便的加入到你的项目中，并且拥有着让人喜悦的特性。本文主要介绍通过SpringBoot集成poi-tl实现模板方式的Word导出功能。

## 知识准备

> 需要理解文件上传和下载的常见场景和技术手段。@pdai

### 什么是poi-tl

> 如下内容来源于，[poi-tl官网](http://deepoove.com/poi-tl)。

poi-tl（poi template language）是Word模板引擎，使用Word模板和数据创建很棒的Word文档。

优势：

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-tl-5.png)

它还支持自定义插件，如下是[官网代码仓库](https://github.com/Sayi/poi-tl)支持的特性

> poi-tl supports **custom functions (plug-ins)**, functions can be executed anywhere in the Word template, do anything anywhere in the document is the goal of poi-tl.

| Feature | Description |
| --- | --- |
| ✅ Text | Render the tag as text |
| ✅ Picture | Render the tag as a picture |
| ✅ Table | Render the tag as a table |
| ✅ Numbering | Render the tag as a numbering |
| ✅ Chart | Bar chart (3D bar chart), column chart (3D column chart), area chart (3D area chart), line chart (3D line chart), radar chart, pie chart (3D pie Figure) and other chart rendering |
| ✅ If Condition | Hide or display certain document content (including text, paragraphs, pictures, tables, lists, charts, etc.) according to conditions |
| ✅ Foreach Loop | Loop through certain document content (including text, paragraphs, pictures, tables, lists, charts, etc.) according to the collection |
| ✅ Loop table row | Loop to copy a row of the rendered table |
| ✅ Loop table column | Loop copy and render a column of the table |
| ✅ Loop ordered list | Support the loop of ordered list, and support multi-level list at the same time |
| ✅ Highlight code | Word highlighting of code blocks, supporting 26 languages ​​and hundreds of coloring styles |
| ✅ Markdown | Convert Markdown to a word document |
| ✅ Word attachment | Insert attachment in Word |
| ✅ Word Comments | Complete support comment, create comment, modify comment, etc. |
| ✅ Word SDT | Complete support structured document tag |
| ✅ Textbox | Tag support in text box |
| ✅ Picture replacement | Replace the original picture with another picture |
| ✅ bookmarks, anchors, hyperlinks | Support setting bookmarks, anchors and hyperlinks in documents |
| ✅ Expression Language | Fully supports SpringEL expressions and can extend more expressions: OGNL, MVEL... |
| ✅ Style | The template is the style, and the code can also set the style |
| ✅ Template nesting | The template contains sub-templates, and the sub-templates then contain sub-templates |
| ✅ Merge | Word merge Merge, you can also merge in the specified position |
| ✅ custom functions (plug-ins) | Plug-in design, execute function anywhere in the document |

### poi-tl的TDO模式

> TDO模式：Template + data-model = output

以官网的例子为例：

```java
XWPFTemplate template = XWPFTemplate.compile("template.docx").render(
  new HashMap<String, Object>(){{
    put("title", "Hi, poi-tl Word模板引擎");
}});  
template.writeAndClose(new FileOutputStream("output.docx"));
```

- compile 编译模板 - Template
- render 渲染数据 - data-model
- write 输出到流 - output

#### Template：模板

模板是Docx格式的Word文档，你可以使用Microsoft office、WPS Office、Pages等任何你喜欢的软件制作模板，也可以使用Apache POI代码来生成模板。

所有的标签都是以`{{`开头，以`}}`结尾，标签可以出现在任何位置，包括页眉，页脚，表格内部，文本框等，表格布局可以设计出很多优秀专业的文档，推荐使用表格布局。

poi-tl模板遵循“所见即所得”的设计，模板和标签的样式会被完全保留。

#### Data-model：数据

数据类似于哈希或者字典，可以是Map结构（key是标签名称）：

```java
Map<String, Object> data = new HashMap<>();
data.put("name", "Sayi");
data.put("start_time", "2019-08-04");
```

可以是对象（属性名是标签名称）：

```java
public class Data {
  private String name;
  private String startTime;
  private Author author;
}
```

数据可以是树结构，每级之间用点来分隔开，比如`{ {author.name} }`标签对应的数据是author对象的name属性值。

**Word模板不是由简单的文本表示，所以在渲染图片、表格等元素时提供了数据模型，它们都实现了接口RenderData**，比如图片数据模型PictureRenderData包含图片路径、宽、高三个属性。

#### Output：输出

以流的方式进行输出：

```java
template.write(OutputStream stream);
```

可以写到任意输出流中，比如文件流：

```java
template.write(new FileOutputStream("output.docx"));
```

比如网络流：

```java
response.setContentType("application/octet-stream");
response.setHeader("Content-disposition","attachment;filename=\""+"out_template.docx"+"\"");

// HttpServletResponse response
OutputStream out = response.getOutputStream();
BufferedOutputStream bos = new BufferedOutputStream(out);
template.write(bos);
bos.flush();
out.flush();
PoitlIOUtils.closeQuietlyMulti(template, bos, out); // 最后不要忘记关闭这些流。
```

## 实现案例

> 这里展示SpringBoot集成poi-tl基于word模板导出Word， 以及导出markdown为word的例子。

### Pom依赖

引入poi的依赖包

基础的包：

```xml
<dependency>
    <groupId>com.deepoove</groupId>
    <artifactId>poi-tl</artifactId>
    <version>1.12.0</version>
</dependency>
```

插件的包如下，比如highlight,markdown包

```xml
<dependency>
    <groupId>com.deepoove</groupId>
    <artifactId>poi-tl-plugin-highlight</artifactId>
    <version>1.0.0</version>
</dependency>
<dependency>
    <groupId>com.deepoove</groupId>
    <artifactId>poi-tl-plugin-markdown</artifactId>
    <version>1.0.3</version>
</dependency>
```

### 导出基于template的word

controller中的方法

```java
@ApiOperation("Download Word")
@GetMapping("/word/download")
public void download(HttpServletResponse response) {
    try {
        XWPFTemplate document = userService.generateWordXWPFTemplate();
        response.reset();
        response.setContentType("application/octet-stream");
        response.setHeader("Content-disposition",
                "attachment;filename=user_word_" + System.currentTimeMillis() + ".docx");
        OutputStream os = response.getOutputStream();
        document.write(os);
        os.close();
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

Service中的实际方法

```java
@Override
public XWPFTemplate generateWordXWPFTemplate() throws IOException {
    Map<String, Object> content = new HashMap<>();
    content.put("title", "Java 全栈知识体系");
    content.put("author", "pdai");
    content.put("site", new HyperlinkTextRenderData("", ""));

    content.put("poiText", "Apache POI 是创建和维护操作各种符合Office Open XML（OOXML）标准和微软的OLE 2复合文档格式（OLE2）的Java API。用它可以使用Java读取和创建,修改MS Excel文件.而且,还可以使用Java读取和创建MS Word和MSPowerPoint文件。更多请参考[官方文档](https://poi.apache.org/index.html)");

    content.put("poiText2", "生成xls和xlsx有什么区别？POI对Excel中的对象的封装对应关系？");
    content.put("poiList", Numberings.create("excel03只能打开xls格式，无法直接打开xlsx格式",
            "xls只有65536行、256列; xlsx可以有1048576行、16384列",
            "xls占用空间大, xlsx占用空间小，运算速度也会快一点"));

    RowRenderData headRow = Rows.of("ID", "Name", "Email", "TEL", "Description").textColor("FFFFFF")
            .bgColor("4472C4").center().create();
    TableRenderData table = Tables.create(headRow);
    getUserList()
            .forEach(a -> table.addRow(Rows.create(a.getId() + "", a.getUserName(), a.getEmail(), a.getPhoneNumber() + "", a.getDescription())));
    content.put("poiTable", table);

    Resource resource = new ClassPathResource("pdai-guli.png");
    content.put("poiImage", Pictures.ofStream(new FileInputStream(resource.getFile())).create());

    return XWPFTemplate.compile(new ClassPathResource("poi-tl-template.docx").getFile()).render(content);
}

private List<User> getUserList() {
    List<User> userList = new ArrayList<>();
    for (int i = 0; i < 5; i++) {
        userList.add(User.builder()
                .id(Long.parseLong(i + "")).userName("pdai" + i).email("pdai@pdai.tech" + i).phoneNumber(121231231231L)
                .description("hello world" + i)
                .build());
    }
    return userList;
}
```

准备模板

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-tl-3.png)

导出word

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-tl-1.png)

### 导出markdown为word

controller中的方法

```java
@ApiOperation("Download Word based on markdown")
@GetMapping("/word/downloadMD")
public void downloadMD(HttpServletResponse response) {
    try {
        XWPFTemplate document = userService.generateWordXWPFTemplateMD();
        response.reset();
        response.setContentType("application/octet-stream");
        response.setHeader("Content-disposition",
                "attachment;filename=user_word_" + System.currentTimeMillis() + ".docx");
        OutputStream os = response.getOutputStream();
        document.write(os);
        os.close();
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

Service中实现的方法

```java
@Override
public XWPFTemplate generateWordXWPFTemplateMD() throws IOException {
    MarkdownRenderData code = new MarkdownRenderData();

    Resource resource = new ClassPathResource("test.md");
    code.setMarkdown(new String(Files.readAllBytes(resource.getFile().toPath())));
    code.setStyle(MarkdownStyle.newStyle());

    Map<String, Object> data = new HashMap<>();
    data.put("md", code);

    Configure config = Configure.builder().bind("md", new MarkdownRenderPolicy()).build();

    return XWPFTemplate.compile(new ClassPathResource("markdown_template.docx").getFile(), config).render(data);
}
```

准备模板

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-tl-4.png)

导出word

![](https://www.pdai.tech/images/spring/springboot/springboot-file-word-poi-tl-2.png)

## 示例源码

https://github.com/realpdai/tech-pdai-spring-demos

## 参考文章

http://deepoove.com/poi-tl/