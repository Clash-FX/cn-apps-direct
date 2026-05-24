# cn-apps-direct

[English](README.md) | [简体中文](README_zh-CN.md)

Curated `PROCESS-NAME` bypass rules for common Chinese apps on macOS, in
mihomo / Clash classical rule-provider format.

Consumed by [ClashFX](https://github.com/Clash-FX/ClashFX)'s **Bypass Common
Chinese Apps** toggle (Enhanced Mode menu). When the toggle is on, ClashFX
injects this list at the top of the rules in its generated
`.enhanced_config.yaml`, so the listed apps' traffic skips TUN/proxy and
goes direct — avoiding the "WeChat keeps disconnecting under TUN" class of
issues caused by frequent IP changes.

## Usage

### Through ClashFX (default consumer)

Menu Bar → Enhanced Mode → ☑ Bypass Common Chinese Apps. Nothing else
required.

### Standalone (other mihomo / Clash clients)

Add this to your `config.yaml`:

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
  # ... your existing rules below
```

## What's the right process name?

mihomo's `PROCESS-NAME` matches the bare executable name found at
`<App>.app/Contents/MacOS/<executable>`, not the bundle id and not the full
path. To find it for a specific app:

```bash
ls /Applications/WeChat.app/Contents/MacOS/
# → WeChat
```

The string after `MacOS/` is what goes into `PROCESS-NAME,<name>,DIRECT`.

## Contributing

PRs welcome. To add an app:

1. Verify the macOS executable name with `ls App.app/Contents/MacOS/`.
2. Add the rule in the appropriate section of `apps-direct.list`.
3. Keep entries alphabetical within each section where reasonable.
4. Open a PR with a short note: "Add `<App Name>` (`PROCESS-NAME`)".

Rules of inclusion:

- App must have an **official macOS client**.
- App must be **commonly used in mainland China** and reasonably expected
  to misbehave under TUN/proxy (e.g. session drops, login loops, ranking
  bias).
- One PR per app where possible, for easy review and revert.

## License

MIT
