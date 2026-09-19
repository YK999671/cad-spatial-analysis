# 工程图纸多专业分析（cad-spatial-analysis）

一个面向 Codex 的只读工程图纸分析技能。它以 DWG/DXF 对象为主要依据，并可结合 PDF、图片、图签、图例和详图，按专业建立空间、构件、系统及跨图关系。

## 能力范围

- 建筑：空间、门窗、楼梯、路径、洞口、高差和详图索引。
- 结构：基础、柱、墙、梁、板、节点、构件表及配筋关系。
- 给排水、电气、暖通：设备、管线、回路、立管、末端与系统连接。
- 施工布置与工序：场地、道路、临设、设备、阶段和明确的工序依赖。
- 多专业对照：按楼栋、楼层、轴网、标高、编号和索引建立可追溯关系。

技能默认只读，不修改源图，不把工程常识冒充图纸事实，也不默认开展设计验算、规范审查或工程量统计。

## 安装

在 Codex 中使用技能安装器，并提供本仓库地址：

```text
请安装这个技能：https://github.com/YK999671/cad-spatial-analysis
```

也可以将仓库克隆到 Codex 技能目录：

```bash
git clone https://github.com/YK999671/cad-spatial-analysis.git ~/.codex/skills/cad-spatial-analysis
```

安装后可这样调用：

```text
使用 $cad-spatial-analysis 只读分析我提供的图纸文件夹，先建立图纸索引，再回答三层西侧活动室附近有哪些梁、柱、洞口和高差。
```

## 使用方式

提供图纸文件夹或单个文件路径即可。只给目录时，技能先完成资料清单、专业识别和全局概览；提出具体问题时，会定位相关主图、详图和跨专业依据，并区分：

- 直接读取；
- 对象关系推理；
- 未确认或冲突。

分析报告默认写入当前工作区的 `drawing-analysis` 子目录，不写入源图目录。

## 文件结构

```text
cad-spatial-analysis/
├── SKILL.md
├── agents/openai.yaml
├── scripts/inventory.py
└── references/
    ├── construction.md
    ├── cross-drawing.md
    ├── evidence-model.md
    ├── local-reader.md
    ├── mep.md
    ├── route-audit.md
    └── structure.md
```

`scripts/inventory.py` 只生成文件清单、哈希和重复内容分组，不解析图形，也不会修改图纸。

## 可选本机依赖

技能本身不绑定某个 CAD 服务。对象级读取可使用当前环境已有的 CAD MCP，或采用：

- Python 3；
- `ezdxf`；
- ODA File Converter（读取 DWG 时）。

没有对象级读取能力时，也可以对 PDF 或图片进行受限的视觉分析，但报告必须明确证据降级和读取限制。

## 许可

本项目采用 MIT License，详见 [LICENSE](LICENSE)。
