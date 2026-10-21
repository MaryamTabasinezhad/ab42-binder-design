#!/usr/bin/env python3
"""Visual project overview. Reuses drawing/OOXML helpers from build_visual_workflow_slide.py.
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
pdf_surface=cairo.PDFSurface(str(P/'08_07_alzheimer_visual_overview.pdf'),PDF_WIDTH_PT,PDF_WIDTH_PT*H/W)
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
 idx+=1;d.line(points,fill='#'+c,width=width,joint='curve')
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
import csv,json
PURPLE='8056A8';FAIL='A8B1BA';PALE='F1F6FA'
rows=list(csv.DictReader((P/'08_04_fusion_plot_data.csv').open()))
assert len(rows)==250
for r in rows:
 for k in ['tfr1_plddt','ab42_plddt','inter_domain_pae','ptm']:r[k]=float(r[k])
 r['passed']=r['tfr1_plddt']>80 and r['ab42_plddt']>80 and r['inter_domain_pae']>15
 assert r['passed']==(r['pass_all']=='True')
assert sum(r['passed'] for r in rows)==183
# Compact helical glyphs are schematic, not atomic structures.
def helix(cx,cy,col,scale=1):
 for off,flip in [(-35,1),(0,-1),(35,1)]:
  pts=[(cx+scale*(off+12*math.sin(i*.45)),cy+scale*(i*3-66)*flip) for i in range(45)]
  path(pts,col,round(8*scale))
 path([(cx-35*scale,cy+66*scale),(cx-16*scale,cy+83*scale),(cx,cy+66*scale)],col,round(5*scale))
 path([(cx,cy-66*scale),(cx+17*scale,cy-81*scale),(cx+35*scale,cy-66*scale)],col,round(5*scale))
def label(cx,y,s,n=28,c=NAVY,b=0,w=500):text(cx-w/2,y,s,n,c,b,w=w,align='center')
def dash(x1,y1,x2,y2):
 dist=math.hypot(x2-x1,y2-y1)
 for k in range(0,round(dist),18):
  a=k/dist;b=min((k+10)/dist,1)
  path([(x1+(x2-x1)*a,y1+(y2-y1)*a),(x1+(x2-x1)*b,y1+(y2-y1)*b)],MUTED,2)
shape(0,0,W,H,WHITE,'rect')
text(75,40,'De novo bispecific binders for Alzheimer’s disease',62,NAVY,1)
text(78,127,'Aβ42 recognition × TfR1 targeting  |  Goal: receptor-mediated brain delivery',33,MUTED)
path([(75,190),(2325,190)],LIGHT,2)
for cx,num,name in [(320,'01','TARGETS'),(920,'02','ARM DESIGN'),(1510,'03','FUSION LIBRARY'),(2110,'04','FOLD SCREEN')]:
 label(cx,222,num+'  '+name,30,BLUE,1)
# Target A: an amyloid-like paired ribbon, a generic schematic rather than the supplied PDB.
for shift in [-15,15]:
 pts=[(220+i*4,340+shift+28*math.sin(i*.18)) for i in range(51)]
 path(pts,PURPLE,11)
for i in range(0,51,5):
 xx=220+i*4;yy=340+28*math.sin(i*.18);path([(xx,yy-15),(xx,yy+15)],PURPLE,4)
label(320,390,'Aβ42',32,PURPLE,1)
# Target B: generic membrane receptor topology, not a validated binder pose.
path([(165,580),(475,580)],LIGHT,7);path([(165,594),(475,594)],LIGHT,7)
for xx in range(170,475,20):
 shape(xx,576,9,9,'A7B7C4','ellipse');shape(xx,590,9,9,'A7B7C4','ellipse')
for xx in [288,349]:
 path([(xx,582),(xx,535),(xx-10,509)],BLUE,7)
 shape(xx-31,453,64,65,'DCECF7','ellipse',BLUE)
 shape(xx-20,511,40,30,'DCECF7','ellipse',BLUE)
label(320,611,'TfR1',32,BLUE,1)
# Arm library: two explicit tracks, conveying reported campaign counts without a paragraph.
helix(805,350,PURPLE,.68);helix(1040,350,BLUE,.68)
label(805,440,'62',58,PURPLE,1,w=200);label(1040,440,'380',58,BLUE,1,w=200)
label(920,515,'accepted arms (reported)',28,MUTED)
label(920,573,'BindCraft · ProteinMPNN',28,NAVY,1)
label(920,615,'1,342 / 2,051 trajectories',33,MUTED,w=540)
arrow(555,430,650,430,BLUE,5)
# Fusion: show the covalently linked two-domain format, not an IgG antibody.
helix(1430,365,PURPLE,.9);helix(1590,365,BLUE,.9)
path([(1430,425),(1465,460),(1500,430),(1535,460),(1590,425)],MUTED,5)
label(1510,485,'250',62,NAVY,1)
label(1510,563,'5 × 5 arm pairs',30,NAVY,1)
label(1510,610,'5 linkers × 2 domain orders',27,MUTED)
arrow(1170,430,1270,430,BLUE,5);label(1220,346,'5 + 5',33,MUTED,1,w=180)
# Donut: actual Stage 8 pass fraction, not binding success.
cx,cy,rad=2110,411,126
pts=[(cx+rad*math.cos(-math.pi/2+i*2*math.pi/200),cy+rad*math.sin(-math.pi/2+i*2*math.pi/200)) for i in range(201)]
path(pts,'E5EBF0',25)
pts=[(cx+rad*math.cos(-math.pi/2+i*(183/250)*2*math.pi/150),cy+rad*math.sin(-math.pi/2+i*(183/250)*2*math.pi/150)) for i in range(151)]
path(pts,BLUE,25)
label(cx,363,'183',72,BLUE,1,w=240);label(cx,448,'of 250',28,MUTED,w=230)
label(cx,563,'73.2% pass Stage 8',30,BLUE,1)
label(cx,610,'AlphaFold2 / ColabFold',27,MUTED)
arrow(1765,430,1875,430,BLUE,5)
path([(75,694),(2325,694)],LIGHT,2)
# Evidence panels. All 250 designs, one top-ranked prediction per design.
text(80,724,'a  Per-arm folding confidence',32,NAVY,1)
text(1280,724,'b  Whole-fusion confidence and uncertainty',32,NAVY,1)
for x,col,s in [(80,BLUE,'Pass (183)'),(330,FAIL,'Fail (67)')]:
 shape(x,783,15,15,col,'ellipse');text(x+25,773,s,25,MUTED)
text(765,773,'All 250 designs',25,MUTED)
text(1280,773,'Inter-domain PAE (Å)',27,NAVY)
text(80,823,'Aβ42 arm pLDDT',27,NAVY)
for kind,left,right,top,bottom in [('arms',175,1120,882,1155),('global',1370,2300,845,1155)]:
 if kind=='arms':xmin,xmax,ymin,ymax=30,100,30,100;xt=yt=[40,60,80,100]
 else:xmin,xmax,ymin,ymax=.4,.75,0,30;xt=[.4,.5,.6,.7];yt=[0,10,20,30]
 X=lambda v:left+(v-xmin)/(xmax-xmin)*(right-left)
 Y=lambda v:bottom-(v-ymin)/(ymax-ymin)*(bottom-top)
 if kind=='arms':shape(X(80),Y(100),X(100)-X(80),Y(80)-Y(100),PALE,'rect')
 for v in xt:
  xx=X(v);path([(xx,top),(xx,bottom)],LIGHT,1);label(xx,bottom+12,f'{v:g}',33,MUTED,w=120)
 for v in yt:
  yy=Y(v);path([(left,yy),(right,yy)],LIGHT,1);text(left-72,yy-14,f'{v:g}',23,MUTED)
 if kind=='arms':dash(X(80),top,X(80),bottom);dash(left,Y(80),right,Y(80))
 else:dash(left,Y(15),right,Y(15))
 for r in sorted(rows,key=lambda r:r['passed']):
  xv,yv=(r['tfr1_plddt'],r['ab42_plddt']) if kind=='arms' else (r['ptm'],r['inter_domain_pae'])
  xx,yy=X(xv),Y(yv);assert left<=xx<=right and top<=yy<=bottom
  shape(xx-4.8,yy-4.8,9.6,9.6,BLUE if r['passed'] else FAIL,'ellipse',WHITE)
 path([(left,top),(left,bottom),(right,bottom)],MUTED,2)
 label((left+right)/2,1205,'TfR1 arm pLDDT' if kind=='arms' else 'Fusion pTM (not a gate)',27,NAVY,1,w=750)
path([(75,1248),(2325,1248)],LIGHT,2)
text(80,1265,'Gates: both arms pLDDT >80; inter-domain PAE >15 Å. High PAE = uncertain relative placement.',33,MUTED)
text(80,1305,'Computational fold screen; dual-target binding and BBB transport remain untested. Molecular drawings are schematic.',33,MUTED)
# Existing clean master/layout package; all visible content is editable.
pdf_surface.finish()
# Render the vector scene with antialiasing rather than integer-only raster paths.
subprocess.run(['pdftoppm','-scale-to-x',str(W),'-scale-to-y',str(H),'-singlefile','-png',str(P/'08_07_alzheimer_visual_overview.pdf'),str(P/'08_07_alzheimer_visual_overview')],check=True)
with Image.open(P/'08_07_alzheimer_visual_overview.png') as preview:preview.save(P/'08_07_alzheimer_visual_overview.png',dpi=(W/(180/25.4),W/(180/25.4)))
with zipfile.ZipFile(P/'08_03_alzheimer_bispecific_interview_slide.pptx') as z:
 files={n:z.read(n) for n in z.namelist() if not n.startswith('ppt/media/')}
files['ppt/slides/slide1.xml']=f'<p:sld xmlns:p="{N}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{"".join(parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
files['ppt/slides/_rels/slide1.xml.rels']=f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>'
with zipfile.ZipFile(P/'08_07_alzheimer_visual_overview_editable.pptx','w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
print('Rendered 250 data points per panel; 183 pass; minimum print label',round(min(text_sizes),2),'pt')
