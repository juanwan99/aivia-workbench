# 上游版本钉扎

```
主线组件：Dify（Web）
OpenWork：optional / 二期
```

| 组件 | 版本 / 镜像 tag | 日期 | 备注 |
|------|-----------------|------|------|
| **Dify** | `1.16.1`（compose project `dify`） | 2026-08-05 | https://github.com/langgenius/dify · 镜像 `langgenius/dify-api:1.16.1` / `langgenius/dify-web:1.16.1` · 入口 `https://workbench.aivia.asia`（现网 `47.121.197.52`，本机反代 `127.0.0.1:13080`） |
| DeepSeek 模型 id | `deepseek-chat`（插件 `langgenius/deepseek` `0.0.19`） | 2026-08-05 | 供应商 `langgenius/deepseek/deepseek` · 默认 LLM 已设 |
| OpenWork（optional） | _二期再填_ | | 非主线 |

## 阶段 A 验收摘要（无密钥）

| 项 | 结果 |
|----|------|
| G0 | PASS · 管理员 setup finished |
| G0b | PASS · 短聊「只回：好」→「好」 |
| 默认入口 | PASS · 应用「Aivia 课件（阶段A）」agent-chat · site code `dV3HeqgfVt4Xmm7f` |
| G1 | PASS · 产物 `g1-pea-hybrid.html` |
| G1+ | PASS · 产物 `g1plus-pea-hybrid-with-quiz.html`（同会话改稿，含练习） |
| HTTPS | 自签证书临时启用（Let's Encrypt HTTP-01 外网校验 403；待 DNS-01 或平台证书替换） |

更新主线上游前：跑浏览器 G1/G2，失败则回退 PIN。
