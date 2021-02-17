# 問題解決測驗平台

## Introduction

This a open-source tool.

## Requirements
Node.js >= 14.15.5
python >= 3.6
MongoDB >= 4.0.22

## Installation

### 1. Set PATH
open windows search bar type "環境變數" or "environment variable"
Set [MongoDB File location]\\Server\\[version]\\bin to PATH

### 2. Install package
1. Install python package
```
pip install -r requirements.txt
```
2. Install node.js package under 
NodejsWebApp1 ver [5.3.4 or 5.2.4]\NodejsWebApp1 folder

```
npm install
```

### 3. Make Launcher.exe
1. In Launcher.py folder
```
pyinstaller -F .\Launcher.py
```
2. get the "Launcher.exe" in dist folder
3. put it in the NodejsWebApp1 ver [5.3.4 or 5.2.4] folder

### 4. Start platform
1. Open Launcher.exe
2. Create users'account and users'password
3. (option) Set second for every quiz and network port
4. Click launch and server will start soon
5. login in admin page use Account:admin Password:admin

## LICENSE
```
MIT License

Copyright (c) 2021 National Taiwan Normal University

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```