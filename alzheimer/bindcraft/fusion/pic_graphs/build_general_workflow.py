#!/usr/bin/env python3
"""Render a general bispecific workflow, adapted from the two supplied charts."""
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
W,H=2400,2850
im=Image.new('RGB',(W,H),'#F5F7FA');d=ImageDraw.Draw(im)
NAVY='#17324D';TEXT='#263E53';MUTED='#586D80';BLUE='#0072B2';GREEN='#008577';LINE='#71879B'
fonts={b:subprocess.check_output(['fc-match','-f','%{file}','Liberation Sans:style='+('Bold' if b else 'Regular')],text=True).strip() for b in [False,True]}
def font(n,b=False):return ImageFont.truetype(fonts[b],n)
def text(x,y,s,n=32,c=TEXT,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def center(y,s,n=32,c=TEXT,b=False):
 width=d.textlength(s,font=font(n,b));text((W-width)/2,y,s,n,c,b)
def fit(x,y,s,n,maxw,c=TEXT,b=False):
 assert d.textlength(s,font=font(n,b))<=maxw,(s,maxw)
 text(x,y,s,n,c,b)
def box(x,y,w,h,title,lines,color=BLUE,tint='#FFFFFF',n=31):
 d.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=tint,outline='#D7E1EA',width=2)
 d.rounded_rectangle((x,y,x+8,y+h),radius=4,fill=color)
 fit(x+32,y+23,title,36,w-65,color,True)
 for i,line in enumerate(lines):fit(x+32,y+79+i*44,line,n,w-65)
def arrow(x,y1,y2,color=LINE):
 d.line((x,y1,x,y2-13),fill=color,width=5)
 d.polygon([(x-12,y2-17),(x+12,y2-17),(x,y2)],fill=color)
# Title and scope.
d.rectangle((0,0,W,190),fill='white')
text(85,32,'GENERAL DESIGN WORKFLOW',27,BLUE,True)
text(85,77,'AI-designed bispecific binders & antibodies',64,NAVY,True)
text(87,151,'Two targets or two distinct epitopes  •  Design each arm independently, then engineer the combined format',31,MUTED)
box(170,230,2060,175,'01  DEFINE TARGETS, EPITOPES & FUNCTION',[
 'Use experimental structures where available; AlphaFold models can support missing structural information.',
 'Map accessible sites, glycans and native numbering; define counter-targets, valency and desired biological effect.'
],n=31)
arrow(1200,405,447)
center(452,'02  CHOOSE A DESIGN ROUTE FOR EACH ARM  (A and B may use different formats)',31,NAVY,True)
# Modality routes; each operates on an individual target/epitope.
d.line((1200,493,1200,512),fill=LINE,width=5);d.line((630,512,1770,512),fill=LINE,width=5)
arrow(630,512,545,BLUE);arrow(1770,512,545,GREEN)
box(95,545,1070,445,'MINIPROTEIN / DE NOVO BINDER',[
 'RFdiffusion [1] → generate target-conditioned backbones.',
 'ProteinMPNN [2] → design sequences for those backbones.',
 'Alternative: BindCraft [3] → AlphaFold2-guided design',
 'with ProteinMPNN redesign and structural filtering.',
 'Output: diverse binder sequences and predicted poses.',
 'Retain multiple scaffolds, not only the highest score.'
],BLUE,'#EFF6FC',n=30)
box(1235,545,1070,445,'ANTIBODY / NANOBODY',[
 'RFantibody [4] → framework-based antibody/CDR design.',
 'Antibody-tuned RFdiffusion → generate binding loops.',
 'ProteinMPNN → redesign allowed sequence positions.',
 'Antibody-tuned RoseTTAFold2 → predict/filter complexes.',
 'Choose Fab/Fv or VHH frameworks and CDR lengths;',
 'assess human compatibility and sequence liabilities.'
],GREEN,'#EEF8F5',n=30)
# Join the two routes.
d.line((630,990,630,1025,1770,1025,1770,990),fill=LINE,width=5)
arrow(1200,1025,1065)
box(170,1065,2060,175,'03  REPREDICT EACH ARM–TARGET COMPLEX',[
 'AlphaFold2-Multimer / ColabFold or AlphaFold3 [5] → evaluate predicted folds and binding poses.',
 'Use an independent prediction setup where practical; inspect epitope recovery, contacts and structural clashes.'
],n=31)
arrow(1200,1240,1280)
box(170,1280,2060,220,'04  SCREEN, RANK & SELECT DIVERSE ARMS',[
 'Confidence: per-arm pLDDT, within-domain PAE and interface confidence (ipTM / interface PAE, when available).',
 'Rosetta / PyRosetta → interface packing and energy; also assess aggregation, charge and chemical liabilities.',
 'Counter-screen related proteins and relevant normal tissues; confirm shortlisted arm binding when feasible.'
],n=30)
arrow(1200,1500,1540)
box(170,1540,2060,220,'05  ASSEMBLE A BISPECIFIC LIBRARY',[
 'Miniproteins / VHH / scFv: sample arm pairs, linker lengths, linker types and both domain orders.',
 'Antibodies: choose tandem-scFv-Fc or IgG-like architecture; engineer heavy/light-chain pairing as needed.',
 'Balance valency, geometry and target accessibility; allow mixed binder–antibody formats when appropriate.'
],n=31)
arrow(1200,1760,1800)
box(170,1800,2060,220,'06  CHECK THE COMPLETE CONSTRUCT & TARGET ENGAGEMENT',[
 'AlphaFold2 / AlphaFold3 → assess domain folds and sampled arm–target complexes; check steric compatibility.',
 'Inspect pTM, PAE, binding-site accessibility and linker geometry; assess simultaneous binding where feasible.',
 'Uncertain domain orientation can lower global pTM. Set format-specific gates; high inter-domain PAE is not proof of flexibility.'
],n=29)
arrow(1200,2020,2060)
box(170,2060,2060,175,'07  PREPARE FOR EXPRESSION',[
 'Choose expression host, signal peptides/tags and purification strategy; optimize DNA and check sequence identity.',
 'For antibodies: consider secretion, disulfides, glycosylation and assembly. Preserve a diverse experimental panel.'
],n=31)
arrow(1200,2235,2275)
box(170,2275,2060,220,'08  EXPERIMENTALLY VALIDATE & ITERATE',[
 'Expression + purification → SEC / SEC-MALS for assembly and aggregation; DSF for thermal stability.',
 'SPR / BLI → measure affinity to each target, selectivity and simultaneous dual binding; test the intended function.',
 'Use results to redesign arms, linkers or format. Add transport, signaling or efficacy assays as required by the application.'
],GREEN,'#EEF8F5',n=30)
# Iteration arrow, outside the main content.
d.line((2235,2390,2337,2390,2337,1390,2248,1390),fill=GREEN,width=4)
d.polygon([(2248,1390),(2266,1378),(2266,1402)],fill=GREEN)
lab=Image.new('RGBA',(600,44),(0,0,0,0));ld=ImageDraw.Draw(lab);ld.text((0,0),'EXPERIMENT-GUIDED REDESIGN',font=font(25,True),fill=GREEN)
lab=lab.rotate(90,expand=True);im.paste(lab,(2346,1570),lab)
center(2545,'GENERAL TEMPLATE — target tractability and model suitability must be assessed for each campaign.',29,MUTED,True)
center(2590,'Prediction scores prioritize hypotheses; they do not establish affinity, selectivity or biological activity.',29,MUTED)
d.line((170,2650,2230,2650),fill='#D7E1EA',width=2)
text(170,2676,'MODEL SOURCES',23,BLUE,True)
text(170,2715,'[1] RosettaCommons/RFdiffusion     [2] dauparas/ProteinMPNN     [3] martinpacesa/BindCraft',26,MUTED)
text(170,2756,'[4] RosettaCommons/RFantibody     [5] google-deepmind/alphafold3  •  Full links and scope notes in README',26,MUTED)
output=P/'08_06_general_bispecific_design_workflow.png'
im.save(output,dpi=(200,200))
print(output.name,im.size)
