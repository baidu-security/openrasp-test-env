# 自动化测试
## agent端测试
### 通用模块
覆盖不同版本通用测试: 包括 
- __通用配置项(P0)__
- __插件逻辑(P0)__
- __云端交互(P0)__
- __常见开源WEB应用覆盖(P0)__
- __BUG回归(P0)__
- 极端情况模拟(P1)

#### 通用配置项
以下列表为OpenRASP通用配置项,需逐项验证

配置名 | 含义 | 是否已支持
---|---|---
plugin.timeout.millis | 对于单次HOOK点检测，JS插件整体超时时间（毫秒），默认100 |
plugin.maxstack | 插件获取堆栈的最大深度，默认100 |
plugin.filter | 文件存在验证开关，切换至扫描器模式，默认false |
log.maxburst | 每个进程/线程每秒钟最大日志条数，默认100 | 
log.maxstack | 报警日志记录的最大堆栈深度，默认10 |
log.maxbackup | 日志最大备份天数(仅云控生效) |
syslog.tag | 用于 syslog 的 tag，默认OpenRASP |
syslog.url | syslog server url |
syslog.facility | 用于 syslog 的 facility，默认1 |
syslog.enable | 报警是否开启 syslog，默认false | 
syslog.connection_timeout | syslog连接超时时间(毫秒)，默认50 |
syslog.read_timeout | syslog读超时时间(毫秒)，默认10 |
syslog.reconnect_interval | syslog重连时间间隔(秒)，默认300 |
block.status_code | 拦截攻击后，将状态码设置为这个值 |
block.redirect_url | 拦截攻击后，跳转到这个URL，并根据模板设置 request_id 参数 |
block.content_json | 拦截攻击后，若期望响应类型为JSON，则根据此模板显示内容 |
block.content_xml | 拦截攻击后，若期望响应类型为XML，则根据此模板显示内容 |
block.content_html | 拦截攻击后，若期望响应类型不为JSON/XML，则根据此模板显示内容 |
inject.urlprefix | 对于以下URL，修改响应并注入HTML | 
body.maxbytes | 最多读取body的前多少字节，默认4 x 1024 (4KB) | 
clientip.header | XFF header name | 
security.enforce_policy | 当服务器不满足安全配置规范，是否拦截，sql连接 |
lru.max_size | LRU最大容量 |
webshell_callable.blacklist | callable回调函数名黑名单 |
hook.white | url-checktype 白名单 | 
ognl.expression.minlength | ognl表达式最小长度(Java) |
xss.filter_regex | 用户输入标签匹配正则表达式 |
xss.min_param_length | 最小出发检测参数长度,默认15 |
xss.max_detection_num | 最多检测参数数目,默认10 |

#### 插件更新
需要覆盖如下四个部分,需要云端协同完成测试:
- [ ] 注册
- [ ] 插件更新
- [ ] 配置更新
- [ ] 日志推送

#### 常见开源WEB应用覆盖
具体列表参考专有测试

#### BUG回归
对于发行版,整理发现BUG列表.
须复现回归,确保后续版本不会重复出现!

#### 极端情况模拟
模拟可能出现的极端情况

#### 云端交互
验证云端插件以及配置更新是否生效

### 专有模块
不同语言版本特有的检测项

#### PHP版本
##### 系统兼容
PHP版本支持linux,macOS
- [ ] ubuntu14
- [ ] ubuntu16
- [ ] ubuntu18
- [ ] centos6
- [ ] centos7
- [ ] macOS

##### 语言版本兼容
需要覆盖PHP5/7两个大版本

- [ ] 5.3
- [ ] 5.4
- [ ] 5.5
- [ ] 5.6
- [ ] 7.0
- [ ] 7.1
- [ ] 7.2
- [ ] 7.3

##### 宿主PHP是否开启ZTS支持

- [ ] ZTS
- [ ] non-ZTS

##### SAPI支持

- [ ] cli-server
- [ ] fpm-cgi
- [ ] apache2handler
- [ ] cgi

##### 运行模式

- [ ] 单机版
- [ ] 云控版

##### ini配置项

配置名 | 含义 | 是否已支持
---|---|---
openrasp.root_dir | openrasp 根目录，存放插件、日志 |
openrasp.locale | 配置的语言类型 |
openrasp.heartbeat_interval | 心跳间隔，单位秒,moren |
openrasp.backend_url | 后台url |
openrasp.app_id | app_id，后台生成 |
openrasp.app_secret | app_secret，后台生成 |
openrasp.remote_management_enable | 云控开关 |

##### HOOK完整性
下表为PHP攻击检测完整HOOK列表,该项可通过make test完成:

|HOOK类型 | 方法名称  | 是否已支持 |
|-----|---------|---------|
|webshell callable | array_walk ||
| | array_map    ||
| | array_filter ||
| | ReflectionFunction::\_\_construct ||
|命令执行(含webshell) | passthru   ||
| | system     ||
| | exec       ||
| | shell_exec ||
| | proc_open  ||
| | popen      ||
| | pcntl_exec ||
|目录遍历 | dir ||
| | scandir ||
| | opendir ||
|XSS(echo) | echo ||
|文件读取  | file              ||
| | readfile          ||
| | file_get_contents ||
| | fopen             ||
| | SplFileObject::\_\_construct ||
|文件写入 | file_put_contents ||
| | fopen ||
| | SplFileObject::\_\_construct ||
|文件拷贝 | copy ||
|文件移动 | rename ||
|文件上传 | move_uploaded_file ||
|文件包含 | include ||
|文件运行(webshell) | eval ||
|| assert(仅PHP5) ||
|SQL注入or异常 | mysql_query(仅PHP5) ||
| | mysqli_query ||
| | mysqli::query ||
| | mysqli_real_query ||
| | mysqli::real_query ||
| | mysqli_prepare ||
| | mysqli::prepare ||
| | PDO::query ||
| | PDO::exec ||
| | PDO::prepare ||
| | pg_query ||
| | pg_send_query ||
| | pg_prepare ||
| | SQLite3::query ||
| | SQLite3::exec ||
| | SQLite3::querySingle ||
|SSRF | curl_exec ||

##### 基线检测完整性

| 检查内容 | 方法名称  | 是否已支持 |
|-----|---------|---------|
|数据库连接账号 | mysql_connect(仅PHP5) ||
|| mysql_pconnect(仅PHP5) ||
|| mysqli::\_\_construct ||
|| mysqli::connect ||
|| mysqli_connect ||
|| mysqli::real_connect ||
|| mysqli_real_connect ||
|| PDO::\_\_construct ||
|| pg_connect ||
|| pg_pconnect ||
|ini检测 | allow_url_include ||
|| expose_php ||
|| display_errors ||
|| yaml.decode_php ||

##### 常见开源WEB应用
- [ ] discuz
- [ ] wordpress
- [ ] phpcms


#### Java版本
待补充
## 云端测试
待补充