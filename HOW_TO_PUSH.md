# 如何推送到 GitHub - 完整指南

## 当前状态
✅ Git 仓库已初始化
✅ 所有文件已提交
✅ 远程仓库已配置: `https://github.com/cleantempmail/cleantempmail-python-examples.git`

## 需要完成的步骤

### 步骤 1: 在 GitHub 上创建仓库（如果还没创建）

1. 访问：https://github.com/organizations/cleantempmail/repositories/new
2. **Repository name**: `cleantempmail-python-examples`
3. **Description**: `Official Python examples for CleanTempMail API`
4. **Visibility**: Public
5. **不要勾选任何初始化选项**
6. 点击 "Create repository"

### 步骤 2: 获取 Personal Access Token（如果没有的话）

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置：
   - **Note**: `CleanTempMail Python Examples`
   - **Expiration**: 90 days（或选择其他）
   - **勾选权限**: 
     - ✅ `repo` (完整仓库权限)
4. 点击 "Generate token"
5. **重要**：立即复制token，关闭页面后将无法再看到！

### 步骤 3: 推送到 GitHub

打开终端，执行：

```bash
cd /Users/meng/Downloads/cursor/cleantempmail/python-examples
git push -u origin main
```

当提示输入认证信息时：
- **Username**: 你的 GitHub 用户名
- **Password**: 粘贴你的 Personal Access Token（**不是**GitHub密码）

### 常见问题

**Q: 为什么不能用密码？**
A: GitHub 已经停止支持密码认证，必须使用 Personal Access Token。

**Q: SSH 方式呢？**
A: SSH 需要先配置密钥：
```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥
cat ~/.ssh/id_ed25519.pub

# 在 GitHub Settings → SSH and GPG keys 中添加
```

然后改用 SSH URL：
```bash
git remote set-url origin git@github.com:cleantempmail/cleantempmail-python-examples.git
git push -u origin main
```

**Q: Token 忘记了怎么办？**
A: 在 https://github.com/settings/tokens 删除旧token，重新创建一个。

**Q: 推送成功的标志是什么？**
A: 你会看到类似这样的输出：
```
Enumerating objects: 17, done.
Counting objects: 100% (17/17), done.
...
To https://github.com/cleantempmail/cleantempmail-python-examples.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 完成后验证

访问：https://github.com/cleantempmail/cleantempmail-python-examples

应该能看到所有文件！

---

**当前你需要执行的命令：**
```bash
cd /Users/meng/Downloads/cursor/cleantempmail/python-examples
git push -u origin main
```

需要输入你的 GitHub 用户名和 Personal Access Token。
