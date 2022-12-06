# srcdep

[（中文版本见这里）](README_zh.md)

A simple, source code based dependency management tool.

## Design principle

* Focus on C/C++ projects
* Based on source code, instead of binaries
* Only solving dependency problems, building problems are not considered

## Install

git clone this project to a local directory, and set it into PATH variable.

## Getting Start

1. Write a `SRCDEP.yaml` file at the root directory of your target project, with content as following:

```yaml
DEPS:
  thirdparty/gn_toolchain:
    GIT_REPO: https://github.com/Streamlet/gn_toolchain.git
    GIT_TAG: master
```

2. Run `srcdep` at the root directory of your project.

Then, gn_toolchain, as a dependency, will be downloaded to thirdparty/gn_toolchain.

## More Documents

### Command Line

Please run `srcdep --help` to get the full document.

### SRCDEP.yaml format

Please refer to [SRCDEP.yaml](SRCDEP.yaml).
