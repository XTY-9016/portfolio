# 项目 03 · 不锈钢板带力学性能预测（硕士学位论文）—— 待上传材料清单

**页面位置**：`index.html` 的「项目三」段落（当前只有文字）
**技术要点**：Sellars + Burke-Turnbull 晶粒尺寸演化唯象模型（R²=0.89）+ Hall-Petch + Swift-Voce 分段本构；屈服强度与实测对标 MAE 23.82 MPa；XGBoost + 随机森林融合预测（屈服/抗拉/延伸率 R² = 0.941 / 0.913 / 0.922）；PySide2 一体化软件已交付

## 建议上传的材料（按页面展示顺序）

| 建议文件 | 内容 | 说明 |
|---|---|---|
| `fig01-dataset-pipeline.png` | 数据链路图：产线工艺数据 + EBSD 组织 + 拉伸试验 → 数据集 | 一眼看懂"数据从哪来" |
| `fig02-grain-size-model.png` | 晶粒尺寸模型拟合结果（R²=0.89 的散点/拟合线） | 机理模型的验证图 |
| `fig03-constitutive-curve.png` | Hall-Petch + Swift-Voce 分段本构与实测真应力-真应变曲线对比 | 体现"试验对标" |
| `fig04-ys-diagonal.png` | 屈服强度预测值 vs 实测值对角线图（MAE 23.82 / RMSE 27.75 MPa） | 论文图 3-5 可直接用 |
| `fig05-sensitivity.png` | 工艺参数重要性/敏感性排序（终轧压下率为核心变量） | 对应"参数敏感性分析" |
| `fig06-model-comparison.png` | 模型对比：XGBoost / RF / 融合 / 融合+半监督 的 R² 对比 | 用论文表 4-6 重绘更清楚 |
| `fig07-software-ui.png` | PySide2 软件界面（三大模块） | **务必打码文件路径、钢种代号、流程卡号** |
| `fig08-confidence-interval.png` | Bootstrap 置信区间预测结果图 | 体现"不只是点预测" |
| `anim01-software-demo.mp4` | 软件操作录屏（可选，10–20 秒） | 交付物最有说服力的形式 |
| `doc01-thesis-abstract.pdf` | 论文摘要页（可选） | 只想给"证明"时用；**注意别放全文**（涉企业委托内容） |

## 上传命令示例

```powershell
$py = "C:\Users\23067\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
& $py tools\import_material.py 03 "C:\Users\23067\Desktop\论文\图3-5.png"     --name ys-diagonal
& $py tools\import_material.py 03 "C:\Users\23067\Desktop\论文\软件界面.png"   --name software-ui
& $py tools\import_material.py 03 "C:\Users\23067\Desktop\论文\软件演示.mp4"   --name software-demo
```

## 数据口径提醒（务必与论文一致，答辩刚过，别自己打自己）

- 屈服强度 R² = **0.941**（不是 0.961）；三项中屈服强度确实最高（0.941 > 延伸率 0.922 > 抗拉 0.913）
- 论文**表 4-5** 里屈服强度的 RMSE/MAE 两列疑似写反（出现 RMSE 10.418 < MAE 17.850，不成立）；
  **表 4-6** 同模型为 RMSE 17.850 / MAE 10.418（正确）。对外材料**只用 R²**，避免踩这个坑
- 摘要里"RMSE 下降 57.2%"是基于写反的数值算的；按正确值约为 18.7% → 不要引用这个百分比
- 实验材料是 **201 不锈钢**（316/304 只出现在文献综述与展望），别写成"316/304/201 系"
- 论文里**没有** Abaqus 断裂仿真；对外表述不要把它挂在本文工作上

## 脱敏注意（本项目特有）

- 论文是**企业委托课题**，工艺参数、产线信息、企业名称可能有保密要求 → 图片打码企业名/产线名/流程卡号
- 软件界面截图最容易带出文件路径与真实钢种代号 → 用示例数据重新截图，或在虚拟机/改名目录里截
- 数据集规模、精度指标属可公开的结论；**具体工艺参数值**建议不公开
