# Introduction

本项目用于将 markdown 文件中的本地图片全部替换为将图片上传托管网站后的网络图片地址。

写 markdown 的时候常常会随手贴一张本地图片，但在将 markdown 文件直接分享给他人时别人是看不见你本地的图片的。本项目旨在将你 markdown 中的本地图片一键替换为网络图片，这样所有人查看你的 markdown 文件时都不用再为此烦恼。

# Status

- [X] 获取 markdown 文件中的本地图片地址
- [ ] 将本地图片上传到图片托管网站获取网络图片地址
- [ ] 将原 markdown 中本地图片地址替换为网络图片地址

# Usage

将你想要的处理的 markdown 文件放在当前目录，输入：

```bash
$ python -m Markdown-Image-Upload your-markdown-file.md
```

即可