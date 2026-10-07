# 维护说明（内部文档）

> 这是**仓库维护者自用**的说明。访客请看 [README.md](README.md)。
> 日常只需要：**放材料 → 一条命令归位 → `git add/commit/push`**，Pages 会自动重建（约 30–60 秒生效）。

---

## 一、继续上传项目材料（日常核心流程）

```powershell
# 约定：$py = DSH 自带 Python（路径固定）
$py = "C:\Users\23067\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"

# ① 归位：自动判断图片/视频、自动编号、图片缩到 1600px、视频压到 720p
& $py tools\import_material.py 02 "C:\Users\23067\Desktop\电镀\总装图.png" --name assembly-overview

# ② 工具会打印一段可直接粘贴的 <figure> 片段 → 粘到 index.html 对应项目处并补图注
# ③ 查看各项目已有材料
& $py tools\import_material.py --list
# ④ 提交发布
git add -A; git commit -m "add: 02 电镀装备 总装图"; git push
```

项目编号：`01` 高温钢管检测平台 ｜ `02` 电镀装备 ｜ `03` 力学性能预测

**命名规范**（`NN` 决定页面展示顺序）：
图片 `figNN-<slug>.png|jpg` ｜ 视频 `animNN-<slug>.mp4` ｜ 文档 `docNN-<slug>.pdf`

**目录名用中文、文件名用英文 slug**——可读性 + URL 友好兼得。改目录名时记得同步改：`index.html` 里的路径、`tools/import_material.py` 的 `PROJECTS` 映射、各 README 里的引用。

---

## 二、每次新增材料都要过一遍脱敏清单

- [ ] 无企业名称、委托方标识、项目代号、图号、图纸编号、批次号
- [ ] 无 CAD/CAE 软件界面残留（工具栏、文件路径、文件名、坐标系标签）
- [ ] 无人员姓名、工号、联系方式、设备铭牌
- [ ] 几何外形与仿真结论：确认委托方/学校允许公开
- [ ] 现职单位（航空液压作动器相关）材料**不要**放入

完整版见 [projects/README.md](projects/README.md)。

---

## 三、发布（Pages 已开通，日常无需操作）

- 线上地址：<https://xty-9016.github.io/portfolio/>
- 仓库：<https://github.com/XTY-9016/portfolio>
- 发布方式：**Deploy from a branch → `main` / `(root)`**（`build_type=legacy`），已通过 GitHub API 开通
- 日常：`git push` 后 30–60 秒自动重建；失败可在仓库 **Actions** 标签看 `pages build and deployment`

### 本机 git 配置（已设好，换机器时需要重设）
```powershell
git config user.name  "谢天艺"
git config user.email "2306711103@qq.com"
git config http.proxy  "http://127.0.0.1:7897"   # Clash 端口；关代理时用 --unset
git config core.quotepath false                    # 中文文件名不显示为转义
```

### 迁移到其他托管（同一套文件，直接拖/传）
- **Cloudflare Pages**：dash.cloudflare.com → Workers & Pages → Create → Pages → Upload assets → 拖整个目录
- **Gitee Pages**：新建公开仓库上传 → 服务 → Gitee Pages（需实名）
- **腾讯云 COS / 阿里云 OSS**：开启「静态网站」→ 上传 → 用默认域名访问（国内最快）

> `github.io` 在国内部分网络下慢或打不开。**建议同时挂一个国内可达的镜像，二维码指向它**；
> 或用手机 4G 定期验证线上可达性。

---

## 四、自检

```powershell
& $py tools\check_site.py
```
报告：资源引用是否都存在、总体积、有无超大文件（GitHub 单文件 100MB 上限 / Cloudflare Pages 25MB）、
以及哪些材料还没被页面引用（持续补充阶段属正常）。

---

## 五、本地预览

```powershell
& $py -m http.server 8000 --directory .
# 浏览器打开 http://127.0.0.1:8000
```

---

## 六、已知坑（踩过，记下来）

| 坑 | 现象 | 处理 |
|---|---|---|
| GBK 控制台 | `import_material.py` 打印特殊符号时 `UnicodeEncodeError`（文件其实已保存成功） | 已修：脚本内 `sys.stdout.reconfigure(encoding='utf-8')` |
| HEVC 视频 | H.265 mp4 在 Firefox / 部分 Chrome 播放为黑框 | `import_material.py` 统一转 H.264（720p/CRF28/去音轨） |
| Word 锁定 | 简历 docx 被 Word 打开时 python-docx 报 `PackageNotFoundError`，看似"文件不存在" | 编辑前先在 Word 里关闭该文件 |
| OneDrive + `.git` | 同步冲突、文件锁的潜在风险 | 目前可用；正式长期维护建议 `git clone` 到非 OneDrive 目录（如 `C:\dev\portfolio`）再push |
| 中文路径 | 素材 URL 会百分号编码 | 只在分享**素材直链**时难看；站点根地址不受影响 |
| 页脚声明 | 站内页脚已声明"未公开涉密图纸与数据" | 新增材料时别破坏这个口径 |

---

## 七、简历配套

- 简历 v5（`resume-analysis/谢天艺-*-简历-v5.docx`）页眉含作品集链接 + 二维码（二维码已从 PDF 解码验证可扫）
- 换域名/镜像后需同步改：简历那一行文字 + 重新生成二维码（1 分钟）
- 二维码源文件：`resume-analysis/portfolio-qr.png`

---

## 八、站点当前状态

| 项目 | 图片 | 视频 | 待补（详见各自 NOTES.md） |
|---|---|---|---|
| 01 高温钢管检测平台 | 3 | 2 | 网格、网格无关性对比、收敛曲线、关键点温度表、保守工况 |
| 02 电镀装备 | 4 | 1 | 剖视图、桁架对比云图、机械爪强度校核云图、内筒弯矩云图、热分析、样机照片 |
| 03 力学性能预测 | 0 | 0 | 数据链路图、晶粒尺寸拟合、本构对标、屈服强度对角线图、参数敏感性、模型对比、软件界面 |

总体积约 7.2 MB / 24 个文件。
