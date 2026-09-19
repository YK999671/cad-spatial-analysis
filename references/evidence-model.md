# 图纸对象、专业关系与证据记录

用于全局基线、跨轮问答和交接。使用 JSON 或等价表格即可，不必为小问题填满所有字段。

## 图纸与覆盖

- `source`: 绝对路径、SHA-256、读取时间、图纸版本/楼栋/楼层（未知则为空）、工具及读取状态。
- `frame`: 专业、图种、图号、模型/布局、图面范围、坐标系、单位、标高基准、北向证据；一文件多图框分别登记。
- `coverage`: 区域/系统ID、包围框或页码、对象/边界/索引读取状态、截断/外参/类型支持问题。
- `limitations`: 具体受影响区域和对象，不写泛泛免责声明。

“主图各区已浏览”不等于“所有对象归属和关系已确认”。分别记录覆盖状态与关系核验状态。

## 对象

建议字段：

```json
{
  "id": "文件哈希:主图ID:父块/子块/对象句柄",
  "handle_path": "父块/对象句柄",
  "type": "INSERT",
  "layer_raw": "原始图层",
  "layer_effective": "考虑块继承后的图层",
  "world_geometry": null,
  "raw_text": null,
  "block_name": null,
  "visibility": {"entity": "unknown", "ancestors": "unknown", "layer": "unknown"},
  "geometry_support": "exact / approximated / unsupported"
}
```

未知留空，不填猜测的坐标。块插入点、文字插入点、边界范围分开。

## 通用专业节点与关系

节点增加 `discipline`、`entity_kind`、`label_raw`、`system_or_circuit_id`、`floor`、`axis_location`、`elevation_reference` 和原始属性证据；不适用的字段省略。同名梁、同号回路、同名房间按图面及归属区分实例。

关系使用：

- `from`、`to`：唯一节点ID。
- `relation_type`：例如 `adjacent`、`passage`、`supports`、`connected_to`、`feeds`、`routed_via`、`detail_ref`、`precedes`、`same_instance_candidate`；按问题选用并解释，关系名称本身不构成证据。
- `status`：`confirmed` / `ruled_out` / `unknown` / `conflicting`。
- `evidence_direct`、`inference`、`unresolved`：原始依据、推理步骤、缺失或冲突信息。
- `scope`：专业、楼栋、楼层、系统、图纸版本与施工阶段。
- `scenario`：用户假设及受影响的唯一对象ID；不覆盖源图状态。
- `direction_basis`：方向性来自箭头、回路归属或明确标注，未知时不强加。

跨图对应额外记录两个源图ID、索引号、匹配依据、坐标变换及其验证状态；冲突记录双方原文，不自动用一方覆盖另一方。

尺寸/属性记录 `value_raw`、`value_parsed`、`unit`、`source_handle_or_page`、`association_basis`。不清晰字符保留原文和疑点，不能悄悄修成常用规格。

## 建筑模块：空间

- `space_id`：文件与主图范围内唯一。
- `label_raw`、`label_handles`：图中文字及句柄。
- `analysis_name`：如“图面左侧第2间活动室”，注明临时编号。
- `boundary_evidence`、`boundary_status`：闭合边界/局部边界/仅文字定位。
- `kind`：主体、内部功能区、走廊、楼梯平台、竖井、屋面等；附上解释证据。

## 建筑模块：连接

以下是既有建筑记录的细化格式，可映射到通用关系状态：确认通路/隔断对应 `confirmed` 的 passage/barrier，未确认对应 `unknown`。

- `from`、`to`：两个空间ID。
- `connector_id`：唯一门实例，或无编号开口的分析ID。
- `label_raw`：M1429 等标签，可重复。
- `status`：`confirmed_passage` / `confirmed_barrier` / `unknown`。
- `evidence_direct`：文字、门块及内容、洞口墙端、栏杆、标高/详图引线等可核验对象。
- `inference`：为什么这些对象支持两侧归属和连接/隔断。
- `unresolved`：待确认条件及其对结论的影响。
- `scenario`：源图状态或用户假设；封门记录另加 `blocked_connector_ids`，保留原连接。

不要使用人为百分比制造精确置信度。方向性仅在图中或题设有单向通行限制时设置；门扇开启方向本身不等于只能单向通过。

## 输出与更新

默认报告结构：

1. 资料和读取范围。
2. 专业、图种、主要对象定位及跨图索引。
3. 对象关系表（区分确认、未知和冲突）；建筑可用空间—门/通道—空间表。
4. 未读全区域/系统、归属不明、版本、外参、标高或详图缺失问题。
5. 源文件哈希前后结果与证据文件位置。

后续具体问答只引用必要记录。交接时增加：用户当前假设、历史方案、最新修正、下一步所需证据。明确本地文件不会随 Markdown 自动传到另一对话。
