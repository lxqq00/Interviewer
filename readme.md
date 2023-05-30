

这是一个爬虫，用于手动从各种网站上爬取面试题。
该项目英文名为“Interviewer”，意为“面试官”，意为“面试官的面试题”，也可以理解为“面试官的面试题库”。
其底层是用selenium实现的，所以可以爬取各种网站上的面试题，包括但不限于：
- [x] [牛客网](https://www.nowcoder.com/)


## 使用方法
1. 执行脚本的主机需要安装有chrome浏览器和相应驱动，需要部署有python解释器环境
2. 是启动脚本前，需要先更新python脚本中的chrome安装目录，运行脚本时会基于这个目录启动浏览器。
3. 执行项目根目录下的run.bat脚本（windows主机系统），即启动了一个浏览器程序。
4. 之后在浏览器中先访问一个种子页面（类似于爬虫的爬取的根页面），再手动搜索点击根页面中的链接跳转到新页面，等到浏览器切换到需要采集的页面之后，在脚本的控制台中输入"q"（quit）关闭当前页面、"s"（save）将页面的内容保存、"u"（unsave）将最后一个保存的页面取消保存、"n"(new)将最后一个取消保存的页面并根据url重新在浏览器中访问（由于是仅url，可能会有一些查询不能正确复现）
5. 如果新打开的浏览器标签页是已经采集过的页面（通过url判断），就会自动把新页面关闭
6. 最后会将保存的页面的url、页面中的主体文字序列化到文件中

