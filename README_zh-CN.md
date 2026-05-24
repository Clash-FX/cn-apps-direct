# cn-apps-direct

[English](README.md) | [简体中文](README_zh-CN.md)

社区维护的 macOS 国内常用应用 `PROCESS-NAME` 直连规则集，采用 mihomo / Clash classical rule-provider 格式。

服务于 [ClashFX](https://github.com/Clash-FX/ClashFX) 的 **Bypass Common Chinese Apps**（增强模式 → 国内 App 直连）开关。开关打开后，ClashFX 会在生成的 `.enhanced_config.yaml` 顶部注入这份清单，让里面列出的 app 流量绕开 TUN/代理直接走系统出口，避免"TUN 模式下微信频繁掉线"这类因出口 IP 频繁变化触发风控的问题。

## 使用方式

### 通过 ClashFX 使用（默认场景）

菜单栏 → 增强模式 → ☑ Bypass Common Chinese Apps。除此之外不需要任何操作。

### 独立使用（其他 mihomo / Clash 客户端）

在你的 `config.yaml` 加入：

```yaml
rule-providers:
  clashfx-cn-apps-direct:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/Clash-FX/cn-apps-direct/main/apps-direct.list
    path: ./ruleset/clashfx-cn-apps-direct.list
    interval: 86400

rules:
  - RULE-SET,clashfx-cn-apps-direct,DIRECT
  # ... 然后是你原来的规则
```

## 进程名到底该写什么？

mihomo 的 `PROCESS-NAME` 匹配的是 `<App>.app/Contents/MacOS/<executable>` 里那个**裸可执行文件名**，**不是** bundle id，**也不是**完整路径。查某个 app 的进程名：

```bash
ls /Applications/WeChat.app/Contents/MacOS/
# → WeChat
```

`MacOS/` 后面那一串就是 `PROCESS-NAME,<name>,DIRECT` 里的 `<name>`。

匹配是**大小写不敏感**的，但**中文和英文是两个不同的字符串**——`bilibili` 不会匹配 `哔哩哔哩`。不确定时两个都加。

## 如何贡献

欢迎 PR。添加一个 app 的流程：

1. 用 `ls App.app/Contents/MacOS/` 确认 macOS 实际可执行文件名。
2. 在 `apps-direct.list` 对应分类下加规则。
3. 同一分类内尽量字母序排列。
4. 提 PR，标题写 "Add `<App 名称>` (`PROCESS-NAME`)"。

收录标准：

- App 必须有**官方 macOS 客户端**（不接受第三方/iPad 兼容运行版本）。
- App 必须**在中国大陆常用**，并且在 TUN/代理下确实有故障表现（掉线、登录循环、推送收不到、推荐内容按外网 IP 偏斜等）。
- 一个 PR 加一个 app，方便 review 和回滚。

候选 app 清单见 [Issue #2](https://github.com/Clash-FX/cn-apps-direct/issues/2)，可以认领后开 PR。

## 许可证

MIT
