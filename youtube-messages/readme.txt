=== YouTube Messages Auto Import ===
Requires at least: 5.8
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv2 or later

Automatically imports a church's YouTube videos and shows them as a sermon/message grid. Clicking a message opens it on YouTube.

== Setup ==

1. Plugins › Add New › Upload Plugin › choose youtube-messages.zip › Activate.
2. Messages › Settings & Sync:
   * YouTube channel: e.g. https://www.youtube.com/@TrinityUMCFernandinaBeach
   * YouTube API key (recommended, free): Google Cloud Console › new project › enable
     "YouTube Data API v3" › Credentials › Create credentials › API key. Restrict it to the
     YouTube Data API v3. Without a key the plugin falls back to YouTube's RSS feed, which only
     lists the newest 15 videos and is often unavailable.
   * Optional: series playlists (each becomes a Series), title filters, service-type rules.
3. Save, then click "Import full archive" once (or "Check for new videos now").
4. Put [youtube_messages] on the Messages page (Cornerstone: Raw Content; Elementor: Shortcode
   widget; block editor: Shortcode block).

From then on new uploads and finished live streams appear automatically (every hour by default).

== Shortcode options ==

[youtube_messages per_page="12" columns="3" layout="grid" featured="no" filters="yes"
 pagination="yes" series="" type="" show_date="yes" show_type="yes" show_series="no"
 show_duration="yes" show_excerpt="no" date_format=""]

Latest message only: [youtube_messages per_page="1" columns="1" filters="no" pagination="no"]

== Good to know ==

* Shorts and not-yet-started scheduled live streams are skipped (configurable). Private videos
  are never imported.
* Title/description edits made on YouTube are synced; edits made in WordPress are never
  overwritten.
* To hide a video, trash it or set it to Draft. A permanently deleted message is never re-imported.
* Messages have no page of their own on the site: every link (including page-builder loops that
  use the post link) goes to the video on YouTube.
* Imports run on WP-Cron, which fires when the site gets visits. WP Engine sites can turn on
  "Alternate Cron" or a server cron for exact timing.
* Colours: set the accent colour in settings, or override the --ytm-* CSS custom properties on .ytm.
* API quota: an hourly check uses about 50 of the 10,000 free daily units.
