# srcdep

[(Here is the English Version)](README.md)

一个简单的基于源代码依赖管理工具

## 设计理念

* 专注于 C/C++ 项目
* 基于源代码，而不是二进制包
* 只解决依赖问题，不涉及构建

## 安装

git clone 本项目到本地，并将其路径设置到 PATH 中。

## 开始使用

1. 复制 SRCDEP.sample.yaml 到您的源代码根目录并重命名为 `SRCDEP.yaml`。

2. 在您源代码根目录运行 `srcdep`

运行结束后，可以看到 thirdparty/zlib_from_git 和 thirdparty/zlib_from_url 被成功下载。

## 可再发行的脚本

根目录下有两个脚本文件 fetch_deps 和 fetch_deps.bat，它们可以被发布到您的代码根目录，帮助没有 srcdep 环境的使用者更加方便地下载依赖包。

## 更多说明

### 命令行参数

请运行 `srcdep --help` 查看。

### SRCDEP.yaml 格式

见 [SRCDEP.yaml](SRCDEP.yaml)。
