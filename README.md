## 使用方法

命令行键入下列命令之后，程序将会运行并抓取目标用户发布微博，并以csv形式输入结构化数据

```shell
# 微博模块测试
python main.py --type weibo --user-id 2714280233
python main.py --type weibo --user-id 1792634467
```

```shell
# 豆瓣模块测试
python main.py --type douban --entry-id 35209731 --st 1 --ed 20
python main.py --type douban --entry-id 35209733 --st 1 --ed 20
```



爬取之后再对结构化的数据进行可视化