#!/usr/bin/env python3
"""One visual 16:9 workflow, rendered as PNG and native editable PPTX."""
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
pdf_surface=cairo.PDFSurface(str(P/'08_06_general_bispecific_design_workflow.pdf'),PDF_WIDTH_PT,PDF_WIDTH_PT*H/W)
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
# Research schematic; blue computational stages, green experimental stages.
shape(0,0,W,H,WHITE,'rect')
text(70,45,'Structure-guided design of bispecific proteins',62,NAVY,1)
text(73,128,'Proposed general workflow | target-specific discovery to experimental validation',35,MUTED)
path([(70,202),(2330,202)],LIGHT,2)
text(70,234,'A   TARGET-SPECIFIC ARM DISCOVERY',34,BLUE,1)
text(1390,234,'Repeat for arm A and arm B',34,MUTED)
xs=[70,645,1220,1795];cw=535
def node(x,y,title,lines,h=340,color=BLUE):
 shape(x,y,cw,h,WHITE,'rect',stroke='A7B5C2')
 shape(x,y,cw,6,color,'rect')
 text(x+25,y+25,title,36,NAVY,1,w=cw-50)
 for yy,s,n,c,bold in lines:text(x+25,y+yy,s,n,c,bold,w=cw-50)
node(xs[0],310,'1  Target definition',[
 (113,'Structure + epitope',36,NAVY,0),
 (181,'Accessibility + native state',34,MUTED,0),
 (249,'Counter-target panel',34,MUTED,0)])
node(xs[1],310,'2  Arm generation',[
 (89,'MINIPROTEIN',33,BLUE,1),
 (133,'RFdiffusion → ProteinMPNN',34,NAVY,0),
 (176,'or BindCraft',34,MUTED,0),
 (239,'ANTIBODY / VHH',33,BLUE,1),
 (282,'RFantibody',36,NAVY,0)])
path([(xs[1]+25,530),(xs[1]+cw-25,530)],LIGHT,2)
node(xs[2],310,'3  Complex reassessment',[
 (103,'AlphaFold2-Multimer',34,NAVY,0),
 (148,'or AlphaFold3',34,NAVY,0),
 (212,'Independent setup¹',34,MUTED,0),
 (267,'Fold · interface · epitope',34,MUTED,0)])
node(xs[3],310,'4  Arm selection',[
 (100,'Confidence + developability',34,NAVY,0),
 (158,'Controls + scaffold diversity',34,MUTED,0),
 (216,'Confirm arm binding',34,TEAL,0),
 (270,'and specificity²',34,TEAL,0)])
for x in xs[:-1]:arrow(x+cw+7,480,x+cw+34,480,BLUE,4)
# Serpentine routing eliminates the long return connector.
arrow(2062,650,2062,868,BLUE,4)
text(1355,700,'Selected arms A + B',35,BLUE,1,w=620,align='center')
text(70,793,'B   BISPECIFIC ENGINEERING AND EXPERIMENTAL TESTING',34,NAVY,1)
# The numbered path runs right to left in panel B.
node(xs[3],880,'5  Format engineering',[
 (97,'Pairs · linkers · domain order',34,NAVY,0),
 (154,'Valency + accessibility',34,MUTED,0),
 (212,'IgG-like: chain pairing',34,MUTED,0)],h=290)
node(xs[2],880,'6  Construct assessment',[
 (97,'AlphaFold2 / AlphaFold3',34,NAVY,0),
 (154,'Domain folds + clashes',34,MUTED,0),
 (212,'Dual-target accessibility',34,MUTED,0)],h=290)
node(xs[1],880,'7  Production + QC',[
 (97,'Expression + purification',34,NAVY,0),
 (154,'SEC–MALS · DSF',35,MUTED,0),
 (212,'Assembly + stability',34,MUTED,0)],h=290,color=TEAL)
node(xs[0],880,'8  Functional validation',[
 (97,'SPR / BLI · dual binding',34,NAVY,0),
 (154,'Specificity + controls',34,MUTED,0),
 (212,'Application-specific assays',34,MUTED,0)],h=290,color=TEAL)
for i in [3,2,1]:arrow(xs[i]-7,1025,xs[i]-34,1025,BLUE if i==3 else TEAL,4)
# Experimental feedback, explicitly distinct from model scores.
path([(337,1170),(337,1230),(2062,1230)],TEAL,3)
arrow(2062,1230,2062,1180,TEAL,3)
shape(860,1205,720,54,WHITE,'rect')
text(880,1207,'Assay-guided redesign',34,TEAL,1,w=680,align='center')
text(70,1290,'Blue: computational design',33,BLUE)
text(800,1290,'Green: experimental assessment',33,TEAL)
out=P/'08_06_general_bispecific_design_workflow.png'
im.save(out,dpi=(W/(180/25.4),W/(180/25.4)))
pdf_surface.finish()
print('Vector PDF width: 180 mm; minimum label size:',round(min(text_sizes),2),'pt')
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
