# Agent Tool Security Benchmark

用于验证 AI Agent 工具调用安全边界的可复现基准。项目通过合成案例测试工具白名单、参数 Schema、提示注入识别、高风险操作确认、路径沙箱和审计日志。

本仓库是个人开源参考实现，不包含公司业务代码或内部测试集。

## 快速开始

```powershell
python -m agent_tool_security.cli run --cases examples/cases.jsonl --output outputs/result.json
python -m unittest discover -s tests -v
```

## 决策链

1. 工具是否在白名单中
2. 参数是否满足 JSON Schema 子集约束
3. 输入中是否出现提示注入或越权意图
4. 高风险操作是否获得明确确认
5. 文件路径是否位于沙箱目录
6. 记录允许/拒绝原因和审计事件

该基准默认只模拟工具执行，不进行真实删除、付款、发信或系统命令操作。

## 许可

MIT License。仅用于研究、测试和防御目的。
