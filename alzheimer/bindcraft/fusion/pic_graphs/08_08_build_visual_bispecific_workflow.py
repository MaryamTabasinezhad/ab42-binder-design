#!/usr/bin/env python3
"""Visual general bispecific workflow. Reuses existing project vector/OOXML helpers.
Run with existing Pillow/pycairo; no inference or external assets.
"""
from pathlib import Path
import subprocess,zipfile,math
import cairo
from xml.sax.saxutils import escape as esc
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
W,H=2400,1350;S=5080
NAVY='17324D';BLUE='0072B2';TEAL='008577';ORANGE='D55E00';MUTED='617588';LIGHT='E3EAF1';BG='F5F7FA';WHITE='FFFFFF'
A='http://schemas.openxmlformats.org/drawingml/2006/main';N='http://schemas.openxmlformats.org/presentationml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
im=Image.new('RGB',(W,H),'#'+BG);d=ImageDraw.Draw(im);parts=[];idx=1
# Journal-neutral full-width export: 180 mm wide, with live vector text/lines.
PDF_WIDTH_PT=180/25.4*72
pdf_surface=cairo.PDFSurface(str(P/'08_08_visual_bispecific_workflow.pdf'),PDF_WIDTH_PT,PDF_WIDTH_PT*H/W)
ctx=cairo.Context(pdf_surface);ctx.scale(PDF_WIDTH_PT/W,PDF_WIDTH_PT/W)
def ink(c):ctx.set_source_rgb(*(int(c[i:i+2],16)/255 for i in (0,2,4)))
text_sizes=[]
fonts={b:subprocess.check_output(['fc-match','-f','%{file}','Liberation Sans:style='+('Bold' if b else 'Regular')],text=True).strip() for b in [0,1]}
def f(n,b=0):return ImageFont.truetype(fonts[b],n)
def solid(c):return f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
def shape(x,y,w,h,color=WHITE,geom='roundRect',stroke=None):
 global idx
 idx+=1
 if geom=='ellipse':d.ellipse((x,y,x+w,y+h),fill='#'+color,outline='#'+stroke if stroke else None,width=2)
 else:d.rounded_rectangle((x,y,x+w,y+h),radius=18 if geom=='roundRect' else 0,fill='#'+color,outline='#'+stroke if stroke else None,width=2)
 ctx.new_path()
 if geom=='ellipse':
  ctx.save();ctx.translate(x+w/2,y+h/2);ctx.scale(w/2,h/2);ctx.arc(0,0,1,0,2*math.pi);ctx.restore()
 else:ctx.rectangle(x,y,w,h)
 ink(color);ctx.fill_preserve()
 if stroke:ink(stroke);ctx.set_line_width(2);ctx.stroke()
 else:ctx.new_path()
 ln=f'<a:ln w="12700">{solid(stroke)}</a:ln>' if stroke else '<a:ln><a:noFill/></a:ln>'
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="Editable shape {idx}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*S)}" y="{int(y*S)}"/><a:ext cx="{int(w*S)}" cy="{int(h*S)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{solid(color)}{ln}</p:spPr></p:sp>')
def text(x,y,s,n=32,c=NAVY,b=0,w=None,align='left'):
 global idx
 idx+=1
 n=max(n,33)
 width=w or d.textlength(s,font=f(n,b))+8
 while d.textlength(s,font=f(n,b))>width and n>20:n-=1
 if align=='center':px=x+(width-d.textlength(s,font=f(n,b)))/2
 else:px=x
 assert d.textlength(s,font=f(n,b))<=width+1,(s,width)
 d.text((px,y),s,font=f(n,b),fill='#'+c)
 text_sizes.append(n*PDF_WIDTH_PT/W)
 ctx.select_font_face('Liberation Sans',cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD if b else cairo.FONT_WEIGHT_NORMAL)
 ctx.set_font_size(n);ink(c)
 ctx.move_to(px,y+ctx.font_extents()[0]);ctx.show_text(s)
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="{esc(s)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*S)}" y="{int(y*S)}"/><a:ext cx="{int(width*S)}" cy="{int(n*1.5*S)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" rIns="0" tIns="0" bIns="0"/><a:lstStyle/><a:p><a:pPr algn="{"ctr" if align=="center" else "l"}"/><a:r><a:rPr sz="{n*40}" b="{b}" lang="en-US">{solid(c)}<a:latin typeface="Arial"/></a:rPr><a:t>{esc(s)}</a:t></a:r></a:p></p:txBody></p:sp>')
def path(points,c=MUTED,width=5):
 global idx
 idx+=1;d.line(points,fill='#'+c,width=round(width),joint='curve')
 ctx.new_path();ctx.move_to(*points[0])
 for pt in points[1:]:ctx.line_to(*pt)
 ink(c);ctx.set_line_width(width);ctx.set_line_join(cairo.LINE_JOIN_ROUND);ctx.set_line_cap(cairo.LINE_CAP_ROUND);ctx.stroke()
 xmin=min(x for x,y in points);ymin=min(y for x,y in points);w=max(max(x for x,y in points)-xmin,1);h=max(max(y for x,y in points)-ymin,1)
 coords=[(int((x-xmin)*S),int((y-ymin)*S)) for x,y in points]
 cmds=f'<a:moveTo><a:pt x="{coords[0][0]}" y="{coords[0][1]}"/></a:moveTo>'+''.join(f'<a:lnTo><a:pt x="{x}" y="{y}"/></a:lnTo>' for x,y in coords[1:])
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="Editable vector {idx}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(xmin*S)}" y="{int(ymin*S)}"/><a:ext cx="{int(w*S)}" cy="{int(h*S)}"/></a:xfrm><a:custGeom><a:avLst/><a:gdLst/><a:ahLst/><a:cxnLst/><a:rect l="0" t="0" r="r" b="b"/><a:pathLst><a:path w="{int(w*S)}" h="{int(h*S)}" fill="none">{cmds}</a:path></a:pathLst></a:custGeom><a:noFill/><a:ln w="{int(width*S)}" cap="rnd">{solid(c)}</a:ln></p:spPr></p:sp>')
def arrow(x1,y1,x2,y2,c=MUTED,width=5):
 path([(x1,y1),(x2,y2)],c,width)
 theta=math.atan2(y2-y1,x2-x1)
 path([(x2-15*math.cos(theta-.6),y2-15*math.sin(theta-.6)),(x2,y2),(x2-15*math.cos(theta+.6),y2-15*math.sin(theta+.6))],c,width)
def ribbon(cx,cy,c,scale=1):
 pts=[(cx+scale*(i*4-70),cy+scale*(23*math.sin(i*.45)+i*.8)) for i in range(36)]
 path(pts,c,max(3,int(10*scale)))
def blob(cx,cy,c):
 for dx,dy,r in [(-37,-10,32),(5,-33,37),(34,4,31),(-6,30,37)]:shape(cx+dx-r,cy+dy-r,r*2,r*2,c,'ellipse')
def antibody(cx,cy,scale=1):
 path([(cx,cy+65*scale),(cx,cy),(cx-60*scale,cy-60*scale)],BLUE,int(16*scale))
 path([(cx,cy),(cx+60*scale,cy-60*scale)],TEAL,int(16*scale))
 for dx,c in [(-60,BLUE),(60,TEAL)]:shape(cx+dx*scale-11*scale,cy-70*scale,22*scale,22*scale,c,'ellipse')
PURPLE='8056A8';PALE_BLUE='E2EFF8';PALE_PURPLE='EEE7F5';GREEN_PALE='E8F4F0'
def label(cx,y,s,n=34,c=NAVY,b=0,w=540):text(cx-w/2,y,s,n,c,b,w=w,align='center')
def disk(cx,cy,r,c,stroke=None):shape(cx-r,cy-r,2*r,2*r,c,'ellipse',stroke)
def helix(cx,cy,col,scale=1):
 for off,flip in [(-25,1),(0,-1),(25,1)]:
  pts=[(cx+scale*(off+8*math.sin(i*.5)),cy+scale*(i*2.4-48)*flip) for i in range(41)]
  path(pts,col,max(3,round(7*scale)))
 path([(cx-25*scale,cy+48*scale),(cx-13*scale,cy+62*scale),(cx,cy+48*scale)],col,4)
 path([(cx,cy-48*scale),(cx+13*scale,cy-62*scale),(cx+25*scale,cy-48*scale)],col,4)
def target(cx,cy,col,fill,tag=None,scale=1,side=1):
 # Lobed generic molecular surface: colored patch defines a selected epitope.
 for dx,dy,r in [(-22,-12,36),(19,-22,35),(30,18,30),(-8,29,35)]:disk(cx+dx*scale,cy+dy*scale,r*scale,fill)
 disk(cx+side*38*scale,cy-13*scale,13*scale,col)
 if tag:label(cx,cy+70*scale,tag,33,col,1,w=160)
def fab(cx,cy,col,scale=1):
 # Two-chain Fab glyph; no Fc implied.
 for dx,shift in [(-13,0),(13,6)]:
  shape(cx+(dx-11)*scale,cy-47*scale,22*scale,40*scale,col,'ellipse')
  shape(cx+(dx-11)*scale,cy+shift,22*scale,42*scale,'C7D1DA','ellipse')
 path([(cx-10*scale,cy-5*scale),(cx+10*scale,cy-5*scale)],MUTED,3)
def igg(cx,cy,scale=1):
 # Central neutral Fc + two distinct Fab arms; colors denote binding specificities.
 for dx in [-9,9]:path([(cx+dx*scale,cy+62*scale),(cx+dx*scale,cy+5*scale)],'8A9BAA',12*scale)
 path([(cx,cy+5*scale),(cx-65*scale,cy-55*scale)],BLUE,13*scale)
 path([(cx,cy+5*scale),(cx+65*scale,cy-55*scale)],PURPLE,13*scale)
 path([(cx-14*scale,cy+8*scale),(cx-78*scale,cy-45*scale)],BLUE,7*scale)
 path([(cx+14*scale,cy+8*scale),(cx+78*scale,cy-45*scale)],PURPLE,7*scale)
def curve(cx,cy,w=160,h=65,col=TEAL,kind='spr'):
 path([(cx,cy-h),(cx,cy),(cx+w,cy)],MUTED,2)
 if kind=='spr':
  points=[(cx+i*w/70,cy-h*(0 if i<10 else .8*(1-math.exp(-(i-10)/8)) if i<47 else .79*math.exp(-(i-47)/60))) for i in range(71)]
 else:points=[(cx+i*w/70,cy-h*.9*math.exp(-((i-34)/8)**2)) for i in range(71)]
 path(points,col,4)
def check(cx,cy):path([(cx-16,cy),(cx-3,cy+13),(cx+22,cy-18)],TEAL,6)
shape(0,0,W,H,WHITE,'rect')
text(75,38,'De novo design of bispecific proteins',64,NAVY,1)
text(78,124,'Proposed workflow  |  Miniprotein binders, VHHs and antibodies',35,MUTED)
path([(75,193),(2325,193)],LIGHT,2)
text(78,220,'A   DISCOVER EACH ARM',34,NAVY,1)
disk(1530,243,8,BLUE);text(1550,221,'Arm A',33,BLUE,1)
disk(1750,243,8,PURPLE);text(1770,221,'Arm B',33,PURPLE,1)
text(1975,221,'Repeat per target',33,MUTED)
xs=[330,910,1490,2070]
for cx,num,title in zip(xs,['1','2','3','4'],['Define epitopes','Generate arms','Reassess complexes','Select + test arms']):
 label(cx,292,num+'  '+title,36,NAVY,1,w=550)
# 1: two actual objects with distinct epitope patches, not paragraphs.
target(235,436,BLUE,PALE_BLUE,'A');target(425,436,PURPLE,PALE_PURPLE,'B')
label(330,570,'Structure · accessibility',33,MUTED)
label(330,614,'Native target context',33,MUTED)
# 2: modality-specific generation routes are alternatives, not a serial tool chain.
helix(805,410,BLUE,.8);helix(855,437,PURPLE,.65)
fab(1000,420,BLUE,.95);shape(1041,391,38,65,PURPLE,'ellipse')
label(910,516,'RFdiffusion → ProteinMPNN',33,NAVY,w=565)
label(910,563,'or BindCraft',33,MUTED)
label(1030,475,'Fab / VHH',33,MUTED,w=250)
label(910,614,'RFantibody (antibody route)',33,NAVY,w=565)
# 3: target/binder interface plus a confidence matrix glyph (no quantitative values).
target(1410,437,BLUE,PALE_BLUE,scale=.9);helix(1480,417,BLUE,.63)
for i in range(5):
 for j in range(5):
  c='4D99C7' if abs(i-j)<2 else 'D5E6F1'
  shape(1570+i*19,391+j*19,16,16,c,'rect')
label(1490,570,'AlphaFold2-Multimer / AF3',33,NAVY,w=565)
label(1490,614,'Fold · interface · epitope',33,MUTED)
# 4: retain diversity; early arm binding is distinct from computational confidence.
for xx,yy,col in [(1960,389,BLUE),(2020,389,PURPLE),(2080,389,BLUE),(2140,389,PURPLE)]:disk(xx,yy,10,col)
path([(1930,413),(2170,413),(2118,466),(1982,466),(1930,413)],MUTED,3)
helix(2020,508,BLUE,.38);helix(2100,508,PURPLE,.38)
check(2190,508)
label(2070,570,'Diversity · developability',33,MUTED)
label(2070,614,'Binding + specificity',33,TEAL,1)
for i in range(3):arrow(xs[i]+225,450,xs[i+1]-225,450,MUTED,4)
# Narrow inter-panel band connects the numbered serpentine route.
path([(75,688),(2325,688)],LIGHT,2)
text(78,724,'B   ENGINEER AND VALIDATE',34,NAVY,1)
text(1450,724,'Selected arms A + B',33,MUTED)
arrow(2070,661,2070,796,MUTED,4)
for cx,num,title in zip(xs,['8','7','6','5'],['Test dual function','Produce + QC','Assess construct','Combine arms']):
 label(cx,815,num+'  '+title,36,NAVY,1,w=550)
# 5: two alternative architectures: linked domains and asymmetric IgG.
helix(1953,969,BLUE,.7);helix(2050,969,PURPLE,.7)
path([(1953,1005),(1980,1030),(2000,1010),(2025,1030),(2050,1005)],MUTED,4)
igg(2200,983,.82)
label(1980,1064,'Tandem',33,MUTED,w=250);label(2200,1064,'IgG-like',33,MUTED,w=250)
label(2070,1135,'Linker · order · valency',33,NAVY)
label(2070,1180,'IgG: chain pairing',33,MUTED)
# 6: simultaneous-accessibility hypothesis: one binder linked to each target.
target(1360,951,BLUE,PALE_BLUE,scale=.8)
target(1615,951,PURPLE,PALE_PURPLE,scale=.8,side=-1)
helix(1430,970,BLUE,.53);helix(1544,970,PURPLE,.53)
path([(1430,1001),(1466,1025),(1505,1009),(1544,1001)],MUTED,4)
label(1490,1135,'AlphaFold2 / AF3',33,NAVY)
label(1490,1180,'Clashes · target access',33,MUTED)
# 7: sample tube and qualitative SEC trace; no implied experimental result.
path([(790,908),(790,1015),(800,1040),(842,1040),(852,1015),(852,908)],MUTED,4)
shape(785,895,72,17,'BFCAD3','rect')
shape(797,971,48,42,GREEN_PALE,'rect');path([(797,971),(845,971)],TEAL,3)
curve(910,1040,170,100,TEAL,'sec')
label(910,1135,'Expression · purification',33,TEAL)
label(910,1180,'SEC–MALS · stability',33,MUTED)
# 8: dual-target assay schematic and functional cell readout.
target(215,925,BLUE,PALE_BLUE,scale=.58);target(390,925,PURPLE,PALE_PURPLE,scale=.58,side=-1)
helix(267,960,BLUE,.36);helix(337,960,PURPLE,.36)
path([(267,983),(291,998),(314,990),(337,983)],MUTED,3)
curve(220,1092,160,65,TEAL)
disk(460,1028,40,GREEN_PALE,TEAL);check(460,1028)
label(330,1135,'SPR / BLI · simultaneous binding',33,TEAL,w=565)
label(330,1180,'Specificity · cellular function',33,MUTED)
for i in [3,2,1]:arrow(xs[i]-225,982,xs[i-1]+225,982,MUTED,4)
# Feedback is a single thin connector, not another text box.
path([(330,1225),(330,1265),(2070,1265)],TEAL,3)
arrow(2070,1265,2070,1225,TEAL,3)
shape(870,1236,660,60,WHITE,'rect');label(1200,1242,'Assay-guided redesign',33,TEAL,1,w=650)
text(78,1303,'Conceptual schematics; curves illustrate assays, not measured results.',33,MUTED)
text(1595,1303,'Green: experimental assessment',33,TEAL)
pdf_surface.finish()
assert min(text_sizes)>=7.0,min(text_sizes)
subprocess.run(['pdftoppm','-scale-to-x',str(W),'-scale-to-y',str(H),'-singlefile','-png',str(P/'08_08_visual_bispecific_workflow.pdf'),str(P/'08_08_visual_bispecific_workflow')],check=True)
with Image.open(P/'08_08_visual_bispecific_workflow.png') as preview:preview.save(P/'08_08_visual_bispecific_workflow.png',dpi=(W/(180/25.4),W/(180/25.4)))
with zipfile.ZipFile(P/'08_03_alzheimer_bispecific_interview_slide.pptx') as z:
 files={n:z.read(n) for n in z.namelist() if not n.startswith('ppt/media/')}
files['ppt/slides/slide1.xml']=f'<p:sld xmlns:p="{N}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{"".join(parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
files['ppt/slides/_rels/slide1.xml.rels']=f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>'
with zipfile.ZipFile(P/'08_08_visual_bispecific_workflow_editable.pptx','w',zipfile.ZIP_DEFLATED) as z:
 for name,value in files.items():z.writestr(name,value)
print('Saved PNG, vector PDF and native editable PPTX; minimum type:',round(min(text_sizes),2),'pt at 180 mm.')
