import cs, json, re, os, base64, subprocess, glob, sys
S=os.path.dirname(os.path.abspath(__file__))+'/..'
D=S+'/design/lewis-redesign 6'
cache_f='media.json'
cache=json.load(open(cache_f)) if os.path.exists(cache_f) else {}
urls={}
for f in glob.glob(D+'/*.html'):
    t=open(f).read()
    for m in re.finditer(r'https://images\.unsplash\.com/(photo-[0-9a-f-]+)\?[^"\')\s]*',t):
        # alt
        urls[m.group(1)]=None
    for m in re.finditer(r'<img src="https://images\.unsplash\.com/(photo-[0-9a-f-]+)[^"]*" alt="([^"]*)"',t):
        urls[m.group(1)]=m.group(2)
for pid,alt in urls.items():
    if pid in cache: continue
    fn=S+'/img/'+pid+'.jpg'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sSL','-o',fn,f'https://images.unsplash.com/{pid}?w=2000&q=78&fm=jpg&fit=crop'],check=True)
    b=base64.b64encode(open(fn,'rb').read()).decode()
    r=cs.call('cs_upload_media',base64=b,filename='lewis-'+pid+'.jpg',alt=alt or '',title='Lewis '+pid)
    cache[pid]={'id':r.get('id'),'url':r.get('url')}
    json.dump(cache,open(cache_f,'w'),indent=1); print(pid,cache[pid])
for name in ['hero.mp4','welcome.mp4','hero-poster.jpg','welcome-poster.jpg','hero.webm','welcome.webm']:
    if name in cache: continue
    b=base64.b64encode(open(D+'/'+name,'rb').read()).decode()
    try:
        r=cs.call('cs_upload_media',base64=b,filename='lewis-'+name,title='Lewis '+name)
        cache[name]={'id':r.get('id'),'url':r.get('url')}
    except Exception as e:
        print('fail',name,e); continue
    json.dump(cache,open(cache_f,'w'),indent=1); print(name,cache[name])
