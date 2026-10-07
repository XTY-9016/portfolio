# 项目 02 · 封闭式滚动电镀成套装备 —— 待上传材料清单

**页面位置**：`index.html` 的「项目二」段落（当前只有文字，图位已用一行小字占位）
**技术要点**：把「开放式 + 多重溶液浸泡」改为「封闭式电镀箱 + 溶液工序控制 + 滚动式动态电镀」；电镀均匀性 +25%、单件 −18min；CATIA 结构设计 + ANSYS/Abaqus 仿真校核

## 已有材料（2026-10-07 导入）

| 文件 | 页面图号 | 内容 | 备注 |
|---|---|---|---|
| `images/fig01-equipment-overview.jpg` | 图 1 | 成套装备总体布局渲染 | 800×640，无企业标识 ✓ |
| `images/fig02-gripper-drum-engagement.png` | 图 2 | 机械爪与内筒端部配合（CAD 截图） | 1397×776，含 KUKA 机械臂外观，无企业标识 ✓ |
| `images/fig03-inner-drum-bending-rods.jpg` | 图 3 | 内筒抗弯钢筋 + 三组保持架（渲染） | 800×640，无企业标识 ✓ |
| `images/fig04-robot-base-bracket.png` | 图 4 | 机械臂底座安装平台 + 加劲肋 | 1332×927，无企业标识 ✓ |
| `videos/anim01-handling-animation.mp4` | 动画 1 | 上下料动作动画 41s | 原 HEVC 2.0MB → H.264 720p 0.9MB（浏览器兼容性更好） |

**待确认**：图 4 的功能描述（"底座 + 加劲肋 + 螺栓组 → 承载机械臂载荷"）是我按几何特征写的，
若该件的实际作用不同（例如是气缸连接座的直角焊接支架），告诉我我改图注。

## 建议上传的材料（按页面展示顺序）

| 建议文件 | 内容 | 说明 |
|---|---|---|
| `fig01-assembly-overview.png` | 成套装备总装三维图 | 让人 3 秒看懂"这是什么设备" |
| `fig02-box-cutaway.png` | 电镀箱剖视图（机架/箱体/传动/密封） | 体现结构设计深度 |
| `fig03-truss-comparison.png` | 外箱体改桁架前后的应力/变形对比云图 | **"据此将结构改为桁架形式"的实证**，很关键 |
| `fig04-gripper-assembly.png` | 上下料机械爪总装（气缸 4.4kN、Y 形拉动组件、四爪 45° 布置） | 力学传导路径清晰 |
| `fig05-gripper-check.png` | 夹臂/楔块/销轴/连接座螺栓组强度校核云图 | 对应"四类强度校核" |
| `fig06-inner-drum.png` | 内筒抓取环（环形双斜面楔槽）+ 八根抗弯钢筋 + 三组保持架 | 这个设计的亮点，值得单独一张 |
| `fig07-drum-bending.png` | 内筒平放夹取的弯矩/变形分析云图 | 对应"为加强筋布置提供依据" |
| `fig08-thermal-analysis.png` | 电镀箱电热反应热分析（温度分布） | 对应热分析结论 |
| `fig09-prototype.jpg` | 样机/装配现场照片 | **"样机已落地"最有说服力的一张**（注意打码铭牌、标识、人员） |
| `anim01-assembly-rotate.mp4` | 总装旋转动画（可选） | 比静图更能说明结构关系 |

## 上传命令示例

```powershell
$py = "C:\Users\23067\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
& $py tools\import_material.py 02 "C:\Users\23067\Desktop\电镀\总装图.png"          --name assembly-overview
& $py tools\import_material.py 02 "C:\Users\23067\Desktop\电镀\桁架对比.png"        --name truss-comparison
& $py tools\import_material.py 02 "C:\Users\23067\Desktop\电镀\机械爪总装.png"      --name gripper-assembly
& $py tools\import_material.py 02 "C:\Users\23067\Desktop\电镀\样机照片.jpg"        --name prototype
# 每次都按页面顺序 --name，序号会自动递增
```

## 脱敏注意（本项目特有）

- 电镀箱涉及**企业工艺流程改造**，图纸上可能有企业名称/图号/工艺参数 → 上传前打码
- 样机照片最容易泄露：设备铭牌、车间标识、企业 LOGO、人员面孔
- 涉及电镀液配方、工艺窗口参数等，若属委托方技术秘密，**不要公开具体数值**，只留"均匀性 +25%、单件 −18min"这类结论
