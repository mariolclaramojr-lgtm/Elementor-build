"""Transparent header (nav floats over the page hero) for every page built in Cornerstone."""
import cs, json, layouts
ids = json.load(open('layout_ids.json'))
PAGES = [8, 11, 12, 92, 103, 14, 82, 88, 113]
asg = [{'group': True, 'condition': 'single:specific-post-of-type|page', 'value': p} for p in PAGES]
r = cs.call('cs_save_layout', id=ids['header'], type='header', title='Lewis Header – Transparent (hero pages)',
            regions=layouts.header_regions(),
            settings={'customCSS': layouts.HEADER_CSS, 'assignments': asg, 'assignment_priority': 0})
print(r.get('summary'))
