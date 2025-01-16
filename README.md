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

- [ ] 统计分析
  - [ ] 收支趋势图
  - [ ] 分类占比分析
  - [ ] 月度收支报告
  - [ ] 年度收支报告

- [ ] 预算管理
  - [ ] 设置月度预算
  - [ ] 预算执行跟踪
  - [ ] 超支提醒

## 技术栈

- 后端：Django 5.0.1
- 前端：Bootstrap 5
- 数据库：SQLite
- 图标：Font Awesome 5

## 部署说明

### PythonAnywhere部署
1. 在PythonAnywhere创建Web应用
2. 克隆代码仓库：
   ```bash
   git clone https://github.com/rzr1233/little-butler.git
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

## 作者

清香客

## 更新日志

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