#!/usr/bin/env python3
"""Build a single 16:9 slide and plots from committed Stage 8 data; Pillow only."""
import csv, json, statistics, zipfile, subprocess
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageDraw, ImageFont

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
rows=list(csv.DictReader((BASE/'stage8_results_merged.csv').open()))
assert len(rows)==len({r['id'] for r in rows})==250
for r in rows:
    for k in ['arm1_plddt','arm2_plddt','inter_domain_pae','ptm']:
        r[k]=float(r[k])
    r['pass']=r['arm1_plddt']>80 and r['arm2_plddt']>80 and r['inter_domain_pae']>15
    assert r['pass']==(r['pass_all'].lower()=='true')
assert sum(r['pass'] for r in rows)==183
# Arm numbers are sequence positions; map both orientations to target identities.
manifest={r['id']:r for r in csv.DictReader((BASE/'inputs/fusion_manifest.csv').open())}
for r in rows:
    m=manifest[r['id']]
    assert r['domain_order']==m['domain_order']
    assert m['domain_order'] in ('ab-tfr1','tfr1-ab')
    ab_first=m['domain_order']=='ab-tfr1'
    assert m['arm1_id']==m['ab42_design' if ab_first else 'tfr1_design']
    assert m['arm2_id']==m['tfr1_design' if ab_first else 'ab42_design']
    r['ab42_plddt']=r['arm1_plddt' if ab_first else 'arm2_plddt']
    r['tfr1_plddt']=r['arm2_plddt' if ab_first else 'arm1_plddt']
# Verify pooled split metrics, preferring populated rows.
pooled={}
for split in ['splitA','splitB']:
    for r in csv.DictReader((BASE/f'stage8_results_{split}.csv').open()):
        if r['arm1_plddt']: pooled[r['id']]=r
assert len(pooled)==250
assert all(all(float(pooled[r['id']][k])==r[k] for k in ['arm1_plddt','arm2_plddt','inter_domain_pae','ptm']) for r in rows)

NAVY='#102B46'; TEAL='#0072B2'; GRAY='#D55E00'; TEXT='#263E53'; MUTED='#546B7E'; BG='#F3F6FA'; WHITE='#FFFFFF'; LINE='#DAE3EC'; GOLD='#F0B44B'
# Liberation Sans is an Arial-compatible conventional presentation font.
FONT_PATHS={bold:subprocess.check_output(['fc-match','-f','%{file}', 'Liberation Sans:style='+('Bold' if bold else 'Regular')],text=True).strip() for bold in (False,True)}
def font(n,bold=False): return ImageFont.truetype(FONT_PATHS[bold],n)
def txt(d,xy,s,n=24,fill=TEXT,bold=False): d.text(xy,s,font=font(n,bold),fill=fill)
def chart(kind):
    im=Image.new('RGB',(1040,570),WHITE);d=ImageDraw.Draw(im)
    x0,y0,x1,y1=105,70,990,455
    if kind=='arms':
        xmin,xmax,ymin,ymax=30,100,30,100
        title='Per-arm folding confidence across fusion designs'
        xlabel='TfR1 arm mean pLDDT'; ylabel='Aβ42 arm mean pLDDT'
        xticks=yticks=[30,40,50,60,70,80,90,100]
    else:
        xmin,xmax,ymin,ymax=0.4,0.75,0,30
        title='Whole-chain confidence vs. domain independence'
        xlabel='Fusion pTM (informational; not a gate)';ylabel='Inter-domain PAE (Å)'
        xticks=[.4,.45,.5,.55,.6,.65,.7,.75];yticks=[0,5,10,15,20,25,30]
    X=lambda v:x0+(v-xmin)/(xmax-xmin)*(x1-x0)
    Y=lambda v:y1-(v-ymin)/(ymax-ymin)*(y1-y0)
    txt(d,(35,8),title,27,bold=True)
    if kind=='arms': d.rectangle((X(80),Y(100),X(100),Y(80)),fill='#EFF6FB')
    else: d.rectangle((x0,Y(30),x1,Y(15)),fill='#EFF6FB')
    for v in xticks:
        d.line((X(v),y0,X(v),y1),fill=LINE,width=1)
        label=f'{v:g}';txt(d,(X(v)-15,y1+12),label,22,fill=MUTED)
    for v in yticks:
        d.line((x0,Y(v),x1,Y(v)),fill=LINE,width=1)
        txt(d,(x0-47,Y(v)-14),str(v),22,fill=MUTED)
    def dash(xa,ya,xb,yb):
        dist=((xb-xa)**2+(yb-ya)**2)**.5
        for i in range(0,int(dist),16):
            t=i/dist;u=min((i+9)/dist,1)
            d.line((xa+(xb-xa)*t,ya+(yb-ya)*t,xa+(xb-xa)*u,ya+(yb-ya)*u),fill='#607587',width=3)
    if kind=='arms':
        dash(X(80),y0,X(80),y1);dash(x0,Y(80),x1,Y(80))
    else: dash(x0,Y(15),x1,Y(15))
    for r in sorted(rows,key=lambda r:r['pass']):
        x,y=(r['tfr1_plddt'],r['ab42_plddt']) if kind=='arms' else (r['ptm'],r['inter_domain_pae'])
        assert xmin<=x<=xmax and ymin<=y<=ymax,(kind,x,y)
        xx,yy=X(x),Y(y);c=TEAL if r['pass'] else GRAY
        d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=c,outline=WHITE,width=1)
    d.line((x0,y0,x0,y1,x1,y1),fill=MUTED,width=2)
    txt(d,(235,y1+53),xlabel,24)
    label=Image.new('RGB',(410,35),WHITE);ld=ImageDraw.Draw(label);txt(ld,(0,0),ylabel,24)
    label=label.rotate(90,expand=True);im.paste(label,(8,78))
    return im

arms=chart('arms');conf=chart('confidence')
arms.save(OUT/'08_01_fusion_arm_confidence.png',dpi=(180,180))
conf.save(OUT/'08_02_fusion_ptm_interdomain_pae.png',dpi=(180,180))
W,H=2400,1350
im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
d.rectangle((0,0,W,207),fill=WHITE)
txt(d,(72,30),'CURRENT RESEARCH  /  COMPUTATIONAL PROTEIN DESIGN',24,fill=TEAL,bold=True)
txt(d,(72,75),'AI-designed bispecific binders for Alzheimer’s disease',58,fill=NAVY,bold=True)
txt(d,(74,151),'Aβ42 targeting × transferrin receptor 1 (TfR1)  |  Goal: receptor-mediated delivery across the BBB',30,fill=MUTED)
# Reported exploration counts are trajectories, not accepted sequences.
txt(d,(74,201),'PRE-FILTER EXPLORATION (reported trajectories):  Aβ42  1,342   |   TfR1 / BBB arm  2,051',25,fill=TEXT,bold=True)
# End-to-end workstream.
cards=[('01  TARGET PREPARATION','Structure-guided epitopes','Aβ42: 9CO4  •  TfR1: 6WRV'),('02  DE NOVO DESIGN','BindCraft + ProteinMPNN','Generate, redesign, AF2-score'),('03  FILTER & RANK','Stability + developability','23 Aβ42 / 224 TfR1 retained'),('04  FUSION LIBRARY','5 Aβ42 × 5 TfR1 binders','5 linkers × 2 domain orders'),('05  FOLD & SCREEN','AlphaFold2 / ColabFold','250 fusion predictions scored')]
for i,(a,b,c) in enumerate(cards):
    x=72+i*455
    d.rounded_rectangle((x,238,x+434,394),radius=14,fill=WHITE)
    txt(d,(x+19,257),a,22,fill=TEAL,bold=True)
    txt(d,(x+19,300),b,24,bold=True)
    txt(d,(x+19,345),c,21,fill=MUTED)
# Three outcome cards.
for x,num,label,detail in [(72,'442','accepted arm designs','62 Aβ42 + 380 TfR1 (reported)'),(838,'250','fusion designs modeled','25 binder pairs × 10 variants'),(1604,'183 / 250','pass Stage 8 gates','73.2% computational pass rate')]:
    d.rounded_rectangle((x,420,x+724,575),radius=14,fill=TEAL if x==1604 else WHITE)
    fg=WHITE if x==1604 else NAVY
    txt(d,(x+24,432),num,53,fg,True)
    txt(d,(x+24,497),label,27,fg,True)
    txt(d,(x+24,540),detail,21,'#D7F2EE' if x==1604 else MUTED)
txt(d,(74,593),'FUSION-LEVEL COMPARISON  •  All 250 designs; one top-ranked prediction per design',24,bold=True)
for x,c in [(76,TEAL),(448,GRAY)]: d.ellipse((x,638,x+16,654),fill=c)
txt(d,(103,630),'Pass all gates (n = 183)',22)
txt(d,(476,630),'Fail ≥1 gate (n = 67)',22)
txt(d,(1608,630),'Dashed lines: required thresholds',22,fill=MUTED)
im.paste(arms.resize((1100,550)),(62,674));im.paste(conf.resize((1100,550)),(1238,674))
# crop chart whitespace at bottom leaves footer position deliberately aligned.
d=ImageDraw.Draw(im)
d.rectangle((0,1230,W,H),fill='#E7EEF4')
txt(d,(73,1242),'Gate: both arms pLDDT >80 AND inter-domain PAE >15 Å. High inter-domain PAE reflects uncertain relative orientation.',24,TEXT)
im.save(OUT/'08_03_alzheimer_bispecific_interview_slide.png',dpi=(180,180))
im.save(OUT/'08_03_alzheimer_bispecific_interview_slide.pdf','PDF',resolution=180)
# Standards-based single-slide PPTX, with embedded high-resolution slide image.
ns='http://schemas.openxmlformats.org/presentationml/2006/main';a='http://schemas.openxmlformats.org/drawingml/2006/main';rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
slide=f'''<p:sld xmlns:p="{ns}" xmlns:a="{a}" xmlns:r="{rel}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:pic><p:nvPicPr><p:cNvPr id="2" name="Interview slide" descr="AI-designed bispecific Aβ42–TfR1 binders: 442 accepted arm designs, 250 fusion predictions, 183 pass Stage 8 computational gates."/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''
rels=lambda entries:'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="{i}" Type="{rel}/{t}" Target="{p}"/>' for i,t,p in entries)+'</Relationships>'
files={
'[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>',
'_rels/.rels':rels([('rId1','officeDocument','ppt/presentation.xml')]),
'ppt/presentation.xml':f'<p:presentation xmlns:p="{ns}" xmlns:r="{rel}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId2"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>',
'ppt/_rels/presentation.xml.rels':rels([('rId1','slide','slides/slide1.xml'),('rId2','slideMaster','slideMasters/slideMaster1.xml')]),
'ppt/slides/slide1.xml':slide,
'ppt/slides/_rels/slide1.xml.rels':rels([('rId1','image','../media/slide.png'),('rId2','slideLayout','../slideLayouts/slideLayout1.xml')])}
empty_tree='<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree>'
files['ppt/slideMasters/slideMaster1.xml']=f'<p:sldMaster xmlns:p="{ns}" xmlns:a="{a}" xmlns:r="{rel}"><p:cSld>{empty_tree}</p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles/></p:sldMaster>'
files['ppt/slideMasters/_rels/slideMaster1.xml.rels']=rels([('rId1','slideLayout','../slideLayouts/slideLayout1.xml')])
files['ppt/slideLayouts/slideLayout1.xml']=f'<p:sldLayout xmlns:p="{ns}" xmlns:a="{a}" xmlns:r="{rel}" type="blank" preserve="1"><p:cSld name="Blank">{empty_tree}</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'
files['ppt/slideLayouts/_rels/slideLayout1.xml.rels']=rels([('rId1','slideMaster','../slideMasters/slideMaster1.xml')])
files['[Content_Types].xml']=files['[Content_Types].xml'].replace('</Types>','<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/></Types>')
with zipfile.ZipFile(OUT/'08_03_alzheimer_bispecific_interview_slide.pptx','w',zipfile.ZIP_DEFLATED) as z:
    for p,v in files.items():z.writestr(p,v)
    z.write(OUT/'08_03_alzheimer_bispecific_interview_slide.png','ppt/media/slide.png')
with (OUT/'08_04_fusion_plot_data.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['id','domain_order','arm1_plddt','arm2_plddt','tfr1_plddt','ab42_plddt','inter_domain_pae','ptm','pass_all'],lineterminator='\n');w.writeheader()
    for r in rows:w.writerow({k:r[k] for k in w.fieldnames})
summary={'predicted_fusions':len(rows),'pass_all':sum(r['pass'] for r in rows),'accepted_arm_library_reported':{'ab42':62,'tfr1':380},'pre_filter_trajectories_reported':{'ab42':1342,'tfr1':2051},'left_plot_axes':{'x':'tfr1_plddt','y':'ab42_plddt'},'pass_rate_percent':73.2,'passing_medians':{k:statistics.median(r[k] for r in rows if r['pass']) for k in ['arm1_plddt','arm2_plddt','inter_domain_pae','ptm']}}
(OUT/'08_04_slide_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
