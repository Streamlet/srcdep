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

1. Write a `DEPS.yaml` file at the root directory of your target project, with content as following:

```yaml
DEPS:
  thirdparty/srcdep:
    GIT_REPO: https://github.com/Streamlet/srcdep.git
    GIT_TAG: master
```

2. Run `srcdep` at the root directory of your project.

Then, this project, as a dependency, will be downloaded to thirdparty/srcdep.

## More Documents

### Command Line

Please run `srcdep --help` to get the full document.

### DEPS.yaml format

Please refer to [DEPS.yaml](DEPS.yaml).
