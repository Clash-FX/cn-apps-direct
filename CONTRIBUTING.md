# Contributing

Thanks for helping keep this list accurate.

## Adding a new app

1. **Verify the executable name.** Run:
   ```bash
   ls /Applications/<App>.app/Contents/MacOS/
   ```
   Use the exact name printed (case-sensitive).

2. **Confirm the app misbehaves under TUN/proxy.** Examples of qualifying
   symptoms:
   - Frequent disconnects / forced re-login (IP change detection).
   - Push notifications stop arriving.
   - Login fails with no useful error.
   - In-app content recommendations rank by foreign IP.

3. **Edit `apps-direct.list`.** Add the rule in the matching section.
   Keep one app per line.

4. **Open a PR.** Title: `Add <App Name>`. Body should include:
   - macOS version + app version you tested on.
   - The misbehavior you observed without the bypass rule.
   - A link to the official download page if not obvious.

## Removing an app

If an entry is causing issues (wrong process name, app no longer needs
bypass, etc.) — open an issue first so we can discuss, then PR.

## Renaming an executable

If a Chinese app rebrands or changes its binary name across versions,
include **both** the old and new names so older installs still match.

## Format

Plain mihomo / Clash classical rule-provider syntax. One rule per line.
Comments start with `#`. Blank lines OK.

```
PROCESS-NAME,<executable>,DIRECT
```

Do not mix in `DOMAIN`, `IP-CIDR`, etc. — those belong in a different
list.
