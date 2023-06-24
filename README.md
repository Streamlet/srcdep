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

1. Copy SRCDEP.sample.yaml to root directory of your source code and rename to `SRCDEP.yaml`.

2. Run `srcdep` at root directory of your source code.

Then thirdparty/zlib_from_git and thirdparty/zlib_from_url will be fetched.

## Redistributable scripts

The two script files, fetch_deps and fetch_deps.bat, can be redistributed to your source code root, to help those who don't have srcdep environment, to fetch dependencies conveniently.

## More Documents

### Command Line

Please run `srcdep --help` to get the full document.

### SRCDEP.yaml format

Please refer to [SRCDEP.yaml](SRCDEP.yaml).
