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
# Publication-style diagram: native vector boxes and connectors; no illustrative data.
# Scientific text is intentionally short; implementation notes remain in README.
shape(0,0,W,H,WHITE,'rect')
text(70,53,'Structure-guided design of bispecific proteins',62,NAVY,1)
text(73,135,'Target-specific arm discovery, format engineering and experimental validation',32,MUTED)
path([(70,207),(2330,207)],LIGHT,2)
text(70,242,'A   TARGET-SPECIFIC ARM DISCOVERY',29,BLUE,1)
text(1350,244,'Repeat independently for arm A and arm B',28,MUTED)
xs=[70,645,1220,1795];cw=535
# Flat, consistently sized scientific process nodes.
def node(x,y,title,lines,h=330,color=BLUE):
 shape(x,y,cw,h,WHITE,'rect',stroke='B4C1CD')
 shape(x,y,cw,6,color,'rect')
 text(x+26,y+26,title,35,NAVY,1,w=cw-50)
 for yy,s,n,c,bold in lines:
  text(x+26,y+yy,s,n,c,bold,w=cw-50)
node(xs[0],320,'1  Target definition',[
 (125,'Structure + epitope',34,NAVY,0),
 (183,'Accessibility · native context',29,MUTED,0),
 (237,'Counter-target panel',30,MUTED,0)])
node(xs[1],320,'2  Arm generation',[
 (91,'MINIPROTEIN',23,BLUE,1),
 (127,'RFdiffusion → ProteinMPNN',30,NAVY,0),
 (168,'or BindCraft',29,MUTED,0),
 (227,'ANTIBODY / VHH',23,BLUE,1),
 (265,'RFantibody¹',32,NAVY,0)])
path([(xs[1]+25,532),(xs[1]+cw-25,532)],LIGHT,2)
node(xs[2],320,'3  Complex prediction',[
 (104,'AlphaFold2-Multimer / AlphaFold3',29,NAVY,0),
 (158,'Antibody-tuned RF2',30,NAVY,0),
 (234,'Fold · interface · epitope recovery',28,MUTED,0)])
node(xs[3],320,'4  Arm selection',[
 (108,'Confidence + developability',31,NAVY,0),
 (170,'Selectivity controls',30,MUTED,0),
 (232,'Sequence + scaffold diversity',29,MUTED,0)])
for x in xs[:-1]:arrow(x+cw+8,485,x+cw+33,485,BLUE,4)
# A single row-to-row connector carries selected arms into construct engineering.
path([(2062,650),(2062,755),(560,755)],BLUE,4)
arrow(560,755,560,883,BLUE,4)
shape(710,723,990,63,WHITE,'rect')
text(735,729,'Selected arm A + arm B',33,BLUE,1,w=940,align='center')
text(70,831,'B   BISPECIFIC ENGINEERING',29,BLUE,1)
text(1220,831,'C   EXPERIMENTAL VALIDATION',29,TEAL,1)
node(xs[0],890,'5  Bispecific assembly',[
 (93,'Arm pairs · linkers · domain order',28,NAVY,0),
 (150,'Valency · Fc / chain pairing',29,MUTED,0)],h=240)
node(xs[1],890,'6  Construct evaluation',[
 (93,'AlphaFold2 / AlphaFold3',31,NAVY,0),
 (150,'Folds · accessibility · steric clashes',27,MUTED,0)],h=240)
node(xs[2],890,'7  Expression & QC',[
 (93,'Gene synthesis · production',30,NAVY,0),
 (150,'SEC–MALS · DSF',31,MUTED,0)],h=240,color=TEAL)
node(xs[3],890,'8  Functional validation',[
 (93,'SPR / BLI · simultaneous binding',28,NAVY,0),
 (150,'Specificity · application assays',29,MUTED,0)],h=240,color=TEAL)
for i,x in enumerate(xs[:-1]):arrow(x+cw+8,1010,x+cw+33,1010,BLUE if i==0 else TEAL,4)
# Iteration is an experimental feedback path, not a claim of completed validation.
path([(2062,1130),(2062,1190),(337,1190)],TEAL,3)
arrow(337,1190,337,1138,TEAL,3)
shape(865,1164,690,56,WHITE,'rect')
text(884,1168,'Assay-guided redesign',29,TEAL,1,w=650,align='center')
text(70,1264,'¹ RFantibody: antibody-tuned RFdiffusion → ProteinMPNN → antibody-tuned RoseTTAFold2.',26,MUTED)
out=P/'08_06_general_bispecific_design_workflow.png';im.save(out,dpi=(300,300))
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
