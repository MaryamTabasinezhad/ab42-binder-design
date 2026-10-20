#!/usr/bin/env python3
"""Create native editable PowerPoint text/shapes and scatter charts; stdlib only."""
import csv, io, zipfile
from pathlib import Path
from xml.sax.saxutils import escape as esc
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
NS='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
C='http://schemas.openxmlformats.org/drawingml/2006/chart'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'
S=5080
rows=list(csv.DictReader((P/'08_04_fusion_plot_data.csv').open()))
assert len(rows)==250 and sum(r['pass_all']=='True' for r in rows)==183
navy='102B46';blue='0072B2';orange='D55E00';muted='546B7E';bg='F3F6FA';white='FFFFFF';text='263E53'
parts=[];counter=1
def shape(x,y,w,h,fill=None,label='',size=24,color=text,bold=False,rounding=False):
 global counter
 counter+=1;i=counter
 fillxml=f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
 body=''
 if label:
  body=f'<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="t"/><a:lstStyle/><a:p><a:pPr/><a:r><a:rPr lang="en-US" sz="{round(size*40)}" b="{int(bold)}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="Arial"/><a:ea typeface="Arial"/><a:cs typeface="Arial"/></a:rPr><a:t>{esc(label)}</a:t></a:r><a:endParaRPr lang="en-US"/></a:p></p:txBody>'
 parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="{esc(label[:65]) if label else "Panel"}"/><p:cNvSpPr txBox="{int(bool(label))}"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{round(x*S)}" y="{round(y*S)}"/><a:ext cx="{round(w*S)}" cy="{round(h*S)}"/></a:xfrm><a:prstGeom prst="{"roundRect" if rounding else "rect"}"><a:avLst/></a:prstGeom>{fillxml}<a:ln><a:noFill/></a:ln></p:spPr>{body}</p:sp>')
def txt(x,y,w,s,n=24,color=text,bold=False):shape(x,y,w,n*1.55,label=s,size=n,color=color,bold=bold)
shape(0,0,2400,1350,bg);shape(0,0,2400,207,white)
txt(72,30,2200,'CURRENT RESEARCH  /  COMPUTATIONAL PROTEIN DESIGN',24,blue,True)
txt(72,75,2270,'AI-designed bispecific binders for Alzheimer’s disease',58,navy,True)
txt(74,151,2250,'Aβ42 targeting × transferrin receptor 1 (TfR1)  |  Goal: receptor-mediated delivery across the BBB',30,muted)
txt(74,201,2250,'PRE-FILTER EXPLORATION (reported trajectories):  Aβ42  1,342   |   TfR1 / BBB arm  2,051',25,text,True)
cards=[('01  TARGET PREPARATION','Structure-guided epitopes','Aβ42: 9CO4  •  TfR1: 6WRV'),('02  DE NOVO DESIGN','BindCraft + ProteinMPNN','Generate, redesign, AF2-score'),('03  FILTER & RANK','Stability + developability','23 Aβ42 / 224 TfR1 retained'),('04  FUSION LIBRARY','5 Aβ42 × 5 TfR1 binders','5 linkers × 2 domain orders'),('05  FOLD & SCREEN','AlphaFold2 / ColabFold','250 fusion predictions scored')]
for i,(a,b,c) in enumerate(cards):
 x=72+i*455;shape(x,238,434,156,white,rounding=True)
 txt(x+19,257,405,a,22,blue,True);txt(x+19,300,405,b,24,text,True);txt(x+19,345,405,c,21,muted)
for x,num,label,detail in [(72,'442','accepted arm designs','62 Aβ42 + 380 TfR1 (reported)'),(838,'250','fusion designs modeled','25 binder pairs × 10 variants'),(1604,'183 / 250','pass Stage 8 gates','73.2% computational pass rate')]:
 highlighted=x==1604;fg=white if highlighted else navy
 shape(x,420,724,155,blue if highlighted else white,rounding=True)
 txt(x+24,432,670,num,53,fg,True);txt(x+24,497,670,label,27,fg,True);txt(x+24,540,670,detail,21,'D7EAF6' if highlighted else muted)
txt(74,593,2250,'FUSION-LEVEL COMPARISON  •  All 250 designs; one top-ranked prediction per design',24,text,True)
shape(76,638,16,16,blue);txt(103,630,340,'Pass all gates (n = 183)',22)
shape(448,638,16,16,orange);txt(476,630,430,'Fail ≥1 gate (n = 67)',22)
txt(1608,630,700,'Dashed lines: required thresholds',22,muted)
shape(62,674,1100,550,white);shape(1238,674,1100,550,white)
txt(88,685,1040,'Per-arm folding confidence across fusion designs',27,text,True)
txt(1264,685,1040,'Whole-chain confidence vs. domain independence',27,text,True)
shape(0,1230,2400,120,'E7EEF4')
txt(73,1242,2250,'Gate: both arms pLDDT >80 AND inter-domain PAE >15 Å. High inter-domain PAE reflects uncertain relative orientation.',24)

def rels(items):return f'<Relationships xmlns="{PKG}">'+''.join(f'<Relationship Id="{i}" Type="{R}/{t}" Target="{v}"/>' for i,t,v in items)+'</Relationships>'
def workbook(series):
 # Each series has an independent x/y column pair, including threshold lines.
 sheetrows={1:[]}
 def col(n):
  s=''
  while n:n,k=divmod(n-1,26);s=chr(65+k)+s
  return s
 for k,(name,xs,ys,_,_) in enumerate(series):
  for j,values in enumerate([xs,ys]):
   letter=col(2*k+j+1)
   sheetrows[1].append(f'<c r="{letter}1" t="inlineStr"><is><t>{esc(name)} {"x" if j==0 else "y"}</t></is></c>')
   for i,v in enumerate(values,2):sheetrows.setdefault(i,[]).append(f'<c r="{letter}{i}"><v>{v}</v></c>')
 cells=''.join(f'<row r="{i}">{"".join(v)}</row>' for i,v in sorted(sheetrows.items()))
 contents={'[Content_Types].xml':'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>',
 '_rels/.rels':rels([('rId1','officeDocument','xl/workbook.xml')]),
 'xl/workbook.xml':f'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="{R}"><sheets><sheet name="Fusion data" sheetId="1" r:id="rId1"/></sheets></workbook>',
 'xl/_rels/workbook.xml.rels':rels([('rId1','worksheet','worksheets/sheet1.xml')]),
 'xl/worksheets/sheet1.xml':f'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{cells}</sheetData></worksheet>'}
 out=io.BytesIO()
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  for n,s in contents.items():z.writestr(n,s)
 return out.getvalue()
def rich(s,n=1100):return f'<c:tx><c:rich><a:bodyPr/><a:lstStyle/><a:p><a:pPr/><a:r><a:rPr sz="{n}"><a:solidFill><a:srgbClr val="{text}"/></a:solidFill><a:latin typeface="Arial"/></a:rPr><a:t>{esc(s)}</a:t></a:r></a:p></c:rich></c:tx>'
def axis(i,cross,position,title,lo,hi,step):
 return f'<c:valAx><c:axId val="{i}"/><c:scaling><c:orientation val="minMax"/><c:max val="{hi}"/><c:min val="{lo}"/></c:scaling><c:delete val="0"/><c:axPos val="{position}"/><c:majorGridlines><c:spPr><a:ln w="6350"><a:solidFill><a:srgbClr val="DAE3EC"/></a:solidFill></a:ln></c:spPr></c:majorGridlines><c:title>{rich(title)}<c:overlay val="0"/></c:title><c:numFmt formatCode="0.##" sourceLinked="0"/><c:majorTickMark val="none"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/><c:crossAx val="{cross}"/><c:crosses val="min"/><c:crossBetween val="midCat"/><c:majorUnit val="{step}"/></c:valAx>'
extras={}
for chartnum,kind in enumerate(['arms','global'],1):
 if kind=='arms':
  xk,yk='tfr1_plddt','ab42_plddt';xt,yt='TfR1 arm mean pLDDT','Aβ42 arm mean pLDDT';xr=(30,100,10);yr=(30,100,10)
  thresholds=[('TfR1 threshold',[80,80],[30,100],'607587',True),('Aβ42 threshold',[30,100],[80,80],'607587',True)]
 else:
  xk,yk='ptm','inter_domain_pae';xt,yt='Fusion pTM (informational; not a gate)','Inter-domain PAE (Å)';xr=(.4,.75,.05);yr=(0,30,5)
  thresholds=[('PAE threshold',[.4,.75],[15,15],'607587',True)]
 series=[]
 for passing,color,name in [(False,orange,'Fail ≥1 gate (n = 67)'),(True,blue,'Pass all gates (n = 183)')]:
  subset=[r for r in rows if (r['pass_all']=='True')==passing]
  series.append((name,[float(r[xk]) for r in subset],[float(r[yk]) for r in subset],color,False))
 series+=thresholds
 ser=[]
 for k,(name,xs,ys,color,line) in enumerate(series):
  def ref(values,j):
   letter=chr(65+2*k+j);cache=''.join(f'<c:pt idx="{i}"><c:v>{v}</c:v></c:pt>' for i,v in enumerate(values))
   return f'<c:numRef><c:f>\'Fusion data\'!${letter}$2:${letter}${len(values)+1}</c:f><c:numCache><c:formatCode>General</c:formatCode><c:ptCount val="{len(values)}"/>{cache}</c:numCache></c:numRef>'
  stroke=f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:prstDash val="dash"/></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
  marker='<c:marker><c:symbol val="none"/></c:marker>' if line else f'<c:marker><c:symbol val="circle"/><c:size val="4"/><c:spPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln w="3175"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:ln></c:spPr></c:marker>'
  ser.append(f'<c:ser><c:idx val="{k}"/><c:order val="{k}"/><c:tx><c:v>{esc(name)}</c:v></c:tx><c:spPr>{stroke}</c:spPr>{marker}<c:xVal>{ref(xs,0)}</c:xVal><c:yVal>{ref(ys,1)}</c:yVal><c:smooth val="0"/></c:ser>')
 chart=f'<c:chartSpace xmlns:c="{C}" xmlns:a="{A}" xmlns:r="{R}"><c:lang val="en-US"/><c:chart><c:autoTitleDeleted val="1"/><c:plotArea><c:layout/><c:scatterChart><c:scatterStyle val="lineMarker"/><c:varyColors val="0"/>{"".join(ser)}<c:axId val="100"/><c:axId val="200"/></c:scatterChart>{axis(100,200,"b",xt,*xr)}{axis(200,100,"l",yt,*yr)}<c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln><a:noFill/></a:ln></c:spPr></c:plotArea><c:plotVisOnly val="1"/></c:chart><c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln><a:noFill/></a:ln></c:spPr><c:txPr><a:bodyPr/><a:lstStyle/><a:p><a:pPr><a:defRPr sz="1000"><a:solidFill><a:srgbClr val="{muted}"/></a:solidFill><a:latin typeface="Arial"/></a:defRPr></a:pPr><a:endParaRPr lang="en-US"/></a:p></c:txPr><c:externalData r:id="rId1"><c:autoUpdate val="0"/></c:externalData></c:chartSpace>'
 extras[f'ppt/charts/chart{chartnum}.xml']=chart
 extras[f'ppt/charts/_rels/chart{chartnum}.xml.rels']=rels([('rId1','package',f'../embeddings/fusion_data{chartnum}.xlsx')])
 extras[f'ppt/embeddings/fusion_data{chartnum}.xlsx']=workbook(series)
 counter+=1;x=68 if chartnum==1 else 1244
 parts.append(f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{counter}" name="Editable fusion scatter plot {chartnum}"/><p:cNvGraphicFramePr/><p:nvPr/></p:nvGraphicFramePr><p:xfrm><a:off x="{x*S}" y="{727*S}"/><a:ext cx="{1085*S}" cy="{490*S}"/></p:xfrm><a:graphic><a:graphicData uri="{C}"><c:chart xmlns:c="{C}" r:id="rId{chartnum}"/></a:graphicData></a:graphic></p:graphicFrame>')
with zipfile.ZipFile(P/'08_03_alzheimer_bispecific_interview_slide.pptx') as src:
 files={n:src.read(n) for n in src.namelist() if not n.startswith('ppt/media/')}
files['ppt/slides/slide1.xml']=f'<p:sld xmlns:p="{NS}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{"".join(parts)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
files['ppt/slides/_rels/slide1.xml.rels']=rels([('rId1','chart','../charts/chart1.xml'),('rId2','chart','../charts/chart2.xml'),('rId3','slideLayout','../slideLayouts/slideLayout1.xml')])
ct=files['[Content_Types].xml'].decode()
ct=ct.replace('</Types>','<Default Extension="xlsx" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/>'+''.join(f'<Override PartName="/ppt/charts/chart{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.drawingml.chart+xml"/>' for i in [1,2])+'</Types>')
files['[Content_Types].xml']=ct
files.update(extras)
out=P/'08_05_alzheimer_bispecific_interview_slide_editable.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for n in z.namelist():
  if n.endswith(('.xml','.rels')):ET.fromstring(z.read(n))
  if n.endswith('.xlsx'):
   with zipfile.ZipFile(io.BytesIO(z.read(n))) as book:
    assert book.testzip() is None
    for entry in book.namelist():ET.fromstring(book.read(entry))
 slide=ET.fromstring(z.read('ppt/slides/slide1.xml'))
 assert len(slide.findall('.//{'+NS+'}pic'))==0
 assert len(slide.findall('.//{'+C+'}chart'))==2
 print('Saved',out.name,'with',len(slide.findall('.//{'+A+'}t')),'editable text boxes, 2 native charts and 2 embedded workbooks; no flattened slide image.')
