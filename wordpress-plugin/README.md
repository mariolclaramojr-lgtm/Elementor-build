# WordPress plugins (ready to install)

| File | What |
|---|---|
| `rrs-site-assistant.zip` | **RRS Site Assistant 0.3.0**: AI chat that edits a Cornerstone site, with CSMCP built in. |

Install, all inside WordPress:

1. Plugins → Add New → Upload Plugin → choose the zip → **Activate**.
2. The Site Assistant settings page opens. Paste the Anthropic API key and click **Save Changes**.
   The key is checked when you save.
3. The chat bubble appears at the bottom right for admins.

The source is in [`../rrs-site-assistant/`](../rrs-site-assistant/). Its README covers setup, safety and settings.
After changing the source, rebuild the zip from the repo root:

```bash
rm -f wordpress-plugin/rrs-site-assistant.zip && zip -qr -X wordpress-plugin/rrs-site-assistant.zip rrs-site-assistant -x '*.DS_Store'
```
