# UI自动化

### 平台介绍

​		•通过测试工具或其他手段，按照测试人员计划的测试用例去执行测试。

​		•目的是减轻手工测试的工作量。

​		•通常使用ui自动化做正向的、稳定的、回归测试用例简单来说，就是用代码模仿手工测试

### UI平台源码目录展示

#### autoTestPlatform：后端代码

###### 依赖包安装

```
⭐️安装依赖包：pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r req_autoTestP.txt
⭐️注意：需要按照 req_autoTestP.txt 内指定版本进行安装
⭐️单独安装依赖包：pip3 install django -i https://mirrors.aliyun.com/pypi/simple/
⭐️单独卸载依赖包：pip3 uninstall django
⭐️依赖包安装成功后，使用   python3 manage.py runserver 127.0.0.1:8001 运行服务
⭐️注意：本地安装的是 python3 环境，所以使用 python3 manage.py runserver 127.0.0.1:8001运行服务
```

##### 使用 python3 manage.py runserver 127.0.0.1:8001 运行后端服务

![运行后端服务](/Users/tankaihua/Desktop/git/alter_test_platfrom/autofrontend/src/assets/img/run_python3.png)



#### autofrontend：前端代码

###### 依赖包安装

```
⭐️安装依赖关系:	npm install
⭐️使用 localhost:8080 进行热重载服务:	npm run dev
为生产进行最小化构建:	npm run build
为生产构建并查看包分析器报告:	npm run build --report
运行单元测试:	npm run unit
运行e2e测试:  npm run e2e
运行所有测试: npm test
```

#####  使用 npm run dev 运行前端服务

![运行前端服务](/Users/tankaihua/Desktop/git/alter_test_platfrom/autofrontend/src/assets/img/npm_run_dev.png)

##### 使用 http://0.0.0.0:8081 访问 UI 平台

![登录](/Users/tankaihua/Desktop/git/alter_test_platfrom/autofrontend/src/assets/img/login.png)



###### 代码存放位置

```
⭐️ build
⭐️ config
⭐️ node_modules
⭐️ src/api
⭐️ src/assets/ico
⭐️ src/assets/iconfont
⭐️ src/assets/img
⭐️ src/components
⭐️ src/config
⭐️ src/router
⭐️ src/style
⭐️ src/page
  - backCaseList.vue:     UI用例列表icon展示以及功能文字展示
  - backParamAdd.vue:     UI参数配置icon展示以及功能文字展示
  - backParamList.vue:    UI参数列表icon展示以及功能文字展示
  - backReport.vue:       UI测试报告icon展示以及功能文字展示
  - backstepmod.vue:      UI复用步骤修改icon展示以及功能文字展示
  - envManagement.vue:    UI环境管理icon展示以及功能文字展示
  - groupManagement.vue:  UI分组管理icon展示以及功能文字展示
  - help.vue:   	  UI帮助文档icon展示以及功能文字展示
  - home.vue:             首页背景展示
  - Login.vue:  	  登录页面icon展示以及功能文字展示
  - menu.vue:   	  左侧icon展示以及功能文字展示
⭐️ App.vue:	
⭐️ main.js:
⭐️ static: 
⭐️ test/e2e/custom-asserions
⭐️ test/e2e/specs
⭐️ test/e2e/nightwatch.conf.js:
⭐️ test/e2e/runner.js:
⭐️ test/unit/.eslintrc:		
⭐️ test/unit/jest.conf.js:
⭐️ test/unit/setup.js:
⭐️ .babelrc:
⭐️ .editorconfig:
⭐️ .eslintignore:
⭐️ .eslintrc.js:
⭐️ .postcssrc.js:
⭐️ auto.ico:					title图标
⭐️ element-varlables.scss:
⭐️ index.html: title文字以及title图标展示
⭐️ package-lock.json:	
⭐️ package.json:
```

###### 操作手册

第一步 创建 UI环境管理

第二步 进行 新增 登录 用例  (相当于是前置操作)

第三步 新增 分组管理 (管理不同模块用例)

