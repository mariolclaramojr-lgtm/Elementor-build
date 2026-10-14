import cs, os
MARK = '/* ===== LEWIS REDESIGN START ===== */'
END = '/* ===== LEWIS REDESIGN END ===== */'
cur = cs.call('cs_get_option', name='x_custom_styles')['value'] or ''
if not os.path.exists('x_custom_styles.orig.css'):
    open('x_custom_styles.orig.css', 'w').write(cur)
if MARK in cur:
    cur = cur[:cur.index(MARK)].rstrip()
new = cur + '\n\n' + MARK + '\n' + open('lewis.css').read() + END + '\n'
r = cs.call('cs_update_option', name='x_custom_styles', value=new)
print('ok', len(new))
