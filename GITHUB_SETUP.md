# 发布到 GitHub 组织的步骤

## 前提条件
- 已安装 Git
- 有 GitHub 账号并且是 cleantempmail 组织的成员
- 已设置 Git 身份验证（SSH 或 Personal Access Token）

## 发布步骤

### 1. 在 GitHub 上创建新仓库

访问：https://github.com/organizations/cleantempmail/repositories/new

- **Repository name**: `python-examples` (或其他你喜欢的名称)
- **Description**: `Official Python examples for CleanTempMail API`
- **Visibility**: Public (推荐，因为是开源示例)
- **不要勾选**: Initialize with README (我们已经有了)

点击 "Create repository"

### 2. 初始化本地 Git 仓库

```bash
cd /Users/meng/Downloads/cursor/cleantempmail/cleantempmail-python-examples

# 初始化 Git
git init

# 添加所有文件
git add .

# 创建第一次提交
git commit -m "Initial commit: CleanTempMail Python API examples"

# 重命名分支为 main
git branch -M main
```

### 3. 连接到 GitHub 组织仓库

**选项 A: 使用 HTTPS (需要 Personal Access Token)**
```bash
git remote add origin https://github.com/cleantempmail/cleantempmail-python-examples.git
```

**选项 B: 使用 SSH (推荐)**
```bash
git remote add origin git@github.com:cleantempmail/cleantempmail-python-examples.git
```

### 4. 推送代码

```bash
# 第一次推送
git push -u origin main
```

### 5. 验证

访问：https://github.com/cleantempmail/cleantempmail-python-examples

应该可以看到所有文件已上传！

## 后续更新

以后修改代码后，使用：
```bash
git add .
git commit -m "描述你的修改"
git push
```

## 常见问题

### Q: 如果没有 SSH 密钥怎么办？
**A:** 使用 HTTPS 方式，但需要创建 Personal Access Token：
1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token，勾选 `repo` 权限
3. 推送时使用 token 作为密码

### Q: 组织仓库和个人仓库有什么区别？
**A:** 
- 组织仓库: `https://github.com/cleantempmail/cleantempmail-python-examples`
- 个人仓库: `https://github.com/YOUR_PERSONAL_USERNAME/python-examples`
- 推荐使用组织仓库，更专业！

### Q: 如何设置仓库描述和主题？
**A:** 在 GitHub 仓库页面：
- 点击右上角的 ⚙️ Settings
- 编辑 Description 和 Topics
- 建议添加 topics: `python`, `api`, `temporary-email`, `email`, `examples`

## 推荐的仓库设置

### 添加主题 (Topics)
在仓库页面点击齿轮图标，添加：
- python
- api
- temporary-email  
- disposable-email
- email-service
- api-client
- examples

### 添加 About 描述
```
Official Python examples for CleanTempMail API - Free temporary email service
```

### 添加网站链接
```
https://cleantempmail.com
```

## 完成后的推广

1. **在主网站添加链接** - 在 API 文档页面添加指向示例的链接
2. **README Badge** - 已包含 Python 和 License badges
3. **Star 自己的仓库** - 给自己的项目加星
4. **社交分享** - 在相关社区分享

---

完成以上步骤后，你的 Python 示例代码就正式发布了！🎉
