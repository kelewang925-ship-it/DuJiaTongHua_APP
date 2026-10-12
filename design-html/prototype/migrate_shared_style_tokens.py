"""Exact-value semantic token migration; leaves original inline artwork CSS untouched."""
import json,re,sys,hashlib
from pathlib import Path
from verify_pet_controls import ROOT,DEMO

NEW={'--prototype-font-family':'Fairy,serif','--prototype-control-compact':'40px','--prototype-paper-warm':'#fffaf0','--prototype-ink-warm':'#66432d','--prototype-border-warm':'#edd0b8','--prototype-button-primary':'#f6bec8','--prototype-button-secondary':'#f5eae6','--prototype-tag-paper':'#f9e7d3','--prototype-tag-border':'#dfb99a','--prototype-tag-ink':'#583a26','--prototype-loading-base':'#ede2dc','--prototype-toast-error':'#854d48','--prototype-overlay':'#4a363680','--prototype-motion-feedback':'120ms','--prototype-motion-fade':'160ms','--prototype-motion-spin':'900ms'}
COLORS={'#fdfbf7':'--prototype-paper','#6b4f4f':'--prototype-ink','#d4bdb6':'--prototype-border',**{v:k for k,v in NEW.items()if v.startswith('#')}}
SPACES={str(v)+'px':'--prototype-space-'+k for k,v in [('xs',4),('sm',8),('md',12),('lg',16),('xl',24),('xxl',32)]}
FONTS={'14px':'--prototype-font-note','16px':'--prototype-font-body','20px':'--prototype-font-title'}
RADII={'8px':'--prototype-radius-sm','12px':'--prototype-radius-md','20px':'--prototype-radius'}
TIMES={'120ms':'--prototype-motion-feedback','160ms':'--prototype-motion-fade','220ms':'--prototype-motion-enter','900ms':'--prototype-motion-spin'}
def replace_units(value,table):return re.sub(r'(?<![\w.-])(?:'+ '|'.join(re.escape(v)for v in table)+r')\b',lambda m:'var('+table[m[0]]+')',value)
def tokens(prop,value):
    result=value
    if prop in ['padding','padding-top','padding-bottom','padding-left','padding-right','margin','margin-top','margin-bottom','margin-left','margin-right','gap','row-gap','column-gap']:result=replace_units(result,SPACES)
    elif prop=='border-radius':result=replace_units(result,RADII)
    elif prop in ['font','font-size']:result=replace_units(result,FONTS)
    if prop in ['font','font-family']:result=re.sub(r'\bFairy,\s*serif', 'var(--prototype-font-family)',result)
    if prop in ['min-height','min-width']and value.strip()in ['40px','44px','48px']:
        result=result.replace(value.strip(),'var('+{'40px':'--prototype-control-compact','44px':'--prototype-touch','48px':'--prototype-control-height'}[value.strip()]+')')
    if prop in ['color','background','background-color','border','border-top','border-bottom','border-left','border-right','border-color','outline-color']:
        if prop!='background'or value.strip().lower()in COLORS:
            result=re.sub(r'#[0-9a-fA-F]{3,8}\b',lambda m:'var('+COLORS[m[0].lower()]+')'if m[0].lower()in COLORS else m[0],result)
    if prop=='box-shadow'and value.strip()=='0 12px 32px #6b4f4f29':result=result.replace(value.strip(),'var(--prototype-shadow)')
    if prop in ['transition','animation','transition-duration','animation-duration']:result=replace_units(result,TIMES)
    return result

def migrate(text):
    changes=[];start=0;quote=None;comment=False;depth=0;i=0
    while i<len(text):
        ch=text[i]
        if comment:
            if text[i:i+2]=='*/':comment=False;i+=2;continue
        elif quote:
            if ch=='\\':i+=2;continue
            if ch==quote:quote=None
        elif text[i:i+2]=='/*':comment=True;i+=2;continue
        elif ch in ['"',"'"]:quote=ch
        elif ch=='(':depth+=1
        elif ch==')':depth-=1
        elif depth==0 and ch in '{;}':
            if ch!='{':
                part=text[start:i];m=re.match(r'\s*([\w-]+)\s*:(.*)',part,re.S)
                if m and not m[1].startswith('--'):
                    value=m[2];changed=tokens(m[1].lower(),value)
                    if value!=changed:changes.append(dict(start=start+m.start(2),end=i,property=m[1],before=value,after=changed))
            start=i+1
        i+=1
    result=text
    for row in reversed(changes):result=result[:row['start']]+row['after']+result[row['end']:]
    return result,changes

def main():
    apply='--apply'in sys.argv;rows=[];history=ROOT/'evidence/history/pre-shared-style-tokens-74b3eca'
    if apply and (ROOT/'evidence/current/shared-style-token-migration.json').exists():raise SystemExit('Migration already recorded; use --check. Original baseline must not be overwritten.')
    for path in sorted((DEMO/'assets').glob('prototype-*.css')):
        original_raw=path.read_bytes();original=original_raw.decode('utf-8');updated,changes=migrate(original)
        if apply:
            history.mkdir(parents=True,exist_ok=True);(history/path.name).write_bytes(path.read_bytes())
            if path.name=='prototype-components.css':updated+='\n:root{'+''.join(k+':'+v+';'for k,v in NEW.items())+'}\n'
            path.write_bytes(updated.encode('utf-8'))
        rows.append(dict(file=path.relative_to(DEMO).as_posix(),before_sha256=hashlib.sha256(original_raw).hexdigest(),changes=changes))
    if apply:(ROOT/'evidence/current/shared-style-token-migration.json').write_text(json.dumps(dict(new_tokens=NEW,files=rows,scope='Exact semantic value substitution in12 dynamic stylesheets; artwork inline CSS, positioning/cqw/gradients/themes untouched.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(stylesheets=len(rows),declarations=sum(len(r['changes'])for r in rows),new_tokens=len(NEW),applied=apply)))
    if '--check'in sys.argv:raise SystemExit(1 if any(r['changes']for r in rows)else 0)

if __name__=='__main__':main()
