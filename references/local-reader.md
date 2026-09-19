# CAD 读取工具与本机回退

使用前先发现当前环境实际可用的工具、转换器和路径。不要依赖开发者机器上的固定目录；下列流程用于在不同设备上选择只读后端。

## 优先发现读取工具

查找 `cad_dwg` 的 summary、entities、layers、block detail 等只读工具。常见名称为 `mcp__cad_dwg__dxf_summary`、`dxf_get_entities_by_type`、`dxf_get_layer_entities`、`dxf_get_block_detail`。以实际返回 schema 为准。

这些接口曾有结果上限，以及 TEXT/MTEXT 接口的兼容性问题。核查总数/截断、块变换和显示状态字段是否足够；不要把接口错误当成图中没有文字。

## 本机后端选择

读取接口不能提供必要信息时，检查当前 CAD 服务或脚本的加载逻辑是否保持只读，再决定是否使用本机 Python 后端。可选组合通常是：

- DXF：使用 `ezdxf.readfile` 读取对象；
- DWG：使用 ODA File Converter 生成临时 DXF 副本，再由 `ezdxf` 读取；也可使用已经配置好的、等价的只读服务；
- 配置：如需 `ezdxf.ini`，只为本次子进程设置配置路径，不修改系统或用户级配置。

先验证 Python、`ezdxf`、转换器和服务的实际版本与路径。不要复制整个可写服务、修改用户的 CAD 配置，或通过保存源图来绕过读取失败。

给本次子进程设置 `EZDXF_CONFIG_FILE` 后再导入相关模块；不要全局修改环境。只访问原始属性、块定义、变换矩阵与读取 API；不调用 `save`、`saveas`、添加/删除/变换源实体等方法。

MTEXT 通常可用 `plain_text()` 读取，但版本可能变化，调用前检查实际 API。导出坐标时正确处理嵌套 INSERT、镜像、OCS、bulge 及可见性；不要把只导出部分类型的预览脚本描述为全量解析器。

工具/转换器/外参不可用时，报告具体失败及已读取部分。若有同版 PDF/图片，可继续其支持的视觉判断并明确证据降级；不能宣称仍然是 CAD 对象级验证。

## 文件夹清单脚本

```powershell
& '<可用的 Python 路径>' -X utf8 '<技能目录>/scripts/inventory.py' '<用户目录或文件>'
```

脚本仅输出 JSON。需要保存清单时，在当前工作区另存输出；后续分析完成后重算被读取源文件的哈希。清单中的 `stable_during_hash` 仅表示计算哈希期间文件大小和修改时间未变，不等于整个分析阶段文件没有变化。
