# 参与贡献

感谢帮助改进 use-agentsmd。优先提交有实际案例支持的改进，让规则更准确、更短、更容易执行。

## 提交问题

请提供：

1. 使用的宿主及可确认的版本。
2. Skill 的版本或提交。
3. 脱敏后的最小项目结构、相关脚本与原 AGENTS.md。
4. 发给 Agent 的请求、实际输出和你期望的行为。

请勿上传密钥、令牌、客户数据或私有项目文件。用最小示例复现即可。

## 修改流程

1. Fork 并创建自己的分支。
2. 流程改动放在 `skills/use-agentsmd/SKILL.md`，官方资料细节放在 `references/`。
3. 保持来源、项目惯例和本 Skill 的方法之间的区别。
4. 运行 `python scripts/check_package.py`，检查元数据、引用与配图。
5. 对影响判断的改动，用隔离项目执行实际请求；不要只匹配规则文字来宣称行为正确。
6. 在 PR 中说明触发场景、修改后的行为、验证方式和局限。

行为验证建议见 [docs/validation.md](docs/validation.md)。一次修正不应顺带为无关任务增加规则、权限或配置。

## 配图维护

五张配图由 `scripts/generate_visuals.py` 生成可编辑 SVG：

```bash
python scripts/generate_visuals.py
```

PNG 渲染只在维护配图时需要 Playwright，不是 Skill 的运行依赖：

```bash
python -m pip install playwright
python -m playwright install chromium
python scripts/render_visuals.py
python scripts/check_package.py
```

如果本地使用系统 Chrome，可传入 `--browser` 指定可执行文件。生成后应打开图片检查文字、裁切和可读性。

## 发布包

```bash
python scripts/build_release.py
```

生成 `dist/use-agentsmd.zip`，包含 Skill 必需文件、许可证及来源说明。不会把整个 README 图片目录装入 Skill。

提交贡献即表示你同意以本项目的 MIT 许可证发布贡献内容。
