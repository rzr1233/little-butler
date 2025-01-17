# 记账软件 v2.0

一个简单易用的个人和家庭记账软件。

## 功能特性

- [x] 用户管理
  - [x] 用户注册
  - [x] 用户登录/登出
  - [x] 个人资料管理
  - [x] 头像上传
  - [x] 密码重置

- [x] 家庭管理
  - [x] 创建家庭
  - [x] 邀请成员
  - [x] 成员管理
  - [x] 家庭信息编辑

- [x] 账本管理
  - [x] 创建个人/家庭账本
  - [x] 账本列表展示
  - [x] 账本详情查看
  - [x] 账本信息编辑
  - [x] 账本删除功能
  - [x] 账本名称唯一性校验
  - [x] 家庭账本权限控制

- [x] 账单管理
  - [x] 收入/支出记录
  - [x] 自定义分类
  - [x] 账单编辑功能
  - [x] 账单删除功能
  - [x] 账单时间精确到分钟
  - [x] 根据类型动态显示分类
  - [x] 默认分类自动创建
  - [x] 分类图标显示
  - [x] 账单高级搜索
    - [x] 按日期范围搜索
    - [x] 按类型搜索
    - [x] 按分类搜索
    - [x] 按关键词搜索
  - [x] 账单分页显示

- [x] 统计分析
  - [x] 收支趋势图
  - [x] 分类占比分析
  - [x] 月度收支报告
  - [x] 年度收支报告

- [ ] 预算管理
  - [ ] 设置月度预算
  - [ ] 预算执行跟踪
  - [ ] 超支提醒

## 技术栈

- 后端：Django 5.0.1
- 前端：Bootstrap 5
- 数据库：SQLite
- 图标：Font Awesome 5
- 数据可视化：Plotly 5.18.0
- 数据处理：Pandas 2.1.4

## 开发环境

### 虚拟环境使用
1. 打开虚拟环境：
   ```powershell
   # 首次使用需要设置（仅需执行一次）
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # 进入项目目录
   cd 项目目录
   
   # 激活虚拟环境
   .\venv\Scripts\Activate.ps1
   ```
   
   激活成功后，命令提示符前会出现 `(venv)`，例如：
   ```powershell
   (venv) PS E:\编程\AI编程\记账软件>
   ```

2. 退出虚拟环境：
   ```powershell
   deactivate
   ```

3. 安装新的依赖包：
   ```powershell
   # 确保在虚拟环境中（命令提示符前有(venv)）
   pip install 包名==版本号
   
   # 安装完后更新requirements.txt
   pip freeze > requirements.txt
   ```

## 部署说明

### PythonAnywhere部署
1. 在PythonAnywhere创建Web应用
2. 克隆代码仓库：
   ```bash
   # 使用 GitHub
   git clone https://github.com/rzr1233/little-butler.git
   # 或使用 Gitee（推荐国内用户使用）
   git clone https://gitee.com/你的用户名/项目名称.git
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置Web应用：
   - 设置Python版本为3.8或更高
   - 配置虚拟环境
   - 设置WSGI配置文件
   - 配置静态文件路径

### 代码更新步骤
1. 进入项目目录：
   ```bash
   cd little-butler
   ```
2. 拉取最新代码：
   ```bash
   git pull origin master
   ```
   如遇冲突，可重置：
   ```bash
   git reset --hard
   git pull origin master
   ```
3. 安装新依赖：
   ```bash
   # 创建虚拟环境（已经创建了）
   python -m venv venv
   
   # 激活虚拟环境
   # Windows PowerShell:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # 首次使用需要设置
   .\venv\Scripts\Activate.ps1
   # Windows cmd:
   .\venv\Scripts\activate.bat
   # Linux/Mac:
   source venv/bin/activate
   
   # 安装依赖
   pip install -r requirements.txt
   ```
4. 数据库迁移：
   ```bash
   # 可选：备份数据
   python manage.py dumpdata > backup.json
   # 执行迁移
   python manage.py migrate
   ```
5. 收集静态文件（如有更新）：
   ```bash
   python manage.py collectstatic
   ```
6. 重新加载web应用：
   ```bash
   touch /var/www/rzr1233_pythonanywhere_com_wsgi.py
   ```

### 故障排除
- 检查错误日志
- 确保所有依赖正确安装
- 确保数据库迁移成功
- 如需回滚：
  ```bash
  git checkout <之前的commit号>
  python manage.py loaddata backup.json
  ```

### Git连接问题解决
如果遇到SSL连接问题或无法推送代码，建议切换到SSH方式：

1. 检查SSH密钥：
   ```bash
   ls ~/.ssh
   ```

2. 如果没有SSH密钥，生成新的：
   ```bash
   ssh-keygen -t ed25519 -C "你的邮箱"
   ```

3. 将公钥添加到代码托管平台：
   - 复制公钥内容：`cat ~/.ssh/id_rsa.pub`
   - GitHub方式：
     - GitHub.com -> Settings -> SSH and GPG keys
     - 点击 "New SSH key" 并粘贴公钥
   - Gitee方式：
     - Gitee.com -> 设置 -> SSH公钥
     - 点击 "添加公钥" 并粘贴公钥

4. 更改仓库为SSH方式：
   ```bash
   # GitHub方式
   git remote set-url origin git@github.com:rzr1233/little-butler.git
   # Gitee方式
   git remote set-url origin git@gitee.com:你的用户名/项目名称.git
   ```

5. 测试SSH连接：
   ```bash
   # GitHub
   ssh -T git@github.com
   # Gitee
   ssh -T git@gitee.com
   ```
   看到认证成功的信息即表示成功

### 数据库迁移方法

方法一：直接复制数据库文件（推荐）
1. 在本地找到 `db.sqlite3` 文件
2. 在PythonAnywhere的Files页面上传到项目目录
3. 重启web应用：
   ```bash
   touch /var/www/zyn1233_pythonanywhere_com_wsgi.py
   ```

方法二：使用Django的导入导出功能
1. 在本地导出数据：
   ```bash
   python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
   ```
2. 将导出的文件上传到PythonAnywhere
3. 在PythonAnywhere中导入：
   ```bash
   python manage.py loaddata data.json
   ```

注意：如果遇到编码问题，可以分应用导出导入：
```bash
# 导出
python manage.py dumpdata auth.user > users.json
python manage.py dumpdata accounts > accounts.json
python manage.py dumpdata bills > bills.json
python manage.py dumpdata stats > stats.json

# 导入
python manage.py loaddata users.json
python manage.py loaddata accounts.json
python manage.py loaddata bills.json
python manage.py loaddata stats.json
```

## 作者

清香客

## 更新日志

### 2024-01-16 (v2.1)
- 添加统计分析功能
  - 实现收支趋势图表
  - 实现支出分类占比分析
  - 添加月度收支对比
  - 添加年度收支统计
- 集成Plotly和Pandas用于数据可视化
- 优化了虚拟环境配置
- 改进了数据展示精度

### 2024-01-15 (v2.0)
- 添加账单高级搜索功能
  - 支持按日期范围搜索
  - 支持按类型和分类搜索
  - 支持按关键词搜索备注信息
- 实现账单分页功能
- 优化账单列表显示
- 修复金额显示精度问题
- 改进密码重置功能
- 优化数据库查询性能

### 2024-01-14 (v1.1)
- 修复了账本删除后的访问问题
- 修复了家庭账本的权限控制
- 修复了日期时间显示格式问题
- 优化了数据库结构
- 改进了分类选择的用户体验
- 添加了分类图标显示

### 2024-01-13 (v1.0)
- 实现账本的创建和编辑功能
- 添加账单记录功能
- 实现基础的收支统计
- 添加账本名称唯一性校验
- 实现账本删除功能
- 实现账单编辑和删除功能

### 2024-01-12 (v0.1)
- 完成用户注册和登录功能
- 实现个人资料管理
- 添加家庭创建和管理功能 