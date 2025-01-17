# 小管家记账系统

一个简单易用的个人和家庭记账系统。

## 开发进度
- [x] 用户管理
  - [x] 用户注册/登录
  - [x] 密码重置
  - [x] 个人信息管理
- [x] 账户管理
  - [x] 个人账户
  - [x] 家庭账户
  - [x] 账户余额计算
- [x] 记账功能
  - [x] 收入支出记录
  - [x] 分类管理
  - [x] 账单搜索
- [ ] 统计分析
  - [x] 月度收支趋势图（待修复：图表显示问题）
  - [x] 支出分类占比（待修复：图表显示问题）
  - [x] 月度统计比较
  - [x] 年度汇总数据
- [ ] 预算管理
  - [ ] 设置月度预算
  - [ ] 预算执行跟踪
  - [ ] 超支提醒

## 待修复问题
1. 统计分析页面图表不显示
   - 问题描述：趋势图和分类占比图无法正常显示
   - 可能原因：Plotly.js加载顺序或配置问题
   - 解决方向：检查JavaScript加载顺序，调整图表配置

## 版本历史

### v2.1 (2024-01-21)
- 新增统计分析功能
  - 添加月度收支趋势图
  - 添加支出分类占比图
  - 显示月度和年度统计数据
  - 优化图表显示效果，支持中文月份显示
- 优化数据展示
  - 所有金额统一保留两位小数
  - 优化图表布局和样式
- 已知问题
  - 统计分析页面的图表显示异常

### v2.0 (2024-01-20)
- 实现基础记账功能
- 支持个人账户和家庭账户
- 支持收入和支出记录
- 支持账单分类管理
- 支持多用户系统
- 支持密码重置功能

## 功能特性

1. 账户管理
   - 支持个人账户和家庭账户
   - 账户余额自动计算
   - 支持账户备注

2. 记账功能
   - 收入/支出记录
   - 自定义分类
   - 日期选择
   - 备注信息

3. 统计分析
   - 月度收支趋势图
   - 支出分类占比
   - 月度统计比较
   - 年度汇总数据

4. 系统功能
   - 多用户支持
   - 密码重置
   - 响应式界面

## 技术栈

- Django 5.0.1
- Bootstrap 5
- Plotly.js (数据可视化)
- SQLite3 (数据库)

## 部署说明

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 数据库迁移
```bash
python manage.py migrate
```

3. 创建超级用户
```bash
python manage.py createsuperuser
```

4. 运行开发服务器
```bash
python manage.py runserver
```

## Git连接问题解决

如果遇到SSL证书问题，可以尝试以下方法：

1. 关闭SSL验证：
```bash
git config --global http.sslVerify false
```

2. 使用SSH方式：
   - 检查是否有SSH密钥：`ls ~/.ssh`
   - 如果没有，生成新密钥：`ssh-keygen -t ed25519 -C "你的邮箱"`
   - 将公钥添加到GitHub
   - 修改仓库为SSH方式：`git remote set-url origin git@github.com:rzr1233/little-butler.git`
   - 测试连接：`ssh -T git@github.com`

## 数据库迁移方法

### 方法一：直接复制数据库文件（推荐）
1. 找到本地的 `db.sqlite3` 文件
2. 上传到PythonAnywhere项目目录
3. 重启web应用

### 方法二：使用Django导入导出
1. 导出数据：
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```
2. 上传data.json文件
3. 导入数据：
```bash
python manage.py loaddata data.json
```

注意：如果遇到编码问题，请确保使用UTF-8编码保存文件。

## 作者
清香客

## 许可
MIT License 