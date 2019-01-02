const version = '2018-1025-0001'

/*
 * Copyright 2017-2018 Baidu Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// 常用链接
//
// Web 攻击检测能力说明、零规则检测算法介绍
// https://rasp.baidu.com/doc/usage/web.html
//
// CVE 漏洞覆盖说明
// https://rasp.baidu.com/doc/usage/cve.html

'use strict'
var plugin  = new RASP('offical')

// 检测逻辑开关
//
// block  -> 拦截，并打印报警日志
// log    -> 打印日志，不拦截
// ignore -> 关闭这个算法

// BEGIN ALGORITHM CONFIG //

var algorithmConfig = {
    // SQL注入算法#1 - 匹配用户输入
    // 1. 用户输入长度至少 15
    // 2. 用户输入至少包含一个SQL关键词 - 即 pre_filter，默认关闭
    // 3. 用户输入完整的出现在SQL语句中，且会导致SQL语句逻辑发生变化
    sqli_userinput: {
        action:     'ignore',
        min_length: 15,
        pre_filter: 'select|file|from|;',
        pre_enable: false,
    },
    // SQL注入算法#2 - 语句规范
    sqli_policy: {
        action:  'ignore',

        // 粗规则 - 为了减少 tokenize 次数，当SQL语句包含一定特征时才进入
        // 另外，我们只需要处理增删改查的语句，虽然 show 语句也可以报错注入，但是算法2没必要处理
        pre_filter: '^(select|insert|update|delete).*(;|\\/\\*|(?:\\d{1,2},){4}|(?:null,){4}|0x[\\da-f]{8}|\\b(information_schema|outfile|dumpfile|load_file|benchmark|pg_sleep|sleep|is_srvrolemember|updatexml|extractvalue|hex|char|chr|mid|ord|ascii|bin))\\b',

        feature: {
            // 是否禁止多语句执行，select ...; update ...;
            stacked_query:      true,

            // 是否禁止16进制字符串，select 0x41424344
            no_hex:             true,

            // 禁止版本号注释，select/*!500001,2,*/3
            version_comment:    true,

            // 函数黑名单，具体列表见下方，select load_file(...)
            function_blacklist: true,

            // 拦截 union select NULL,NULL 或者 union select 1,2,3,4
            union_null:         true,

            // 是否拦截 into outfile 写文件操作
            into_outfile:       true,

            // 是否拦截 information_schema 相关读取操作，默认关闭
            information_schema: false
        },
        function_blacklist: {
            // 文件操作
            load_file:        true,

            // 时间差注入
            benchmark:        true,
            sleep:            true,
            pg_sleep:         true,

            // 探测阶段
            is_srvrolemember: true,

            // 报错注入
            updatexml:        true,
            extractvalue:     true,

            // 盲注函数，如有误报可删掉一些函数
            hex:              true,
            char:             true,
            chr:              true,
            mid:              true,
            ord:              true,
            ascii:            true,
            bin:              true
        }
    },
    // SSRF - 来自用户输入，且为内网地址就拦截
    ssrf_userinput: {
        action: 'ignore'
    },
    // SSRF - 是否允许访问 aws metadata
    ssrf_aws: {
        action: 'ignore'
    },
    // SSRF - 是否允许访问 dnslog 地址
    ssrf_common: {
        action:  'ignore',
        domains: [
            '.ceye.io',
            '.vcap.me',
            '.xip.name',
            '.xip.io',
            '.nip.io',
            '.burpcollaborator.net',
            '.tu4.org'
        ]
    },
    // SSRF - 是否允许访问混淆后的IP地址
    ssrf_obfuscate: {
        action: 'ignore'
    },
    // SSRF - 禁止使用 curl 读取 file:///etc/passwd、php://filter/XXXX 这样的内容
    ssrf_protocol: {
        action: 'ignore',
        protocols: [
            'file',
            'gopher',

            // java specific
            'jar',
            'netdoc',

            // php specific
            'dict',
            'php',
            'phar',
            'compress.zlib',
            'compress.bzip2'
        ]
    },

    // 任意文件下载防护 - 来自用户输入
    readFile_userinput: {
        action: 'ignore'
    },
    // 任意文件下载防护 - 使用 file_get_contents 等函数读取 http(s):// 内容（注意，这里不区分是否为内网地址）
    readFile_userinput_http: {
        action: 'ignore'
    },
    // 任意文件下载防护 - 使用 file_get_contents 等函数读取 file://、php:// 协议
    readFile_userinput_unwanted: {
        action: 'ignore'
    },
    // 任意文件下载防护 - 使用 ../../ 跳出 web 目录读取敏感文件
    readFile_outsideWebroot: {
        action: 'ignore'
    },
    // 任意文件下载防护 - 读取敏感文件，最后一道防线
    readFile_unwanted: {
        action: 'ignore'
    },

    // 写文件操作 - NTFS 流
    writeFile_NTFS: {
        action: 'ignore'
    },
    // 写文件操作 - PUT 上传脚本文件
    writeFile_PUT_script: {
        action: 'ignore'
    },
    // 写文件操作 - 脚本文件
    // https://rasp.baidu.com/doc/dev/official.html#case-file-write
    writeFile_script: {
        action: 'ignore'
    },

    // 重命名监控 - 将普通文件重命名为webshell，
    // 案例有 MOVE 方式上传后门、CVE-2018-9134 dedecms v5.7 后台重命名 getshell
    rename_webshell: {
        action: 'ignore'
    },
    // copy_webshell: {
    //     action: 'ignore'
    // },

    // 文件管理器 - 反射方式列目录
    directory_reflect: {
        action: 'ignore'
    },
    // 文件管理器 - 查看敏感目录
    directory_unwanted: {
        action: 'ignore'
    },
    // 文件管理器 - 用户输入匹配，仅当直接读取绝对路径时才检测
    directory_userinput: {
        action: 'ignore'
    },

    // 文件包含 - 用户输入匹配
    include_userinput: {
        action: 'ignore'
    },
    // 文件包含 - 特殊协议
    include_protocol: {
        action: 'ignore',
        protocols: [
            'file',
            'gopher',

            // java specific
            'jar',
            'netdoc',

            // php stream
            'http',
            'https',

            // php specific
            'dict',
            'php',
            'phar',
            'compress.zlib',
            'compress.bzip2'
        ]
    },

    // XXE - 使用 gopher/ftp/dict/.. 等不常见协议访问外部实体
    xxe_protocol: {
        action: 'ignore',
        protocols: [
            'ftp',
            'dict',
            'gopher',
            'jar',
            'netdoc'
        ]
    },
    // XXE - 使用 file 协议读取内容，可能误报，默认 log
    xxe_file: {
        action: 'log',
    },

    // 文件上传 - COPY/MOVE 方式，仅适合 tomcat
    fileUpload_webdav: {
        action: 'ignore'
    },
    // 文件上传 - Multipart 方式上传脚本文件
    fileUpload_multipart_script: {
        action: 'ignore'
    },
    // 文件上传 - Multipart 方式上传 HTML/JS 等文件
    fileUpload_multipart_html: {
        action: 'ignore'
    },

    // OGNL 代码执行漏洞
    ognl_exec: {
        action: 'ignore'
    },

    // 命令执行 - java 反射、反序列化，php eval 等方式
    command_reflect: {
        action: 'ignore'
    },
    // 命令注入 - 命令执行后门，或者命令注入
    command_userinput: {
        action:     'ignore',
        min_length: 8
    },
    // 命令执行 - 是否拦截所有命令执行？如果没有执行命令的需求，可以改为 block，最大程度的保证服务器安全
    command_other: {
        action: 'log'
    },

    // transformer 反序列化攻击
    transformer_deser: {
        action: 'block'
    }
}

// END ALGORITHM CONFIG //

// 将所有拦截开关设置为 log
// Object.keys(algorithmConfig).forEach(function (name) {
//     algorithmConfig[name].action = 'log'
// })

const clean = {
    action:     'ignore',
    message:    'Looks fine to me',
    confidence: 0
}

var forcefulBrowsing = {
    dotFiles: /\.(7z|tar|gz|bz2|xz|rar|zip|sql|db|sqlite)$/,
    nonUserDirectory: /^\/(proc|sys|root)/,

    // webdav 文件探针 - 最常被下载的文件
    unwantedFilenames: [
        // user files
        '.DS_Store',
        'id_rsa', 'id_rsa.pub', 'known_hosts', 'authorized_keys',
        '.bash_history', '.csh_history', '.zsh_history', '.mysql_history',

        // project files
        '.htaccess', '.user.ini',

        'web.config', 'web.xml', 'build.property.xml', 'bower.json',
        'Gemfile', 'Gemfile.lock',
        '.gitignore',
        'error_log', 'error.log', 'nohup.out',
    ],

    // 目录探针 - webshell 查看频次最高的目录
    unwantedDirectory: [
        '/',
        '/home',
        '/var/log',
        '/private/var/log',
        '/proc',
        '/sys',
        'C:\\',
        'D:\\',
        'E:\\'
    ],

    // 文件探针 - webshell 查看频次最高的文件
    absolutePaths: [
        '/etc/shadow',
        '/etc/passwd',
        '/etc/hosts',
        '/etc/apache2/apache2.conf',
        '/root/.bash_history',
        '/root/.bash_profile',
        'c:\\windows\\system32\\inetsrv\\metabase.xml',
        'c:\\windows\\system32\\drivers\\etc\\hosts'
    ]
}

// 如果你配置了非常规的扩展名映射，比如让 .abc 当做PHP脚本执行，那你可能需要增加更多扩展名
var scriptFileRegex = /\.(aspx?|jspx?|php[345]?|phtml)\.?$/i

// 正常文件
var cleanFileRegex = /\.(jpg|jpeg|png|gif|bmp|txt|rar|zip)$/i

// 匹配 HTML/JS 等可以用于钓鱼、domain-fronting 的文件
var htmlFileRegex   = /\.(htm|html|js)$/i

// 其他的 stream 都没啥用
var ntfsRegex       = /::\$(DATA|INDEX)$/i

// SQL注入算法1 - 预过滤正则
var sqliPrefilter1  = new RegExp(algorithmConfig.sqli_userinput.pre_filter)

// SQL注入算法2 - 预过滤正则
var sqliPrefilter2  = new RegExp(algorithmConfig.sqli_policy.pre_filter)

// 常用函数
String.prototype.replaceAll = function(token, tokenValue) {
    // 空值判断，防止死循环
    if (! token || token.length == 0) {
        return this
    }

    var index  = 0;
    var string = this;

    do {
        string = string.replace(token, tokenValue);
    } while((index = string.indexOf(token, index + 1)) > -1);

    return string
}

// function canonicalPath (path) {
//     return path.replaceAll('/./', '/').replaceAll('//', '/').replaceAll('//', '/')
// }

// 我们不再需要简化路径，当出现两个 /../ 或者两个 \..\ 就可以判定为路径遍历攻击了，e.g
// /./././././home/../../../../etc/passwd
// \\..\\..\\..
// \/..\/..\/..
function has_traversal (path) {

    // 左右斜杠，一视同仁
    var path2 = path.replaceAll('\\', '/')

    // 覆盖 ../../
    // 以及 /../../
    var left  = path2.indexOf('../')
    var right = path2.lastIndexOf('/../')

    if (left != -1 && right != -1 && left != right)
    {
        return true
    }

    return false
}

function is_hostname_dnslog(hostname) {
    var domains = algorithmConfig.ssrf_common.domains

    if (hostname == 'requestb.in' || hostname == 'transfer.sh')
    {
        return true
    }

    for (var i = 0; i < domains.length; i ++)
    {
        if (hostname.endsWith(domains[i]))
        {
            return true
        }
    }

    return false
}

function basename (path) {
    // 简单处理，同时支持 windows/linux
    var path2 = path.replaceAll('\\', '/')
    var idx   = path2.lastIndexOf('/')

    return path.substr(idx + 1)
}

function validate_stack_php(stacks) {
    var verdict = false

    for (var i = 0; i < stacks.length; i ++) {
        var stack = stacks[i]

        // 来自 eval/assert/create_function/...
        if (stack.indexOf('eval()\'d code') != -1
            || stack.indexOf('runtime-created function') != -1
            || stack.indexOf('assert code@') != -1
            || stack.indexOf('regexp code@') != -1) {
            verdict = true
            break
        }

        // call_user_func/call_user_func_array 两个函数调用很频繁
        // 必须是 call_user_func 直接调用 system/exec 等函数才拦截，否则会有很多误报
        if (stack.indexOf('@call_user_func') != -1) {
            if (i <= 1) {
                verdict = true
                break
            }
        }
    }

    return verdict
}

function has_file_extension(path) {
    var filename = basename(path)
    var index    = filename.indexOf('.')

    if (index > 0 && index != filename.length - 1) {
        return true
    }

    return false
}

function is_absolute_path(path, is_windows) {

    // Windows - C:\\windows
    if (is_windows) {

        if (path[1] == ':')
        {
            var drive = path[0].toLowerCase()
            if (drive >= 'a' && drive <= 'z')
            {
                return true
            }
        }
    }

    // Unices - /root/
    return path[0] === '/'
}

function is_outside_webroot(appBasePath, realpath, path) {
    var verdict = false

    // servlet 3.X 之后可能会获取不到 appBasePath，或者为空
    // 提前加个判断，防止因为bug导致误报
    if (! appBasePath || appBasePath.length == 0) {
        verdict = false
    }
    else if (realpath.indexOf(appBasePath) == -1 && has_traversal(path)) {
        verdict = true
    }

    return verdict
}

// 路径是否来自用户输入
// file_get_contents("/etc/passwd");
// file_get_contents("../../../../../../../etc/passwd");
//
// 或者以用户输入结尾
// file_get_contents("/data/uploads/" . "../../../../../../../etc/passwd");
function is_path_endswith_userinput(parameter, target, realpath, is_windows)
{
    var verdict = false

    Object.keys(parameter).some(function (key) {
        // 只处理非数组、hash情况
        var value = parameter[key]
            value = value[0]

        // 只处理字符串类型的
        if (typeof value != 'string') {
            return
        }

        // 如果应用做了特殊处理， 比如传入 file:///etc/passwd，实际看到的是 /etc/passwd
        if (value.startsWith('file://') && 
            is_absolute_path(target, is_windows) && 
            value.endsWith(target)) 
        {
            verdict = true
            return true
        }

        // Windows 下面
        // 传入 ../../../conf/tomcat-users.xml
        // 看到 c:\tomcat\webapps\root\..\..\conf\tomcat-users.xml
        if (is_windows){
            value = value.replaceAll('/', '\\')
        }
        
        // 参数必须有跳出目录，或者是绝对路径
        if ((value == target || target.endsWith(value))
            && (has_traversal(value) || value == realpath))
        {
            verdict = true
            return true
        }
    })

    return verdict
}

// 是否来自用户输入 - 适合任意类型参数
function is_from_userinput(parameter, target)
{
    var verdict = false

    Object.keys(parameter).some(function (key) {
        var value = parameter[key]

        // 只处理非数组、hash情况
        if (value[0] == target) {
            verdict = true
            return true
        }
    })
    return verdict
}

// 检查SQL逻辑是否被用户参数所修改
function is_token_changed(raw_tokens, userinput_idx, userinput_length, distance) 
{
    // 当用户输入穿越了多个token，就可以判定为代码注入，默认为2
    var start = -1, end = raw_tokens.length, distance = distance || 2

    // 寻找 token 起始点，可以改为二分查找
    for (var i = 0; i < raw_tokens.length; i++)
    {
        if (raw_tokens[i].stop >= userinput_idx)
        {
            start = i
            break
        }
    }

    // 寻找 token 结束点
    // 另外，最多需要遍历 distance 个 token
    for (var i = start; i < start + distance && i < raw_tokens.length; i++)
    {
        if (raw_tokens[i].stop >= userinput_idx + userinput_length - 1)
        {
            end = i
            break
        }
    }

    if (end - start > distance) {
        return true
    }
    return false
}

// 下个版本将会支持翻译，目前还需要暴露一个 getText 接口给插件
function _(message, args) 
{
    args = args || []

    for (var i = 0; i < args.length; i ++) 
    {
        var symbol = '%' + (i + 1) + '%'
        message = message.replace(symbol, args[i])
    }

    return message
}

// 开始


plugin.log('OpenRASP nouse plugin: Initialized, version', version)

