# 项目材料归档规范

本目录按**项目**分类，每个项目下再分 `images/`、`videos/`、`docs/`。
页面（`index.html`）只引用这些路径，所以**你只要把材料放对位置，页面就能引用它**。

```
projects/
├── 01-高温钢管检测平台/        高温钢管表面缺陷检测平台
│   ├── images/               figNN-<slug>.png|jpg
│   ├── videos/               animNN-<slug>.mp4
│   ├── docs/                 docNN-<slug>.pdf（报告、图纸导出等）
│   └── NOTES.md              该项目材料清单 + 待补项
├── 02-电镀装备/     封闭式滚动电镀成套装备
│   └── …（同上）
└── 03-力学性能预测/             不锈钢板带力学性能预测（硕士学位论文）
    └── …（同上）
```

## 命名规范（重要：URL 友好 + 自动排序）

| 类型 | 规范 | 示例 |
|---|---|---|
| 图片 | `figNN-<slug>.png\|jpg` | `fig04-mesh-overview.png` |
| 视频 | `animNN-<slug>.mp4` | `anim03-transient-preview.mp4` |
| 文档 | `docNN-<slug>.pdf` | `doc01-simulation-report.pdf` |

- `NN` 是两位序号，**决定页面展示顺序**，由工具自动分配
- `<slug>` 用**英文小写 + 连字符**（中文文件名在 URL 里会被百分号编码，不利于分享）
- 图片宽 > 1600px 会被自动等比缩小；视频自动压成 720p/CRF28/去音轨（体积约降 90%）

## 上传流程（推荐）

```powershell
# 1) 把材料归位（自动分类、规范命名、压缩）
& "C:\Users\23067\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" `
    tools\import_material.py 01 "C:\Users\23067\Desktop\网格截图.png" --name mesh-overview

# 工具会打印一段可直接粘贴到 index.html 的 <figure> 片段（含 TODO 图注）

# 2) 看看现在各项目都有什么
& "C:\Users\23067\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" tools\import_material.py --list

# 3) 提交并推送
git add -A; git commit -m "add: 01 网格与收敛曲线"; git push
```

一次导入整个目录里的所有文件：

```powershell
python tools\import_material.py 02 "C:\Users\23067\Desktop\电镀装备材料\"
```

## 发布前脱敏清单（每次新增材料都要过一遍）

- [ ] 无企业名称、委托方标识、项目代号、图号、图纸编号、批次号
- [ ] 无 CAD/CAE 软件界面残留（工具栏、文件路径、文件名、坐标系标签里的项目名）
- [ ] 无人员姓名、工号、联系方式
- [ ] 几何外形与仿真结论：确认委托方/学校允许公开
- [ ] 现职单位（航空液压作动器相关）材料**不要**放进本仓库
- [ ] 图片 EXIF 已清理（`import_material.py` 用 PIL 重新保存，会自动去掉 EXIF）

## 各项目材料现状

| 项目 | 图片 | 视频 | 文档 | 状态 |
|---|---|---|---|---|
| 01 高温钢管检测平台 | 3 | 2 | 0 | 已有基础材料，待补网格/收敛/温度表/保守工况 |
| 02 封闭式滚动电镀装备 | 0 | 0 | 0 | **待上传**（清单见 NOTES.md） |
| 03 硕士论文（机理+数据） | 0 | 0 | 0 | **待上传**（清单见 NOTES.md） |

用 `tools\check_site.py` 可以随时检查：引用是否完整、有没有超大文件、哪些材料还没被页面引用。
