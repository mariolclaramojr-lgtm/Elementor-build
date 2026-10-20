"""Square (1:1) copies of the photos used in round Image elements, so the circle comes from the
element's own Border Radius setting (no aspect-ratio CSS). Results cached in square_images.json."""
import json,os,io,base64,sys,time,urllib.request
sys.path.insert(0,os.environ['MCPDIR']); from lib import call
from PIL import Image
CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'square_images.json')
_m=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def sq(url,size=1000):
    if url in _m: return _m[url]
    for attempt in range(5):
        try: raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read(); break
        except Exception:
            if attempt==4: raise
            time.sleep(2**attempt)
    im=Image.open(io.BytesIO(raw)).convert('RGB'); w,h=im.size; s=min(w,h)
    im=im.crop(((w-s)//2,(h-s)//3 if h>w else 0,(w-s)//2+s,((h-s)//3 if h>w else 0)+s)).resize((size,size),Image.LANCZOS)
    buf=io.BytesIO(); im.save(buf,'JPEG',quality=84,optimize=True,progressive=True)
    name=os.path.splitext(url.rsplit('/',1)[1])[0].replace('-scaled','')+'-sq.jpg'
    r=call('cs_upload_media',{'base64':base64.b64encode(buf.getvalue()).decode(),'filename':name,'title':name},timeout=180)
    _m[url]=r['url']; json.dump(_m,open(CACHE,'w'),indent=1); return r['url']
