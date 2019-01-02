# OpenRasp Cloud 自动化测试环境

### 使用方法

1. 使用`docker-compose up`命令启动环境

2. 使用`docker-compose exec tester /bin/bash`进入测试docker，进入`/root/test-script/`目录
3. 执行`python init.py`初始化环境
4. 执行python unit_test.py进行自动化测试

### 注意事项

- LRU影响测试

  sql类和ssrf类检测（目前）使用了LRU，会影响测试插件更新的测试结果，不宜选做测试用例

