# WordPress plugins (ready to install)

| File | What |
|---|---|
| `rrs-site-assistant.zip` | **RRS Site Assistant 0.2.0**: AI chat that edits a Cornerstone site, with CSMCP built in. |

Install: WordPress → Plugins → Add New → Upload Plugin → choose the zip → Activate.
Then add the API key to `wp-config.php`:

```php
define( 'RRS_AI_API_KEY', 'sk-ant-...' );
```

The source is in [`../rrs-site-assistant/`](../rrs-site-assistant/). Its README covers setup, safety and settings.
After changing the source, rebuild the zip from the repo root:

```bash
rm -f wordpress-plugin/rrs-site-assistant.zip && zip -qr -X wordpress-plugin/rrs-site-assistant.zip rrs-site-assistant -x '*.DS_Store'
```
