#!/usr/bin/env python3
"""One visual 16:9 workflow, rendered as PNG and native editable PPTX."""
from pathlib import Path
import subprocess,zipfile,math
from xml.sax.saxutils import escape as esc
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
W,H=2400,1350;S=5080
NAVY='17324D';BLUE='0072B2';TEAL='008577';ORANGE='D55E00';MUTED='617588';LIGHT='E3EAF1';BG='F5F7FA';WHITE='FFFFFF'
A='http://schemas.openxmlformats.org/drawingml/2006/main';N='http://schemas.openxmlformats.org/presentationml/2006/main';R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
im=Image.new('RGB',(W,H),'#'+BG);d=ImageDraw.Draw(im);parts=[];idx=1
fonts={b:subprocess.check_output(['fc-match','-f','%{file}','Liberation Sans:style='+('Bold' if b else 'Regular')],text=True).strip() for b in [0,1]}
def f(n,b=0):return ImageFont.truetype(fonts[b],n)
def solid(c):return f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>'
def shape(x,y,w,h,color=WHITE,geom='roundRect',stroke=None):
 global idx
 idx+=1
 if geom=='ellipse':d.ellipse((x,y,x+w,y+h),fill='#'+color,outline='#'+stroke if stroke else None,width=2)
 else:d.rounded_rectangle((x,y,x+w,y+h),radius=18 if geom=='roundRect' else 0,fill='#'+color,outline='#'+stroke if stroke else None,width=2)
 ln=f'<a:ln w="12700">{solid(stroke)}</a:ln>' if stroke else '<a:ln><a:noFill/></a:ln>'
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="Editable shape {idx}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*S)}" y="{int(y*S)}"/><a:ext cx="{int(w*S)}" cy="{int(h*S)}"/></a:xfrm><a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{solid(color)}{ln}</p:spPr></p:sp>')
def text(x,y,s,n=32,c=NAVY,b=0,w=None,align='left'):
 global idx
 idx+=1
 width=w or d.textlength(s,font=f(n,b))+8
 while d.textlength(s,font=f(n,b))>width and n>20:n-=1
 if align=='center':px=x+(width-d.textlength(s,font=f(n,b)))/2
 else:px=x
 assert d.textlength(s,font=f(n,b))<=width+1,(s,width)
 d.text((px,y),s,font=f(n,b),fill='#'+c)
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{idx}" name="{esc(s)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(x*S)}" y="{int(y*S)}"/><a:ext cx="{int(width*S)}" cy="{int(n*1.5*S)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="none" lIns="0" rIns="0" tIns="0" bIns="0"/><a:lstStyle/><a:p><a:pPr algn="{"ctr" if align=="center" else "l"}"/><a:r><a:rPr sz="{n*40}" b="{b}" lang="en-US">{solid(c)}<a:latin typeface="Arial"/></a:rPr><a:t>{esc(s)}</a:t></a:r></a:p></p:txBody></p:sp>')
def path(points,c=MUTED,width=5):
 global idx
 idx+=1;d.line(points,fill='#'+c,width=width,joint='curve')
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
shape(0,0,W,H,BG,'rect');shape(0,0,W,210,WHITE,'rect')
text(72,35,'FROM TARGETS TO A BISPECIFIC',26,BLUE,1)
text(72,80,'AI-designed binders & antibodies',68,NAVY,1)
text(74,163,'Design each arm  •  Choose a format  •  Test dual binding',32,MUTED)
xs=[65+380*i for i in range(6)];titles=['Targets','Design','Screen','Assemble','Predict','Validate']
for i,(x,title) in enumerate(zip(xs,titles)):
 text(x,267,f'0{i+1}',30,BLUE,1)
 text(x,310,title,44,NAVY,1)
 shape(x,385,345,690,WHITE,stroke=LIGHT)
 if i<5:arrow(x+351,730,x+374,730)
# Targets.
x=xs[0];blob(x+97,540,BLUE);blob(x+246,658,TEAL)
text(x+35,630,'A',32,BLUE,1);text(x+260,741,'B',32,TEAL,1)
text(x+24,830,'Structures + epitopes',30,NAVY,1,w=300,align='center')
text(x+24,890,'Target A / Target B',28,MUTED,w=300,align='center')
# Design alternatives.
x=xs[1]
shape(x+18,410,309,285,'EFF6FC')
ribbon(x+168,460,BLUE,.7)
text(x+28,534,'MINIPROTEIN',24,BLUE,1,w=289,align='center')
text(x+28,575,'RFdiffusion / BindCraft',28,NAVY,1,w=289,align='center')
text(x+28,620,'ProteinMPNN',29,MUTED,w=289,align='center')
text(x+28,711,'OR',23,MUTED,w=289,align='center')
shape(x+18,756,309,295,'EEF8F5')
antibody(x+170,834,.52)
text(x+28,889,'ANTIBODY / VHH',24,TEAL,1,w=289,align='center')
text(x+28,930,'RFantibody',33,NAVY,1,w=289,align='center')
text(x+28,982,'RFdiffusion-Ab · MPNN · RF2',23,MUTED,w=289,align='center')
# Screening funnel: progressively fewer candidate dots.
x=xs[2]
for row,count in enumerate([6,4,2]):
 for j in range(count):shape(x+172-(count-1)*19+j*38-10,475+row*65,20,20,BLUE if row<2 else TEAL,'ellipse')
for y,s in [(735,'Fold'),(815,'Interface'),(895,'Developability')]:
 path([(x+35,y+14),(x+46,y+25),(x+66,y)],TEAL,5);text(x+88,y-3,s,29,NAVY,1)
# Assembly: tandem and antibody formats.
x=xs[3]
ribbon(x+99,510,BLUE,.65);ribbon(x+250,510,TEAL,.65)
path([(x+145,524),(x+157,535),(x+169,523),(x+181,535),(x+193,524)],MUTED,4)
text(x+18,609,'Tandem fusion',30,NAVY,1,w=309,align='center')
antibody(x+174,791,.85)
text(x+18,915,'IgG-like / scFv-Fc',29,NAVY,1,w=309,align='center')
# Prediction: a small PAE-style matrix, editable cells.
x=xs[4]
for a in range(8):
 for b in range(8):
  same=(a<4)==(b<4);col=('1B7593' if abs(a-b)<2 else '64A5B9') if same else 'E4EEF2'
  shape(x+65+a*27,455+b*27,25,25,col,'rect')
text(x+15,738,'AlphaFold2 / 3',32,NAVY,1,w=315,align='center')
text(x+15,803,'Folds + complexes',28,MUTED,w=315,align='center')
text(x+15,857,'pLDDT · PAE · ipTM*',26,MUTED,w=315,align='center')
# Experimental validation: response curve and two target badges.
x=xs[5]
path([(x+55,472),(x+55,650),(x+295,650)],MUTED,4)
path([(x+57,635),(x+85,628),(x+110,580),(x+135,533),(x+168,520),(x+252,520),(x+285,560)],TEAL,7)
for y,s in [(747,'Expression'),(827,'Dual binding'),(907,'Function')]:
 shape(x+31,y+5,13,13,TEAL,'ellipse');text(x+66,y,s,30,NAVY,1)
# Iteration below cards.
path([(xs[5]+173,1100),(xs[5]+173,1160),(xs[1]+173,1160)],TEAL,4)
arrow(xs[1]+173,1160,xs[1]+173,1100,TEAL,4)
shape(936,1130,570,57,BG,'rect');text(948,1135,'Experiment-guided redesign',30,TEAL,1)
text(76,1260,'*Interface scores where available. Set target- and format-specific criteria.',25,MUTED)
text(1740,1260,'Two arms → one construct',29,NAVY,1,w=590,align='center')
out=P/'08_06_general_bispecific_design_workflow.png';im.save(out,dpi=(180,180))
# Use existing clean master/layout package; all visible elements above are native shapes.
with zipfile.ZipFile(P/'08_03_alzheimer_bispecific_interview_slide.pptx') as z:
 files={n:z.read(n) for n in z.namelist() if not n.startswith('ppt/media/')}
files['ppt/slides/slide1.xml']=f'<p:sld xmlns:p="{N}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{"".join(parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
files['ppt/slides/_rels/slide1.xml.rels']=f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="{R}/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>'
ppt=P/'08_06_general_bispecific_design_workflow_editable.pptx'
with zipfile.ZipFile(ppt,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(ppt) as z:
 assert z.testzip() is None
 for n in z.namelist():
  if n.endswith(('.xml','.rels')):ET.fromstring(z.read(n))
 root=ET.fromstring(z.read('ppt/slides/slide1.xml'))
 assert not root.findall('.//{'+N+'}pic')
 print('Verified:',len(root.findall('.//{'+A+'}t')),'editable labels;',len(root.findall('.//{'+N+'}sp')),'native shapes; no raster slide image.')
print('Saved',out.name,'and',ppt.name)
