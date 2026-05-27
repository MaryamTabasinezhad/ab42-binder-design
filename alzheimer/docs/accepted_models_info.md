---
title: "Accepted Binder Models --- Binding Interaction Analysis"
subtitle: "BindCraft A$\\beta$42 Campaign (9CO4 C/E/G)"
date: "2026-05-08"
geometry: "landscape,margin=1.5cm"
fontsize: 8pt
header-includes:
  - \usepackage{booktabs}
  - \usepackage{longtable}
  - \usepackage{colortbl}
  - \usepackage{xcolor}
  - \definecolor{hbondblue}{RGB}{210,230,255}
  - \definecolor{saltred}{RGB}{255,220,220}
  - \definecolor{hydrophgreen}{RGB}{220,245,220}
  - \usepackage{array}
---

# 1. Summary of All 7 Accepted Designs

\scriptsize
\setlength{\tabcolsep}{2.5pt}

\begin{longtable}{|c|l|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
\textbf{Rank} & \textbf{Design} & \textbf{Len} & \textbf{MW} & \textbf{i\_pTM} & \textbf{pTM} & \textbf{pLDDT} & \textbf{i\_pAE} & \textbf{B\_pLDDT} & \textbf{B\_RMSD} & \textbf{S.Hyd} & \textbf{SC} & \textbf{dG} & \textbf{dSASA} & \textbf{nIR} & \textbf{nIHb} & \textbf{nUHb} & \textbf{H.RMSD} & \textbf{R.Cl} & \textbf{K} & \textbf{M} & \textbf{HS} & \textbf{Helix\%} & \textbf{Notes} \\
\hline
1 & s120913\_mp1 & 79 & 8.7 & 0.81 & 0.84 & 0.88 & 0.19 & 0.90 & 2.61 & 0.26 & 0.68 & -93.7 & 2929 & 32.5 & 7.5 & 1.5 & 1.02 & 0 & 1.5 & 1.0 & 14/18 & 67.1 & Clean \\
2 & s120913\_mp2 & 79 & 8.7 & 0.81 & 0.84 & 0.88 & 0.19 & 0.89 & 2.18 & 0.28 & 0.69 & -98.9 & 3146 & 39.5 & 11.5 & 1.0 & 1.67 & 0.5 & 1.0 & 2.0 & 14/18 & 65.8 & R.Cl \\
3 & s716952\_mp20 & 87 & 9.6 & 0.76 & 0.80 & 0.89 & 0.21 & 0.89 & 1.47 & 0.34 & 0.66 & -74.7 & 2541 & 29.5 & 4.0 & 2.0 & 3.09 & 0 & 1.0 & 3.0 & 13/18 & 77.0 & Clean, NEW \\
4 & s480128\_mp13 & 82 & 9.0 & 0.72 & 0.80 & 0.89 & 0.20 & 0.86 & 2.15 & 0.34 & 0.71 & -73.7 & 2042 & 24.0 & 3.5 & 2.0 & 1.15 & 0.5 & 1.0 & 0.0 & 11/18 & 85.4 & R.Cl \\
5 & s480128\_mp17 & 82 & 9.0 & 0.76 & 0.82 & 0.92 & 0.18 & 0.95 & 0.90 & 0.34 & 0.68 & -71.0 & 2141 & 25.5 & 3.5 & 2.5 & 1.51 & 0.5 & 1.0 & 0.0 & 11/18 & 85.4 & R.Cl \\
6 & s967366\_mp11 & 82 & 9.0 & 0.79 & 0.84 & 0.94 & 0.17 & 0.95 & 1.11 & 0.32 & 0.76 & -71.8 & 2003 & 21.5 & 3.5 & 3.0 & 1.12 & 0 & 1.5 & 3.0 & 10/18 & 82.9 & Clean \\
7 & s311665\_mp6 & 68 & 7.5 & 0.73 & 0.80 & 0.89 & 0.20 & 0.88 & 1.22 & 0.30 & 0.67 & -62.7 & 2029 & 25.0 & 3.5 & 3.5 & 2.50 & 0 & 0.5 & 3.0 & 9/18 & 82.4 & Clean \\
\hline
\end{longtable}

\normalsize

\textbf{Column key:} Len = binder length (aa), MW = molecular weight (kDa), SC = shape complementarity, dG = binding energy (REU), dSASA = buried surface area (\AA$^2$), nIR = interface residues, nIHb = interface H-bonds, nUHb = unsatisfied H-bonds, H.RMSD = hotspot RMSD (\AA), R.Cl = relaxed clashes, K/M = interface Lys/Met count, HS = hotspot contacts.

\newpage

# 2. Binding Interaction Analysis --- Overview

\small

\begin{longtable}{|l|c|c|c|c|c|c|c|c|c|}
\hline
\textbf{Design} & \textbf{HS} & \textbf{Chain C} & \textbf{Chain E} & \textbf{Chain G} & \textbf{Binder IF Res} & \textbf{H-bond pairs} & \textbf{Hydrophobic pairs} & \textbf{Salt bridges} & \textbf{Dominant type} \\
\hline
s120913\_mp1 & 14/18 & 6/6 & 5/6 & 3/6 & 42 & 12 & 191 & 4 & Mixed (H-bond + Hydro) \\
s120913\_mp2 & 14/18 & 6/6 & 5/6 & 3/6 & 45 & 13 & 203 & 2 & Mixed (H-bond + Hydro) \\
s716952\_mp20 & 13/18 & 3/6 & 4/6 & 6/6 & 33 & 4 & 163 & 0 & Hydrophobic \\
s480128\_mp13 & 11/18 & 3/6 & 4/6 & 4/6 & 32 & 5 & 150 & 0 & Hydrophobic \\
s480128\_mp17 & 11/18 & 3/6 & 4/6 & 4/6 & 31 & 5 & 189 & 0 & Hydrophobic \\
s967366\_mp11 & 10/18 & 2/6 & 3/6 & 5/6 & 25 & 4 & 163 & 0 & Hydrophobic \\
s311665\_mp6 & 9/18 & 3/6 & 3/6 & 3/6 & 27 & 5 & 142 & 0 & Hydrophobic \\
\hline
\end{longtable}

\normalsize

## 2.1 Hotspot Residue Contact Map

Which hotspot residues are contacted ($<$5 \AA) by each design:

\small

\begin{longtable}{|l|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
& \multicolumn{6}{c|}{\textbf{Chain C}} & \multicolumn{6}{c|}{\textbf{Chain E}} & \multicolumn{6}{c|}{\textbf{Chain G}} \\
\cline{2-19}
\textbf{Design} & Y10 & E11 & H13 & H14 & Q15 & K16 & Y10 & E11 & H13 & H14 & Q15 & K16 & Y10 & E11 & H13 & H14 & Q15 & K16 \\
\hline
s120913\_mp1 & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & & $\bullet$ & $\bullet$ \\
s120913\_mp2 & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & & $\bullet$ & $\bullet$ \\
s716952\_mp20 & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ \\
s480128\_mp13 & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & $\bullet$ & $\bullet$ \\
s480128\_mp17 & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & & $\bullet$ & $\bullet$ \\
s967366\_mp11 & & & & & $\bullet$ & $\bullet$ & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & $\bullet$ & & $\bullet$ & $\bullet$ \\
s311665\_mp6 & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & & & & $\bullet$ & $\bullet$ & $\bullet$ & & & & $\bullet$ & $\bullet$ \\
\hline
\end{longtable}

\normalsize

\textbf{Observations:}
\begin{itemize}
\item Q15 and K16 are contacted by all 7 designs on all 3 chains --- most accessible hotspots.
\item Y10 is contacted by 6/7 designs on at least chain C.
\item H13/H14 are the hardest to reach --- only s120913 (chain C) and s716952 (chain G) contact them.
\item s120913 is the only scaffold achieving 6/6 contacts on any single chain (chain C).
\end{itemize}

\newpage

# 3. Per-Design Hotspot Interaction Tables

## 3.1 Rank 1: s120913\_mpnn1 (79 aa, 14/18 hotspots, 4 salt bridges)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:3, B:4, B:7 & T, R, L & 2.1 & Hydrophobic \\
C:E11 & B:4, B:7 & R, L & 3.3 & vdW \\
C:H13 & B:78, B:79 & E, E & 2.6 & Hydrophobic \\
C:H14 & B:77, B:78, B:79 & V, E, E & 1.8 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:Q15 & B:8, B:76, B:77, B:78, B:79 & W, I, V, E, E & 2.3 & Hydrophobic \\
C:K16 & B:8, B:76, B:77, B:78, B:79 & W, I, V, E, E & 2.0 & \cellcolor{hbondblue}\textbf{H-bond} \\
E:E11 & B:7 & L & 2.8 & Hydrophobic \\
E:H14 & B:79 & E & 4.4 & vdW \\
E:K16 & B:8, B:79 & W, E & 1.8 & \cellcolor{saltred}\textbf{H-bond, Salt bridge} \\
E:Q15 & B:8, B:11, B:12, B:15 & W, A, T, L & 1.7 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Y10 & B:3, B:7, B:50, B:52 & T, L, K, F & 2.0 & Hydrophobic \\
G:K16 & B:15 & L & 2.8 & Hydrophobic \\
G:Q15 & B:11, B:12, B:15, B:18 & A, T, L, R & 1.9 & \cellcolor{saltred}\textbf{H-bond, Salt bridge} \\
G:Y10 & B:7, B:11, B:14, B:47, B:52 & L, A, Q, A, F & 1.7 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:8 W (H-bond + hydro with C/E:Q15, K16), B:18 R (\textbf{salt bridge} with G:Q15), B:79 E (\textbf{salt bridge} with E:K16), B:14 Q (H-bond with G:Y10), B:77 V (H-bond with C:K16).

\textbf{Sequence:} MDTREQLWWFATAQLLVRHIIEHMRAVGDTSQLARWEADLEILEERARRKEFTIPEDTEIYRLMKTLKENTKGHKIVEE

\normalsize

## 3.2 Rank 2: s120913\_mpnn2 (79 aa, 14/18 hotspots, 2 salt bridges)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:1, B:2, B:3, B:4, B:7 & M, P, T, R, L & 2.0 & Hydrophobic \\
C:E11 & B:4, B:7 & R, L & 2.9 & vdW \\
C:H13 & B:4, B:78, B:79 & R, E, E & 3.3 & vdW \\
C:H14 & B:77, B:78, B:79 & V, E, E & 1.9 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:Q15 & B:4, B:8, B:76, B:77, B:78 & R, W, I, V, E & 2.1 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:K16 & B:8, B:76, B:77, B:78, B:79 & W, I, V, E, E & 1.9 & \cellcolor{hbondblue}\textbf{H-bond} \\
E:E11 & B:7 & L & 2.7 & Hydrophobic \\
E:H14 & B:79 & E & 4.4 & vdW \\
E:K16 & B:8, B:15, B:79 & W, L, E & 3.2 & vdW \\
E:Q15 & B:7, B:8, B:11, B:12, B:15 & L, W, A, T, L & 1.8 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Y10 & B:2, B:7, B:50, B:52 & P, L, K, F & 2.1 & Hydrophobic \\
G:K16 & B:15 & L & 2.6 & Hydrophobic \\
G:Q15 & B:11, B:15, B:18 & A, L, R & 1.8 & \cellcolor{saltred}\textbf{H-bond, Salt bridge} \\
G:Y10 & B:7, B:11, B:14, B:47, B:52 & L, A, Q, A, F & 1.7 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:8 W (H-bond with C/E:Q15), B:18 R (\textbf{salt bridge} with G:Q15), B:14 Q (H-bond with G:Y10), B:76 I (H-bond with C:Q15), B:77 V (H-bond with C:K16). Same scaffold as Rank 1, different MPNN sequence. Strongest binding energy (dG = -98.9 REU), largest BSA (3146 \AA$^2$).

\textbf{Sequence:} MPTREKLWWFATAQLLVRHIIEHMRARGDTSQLAQWEADLEILEENARKKIFEIPEDTPIYRLMKTLKENTKGHEIVEE

\normalsize

\newpage

## 3.3 Rank 3: s716952\_mpnn20 (87 aa, 13/18 hotspots --- NEW)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:3 & I & 3.0 & Hydrophobic \\
C:Q15 & B:6, B:8, B:9 & T, V, E & 1.7 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:K16 & B:8 & V & 3.4 & vdW \\
E:E11 & B:58 & M & 4.5 & vdW \\
E:Y10 & B:3, B:4, B:6, B:58 & I, P, T, M & 2.4 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Q15 & B:6, B:7, B:8 & T, I, V & 1.7 & Hydrophobic \\
E:K16 & B:8 & V & 3.5 & vdW \\
G:Y10 & B:4, B:54, B:55, B:58, B:59 & P, V, Y, M, L & 2.2 & Hydrophobic \\
G:E11 & B:49, B:50, B:54, B:58 & D, D, V, M & 2.4 & Hydrophobic \\
G:H13 & B:48, B:49, B:50 & H, D, D & 2.3 & \cellcolor{hydrophgreen}Hydrophobic \\
G:H14 & B:48, B:49 & H, D & 2.0 & \cellcolor{hydrophgreen}Hydrophobic \\
G:Q15 & B:7, B:43, B:46, B:48 & I, H, L, H & 2.1 & Hydrophobic \\
G:K16 & B:7, B:48 & I, H & 4.0 & vdW \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:6 T (H-bond with C:Q15), B:4 P (H-bond with E:Y10), B:48 H (contacts G:H13, G:H14, G:Q15, G:K16 --- multi-hotspot anchor), B:58 M (contacts E:E11, E:Y10, G:E11, G:Y10 --- cross-chain bridge). Only design with 6/6 hotspot contacts on chain G including rare H13/H14.

\textbf{Sequence:} EGIPPTIVESFQFMMEISKVWDAMPEEYRVPLKELFTKLIWLHINLPHDDSEEVYRKMLEAGRLYEEIKKLWEEAMKIPEVRAAAEK

\normalsize

## 3.4 Rank 4: s480128\_mpnn13 (82 aa, 11/18 hotspots)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:3, B:4, B:7 & H, Q, P & 2.6 & Hydrophobic \\
C:Q15 & B:8, B:11, B:12 & K, A, W & 2.2 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:K16 & B:12 & W & 3.5 & Hydrophobic \\
E:E11 & B:14 & Q & 4.9 & vdW \\
E:Y10 & B:3, B:7, B:10, B:11, B:14 & H, P, W, A, Q & 1.7 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Q15 & B:11, B:14, B:15 & A, Q, F & 1.6 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:K16 & B:12, B:15 & W, F & 2.9 & Hydrophobic \\
G:E11 & B:14 & Q & 3.7 & vdW \\
G:Y10 & B:3, B:10, B:14 & H, W, Q & 1.9 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
G:Q15 & B:14, B:15, B:18 & Q, F, F & 1.9 & Hydrophobic \\
G:K16 & B:15, B:18 & F, F & 2.4 & Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:3 H (H-bond with G:Y10), B:7 P (H-bond with E:Y10), B:11 A (H-bond with E:Q15), B:12 W (H-bond with C:Q15). Same scaffold as Rank 5. Zero Met at interface.

\textbf{Sequence:} SFHQKYPKAWAWQQFLEFIVRQILGDTPEAKKIVEEVTSEAEKLLEADKSGELGTTEEGANKLFIEMLTRAFSKVADVLLNP

\normalsize

## 3.5 Rank 5: s480128\_mpnn17 (82 aa, 11/18 hotspots)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:3, B:4, B:7 & H, Q, P & 2.4 & Hydrophobic \\
C:Q15 & B:11, B:12, B:57 & A, W, E & 2.1 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
C:K16 & B:12 & W & 3.3 & Hydrophobic \\
E:E11 & B:10 & W & 4.8 & vdW \\
E:Y10 & B:3, B:7, B:10, B:11 & H, P, W, A & 2.0 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Q15 & B:11, B:12, B:15 & A, W, F & 2.2 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:K16 & B:12, B:15 & W, F & 2.8 & Hydrophobic \\
G:E11 & B:10 & W & 4.4 & vdW \\
G:Y10 & B:3, B:10, B:14 & H, W, Q & 1.9 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
G:Q15 & B:14, B:15, B:18 & Q, F, F & 2.0 & Hydrophobic \\
G:K16 & B:15, B:18, B:22 & F, F, Q & 2.3 & Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:3 H (H-bond with G:Y10), B:7 P (H-bond with E:Y10), B:11 A (H-bond with E:Q15), B:57 E (H-bond with C:Q15). Lowest binder RMSD (0.90 \AA). Zero Met at interface.

\textbf{Sequence:} SFHQKYPKAWAWIQFLRFIVEQILGDTPEAQDIYDTVASEAKEKLEADKSGELGTTEEGANELFIEMLTRAFSLVADVLLNP

\normalsize

\newpage

## 3.6 Rank 6: s967366\_mpnn11 (82 aa, 10/18 hotspots)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Q15 & B:10, B:13 & F, M & 2.1 & Hydrophobic \\
C:K16 & B:10 & F & 2.9 & Hydrophobic \\
E:Y10 & B:13, B:17, B:20 & M, D, Y & 1.9 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Q15 & B:10, B:13, B:14, B:17 & F, M, F, D & 2.1 & Hydrophobic \\
E:K16 & B:10, B:14 & F, F & 2.5 & Hydrophobic \\
G:E11 & B:21, B:25 & A, R & 2.4 & Hydrophobic \\
G:H13 & B:25 & R & 3.8 & vdW \\
G:Q15 & B:13, B:14, B:15, B:17, B:18 & M, F, F, D, Y & 2.2 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
G:K16 & B:14 & F & 2.6 & Hydrophobic \\
G:Y10 & B:20, B:21, B:24, B:25 & Y, A, Y, R & 2.3 & Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:17 D (H-bond with E:Y10), B:14 F (H-bond with G:Q15). Highest pLDDT (0.94), best shape complementarity (0.76). Mostly hydrophobic contacts. Only design reaching G:H13 besides s716952.

\textbf{Sequence:} MPKEVEIWEFLQMFFMDYFYAEIYRGKLSEEEKEIVEKIDKTWQKVIDNMKKNNGVMSEEDQKEMQEVLLDIINLKKKLEEK

\normalsize

## 3.7 Rank 7: s311665\_mpnn6 (68 aa, 9/18 hotspots --- smallest)

\scriptsize
\setlength{\tabcolsep}{3pt}

\begin{longtable}{|l|l|l|c|l|}
\hline
\textbf{Hotspot} & \textbf{Binder Res} & \textbf{AA} & \textbf{Dist (\AA)} & \textbf{Interaction Type} \\
\hline
C:Y10 & B:3, B:6, B:7 & R, L, T & 2.6 & Hydrophobic \\
C:Q15 & B:6, B:7, B:12 & L, T, M & 2.6 & Hydrophobic \\
C:K16 & B:12 & M & 3.4 & vdW \\
E:Y10 & B:1, B:2, B:6 & M, T, L & 1.8 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
E:Q15 & B:11, B:12, B:15, B:16 & F, M, D, M & 2.4 & Hydrophobic \\
E:K16 & B:12, B:16 & M, M & 2.3 & Hydrophobic \\
G:Y10 & B:1, B:11, B:15, B:19, B:32, B:36 & M, F, D, H, Y, I & 2.0 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
G:Q15 & B:15, B:16, B:19, B:20 & D, M, H, L & 2.1 & \cellcolor{hbondblue}\textbf{H-bond}, Hydrophobic \\
G:K16 & B:16, B:20 & M, L & 2.6 & Hydrophobic \\
\hline
\end{longtable}

\small
\textbf{Key binder residues:} B:15 D (H-bond with G:Y10 and G:Q15), B:1 M (H-bond with E:Y10). Smallest binder (68 aa, 7.5 kDa) --- best candidate for bispecific fusion. Symmetric contacts (Y10+Q15+K16 on all 3 chains). Lowest surface hydrophobicity (0.30).

\textbf{Sequence:} MTREMLTDPWFMITDMIYHLFMKDNEEISKKYNEIIENADKMTPEEFREKLMELLVEAVRTWHKRNFE

\normalsize

\newpage

# 4. Binder Interface Residues --- Complete Lists

Binder residues within 5 \AA\ of any target hotspot, classified by interaction type.

\small

## 4.1 s120913\_mpnn1 (24 interface residues contacting hotspots)

| Res | AA | Interactions | Res | AA | Interactions |
|-----|-----|------|-----|-----|------|
| B:2 | D | vdW | B:47 | A | Hydrophobic |
| B:3 | T | Hydrophobic | B:48 | R | vdW |
| B:4 | R | Hydrophobic | B:50 | K | Hydrophobic |
| B:7 | L | Hydrophobic | B:52 | F | Hydrophobic |
| B:8 | **W** | **H-bond**, Hydrophobic | B:74 | H | vdW |
| B:9 | W | vdW | B:75 | K | vdW |
| B:10 | F | vdW | B:76 | I | Hydrophobic |
| B:11 | **A** | **H-bond** | B:77 | **V** | **H-bond** |
| B:12 | **T** | **H-bond**, Hydrophobic | B:78 | E | Hydrophobic |
| B:14 | **Q** | **H-bond**, Hydrophobic | B:79 | **E** | **H-bond, Salt bridge** |
| B:15 | L | Hydrophobic | | | |
| B:18 | **R** | **H-bond, Salt bridge** | | | |

## 4.2 s120913\_mpnn2 (24 interface residues contacting hotspots)

| Res | AA | Interactions | Res | AA | Interactions |
|-----|-----|------|-----|-----|------|
| B:1 | M | vdW | B:47 | A | Hydrophobic |
| B:2 | P | Hydrophobic | B:48 | R | vdW |
| B:3 | T | Hydrophobic | B:50 | K | Hydrophobic |
| B:4 | R | Hydrophobic | B:52 | F | Hydrophobic |
| B:7 | L | Hydrophobic | B:75 | E | vdW |
| B:8 | **W** | **H-bond**, Hydrophobic | B:76 | **I** | **H-bond**, Hydrophobic |
| B:9 | W | vdW | B:77 | **V** | **H-bond** |
| B:10 | F | vdW | B:78 | E | Hydrophobic |
| B:11 | **A** | **H-bond**, Hydrophobic | B:79 | **E** | **H-bond**, Hydrophobic |
| B:12 | **T** | **H-bond**, Hydrophobic | | | |
| B:14 | **Q** | **H-bond**, Hydrophobic | | | |
| B:15 | L | Hydrophobic | | | |
| B:18 | **R** | **H-bond, Salt bridge** | | | |

## 4.3 s716952\_mpnn20 (19 interface residues contacting hotspots)

| Res | AA | Interactions | Res | AA | Interactions |
|-----|-----|------|-----|-----|------|
| B:1 | E | vdW | B:46 | L | vdW |
| B:2 | G | vdW | B:48 | H | Hydrophobic |
| B:3 | I | Hydrophobic | B:49 | D | Hydrophobic |
| B:4 | **P** | **H-bond**, Hydrophobic | B:50 | D | Hydrophobic |
| B:5 | P | vdW | B:51 | S | vdW |
| B:6 | **T** | **H-bond**, Hydrophobic | B:54 | V | Hydrophobic |
| B:7 | I | Hydrophobic | B:55 | Y | Hydrophobic |
| B:8 | V | Hydrophobic | B:58 | M | Hydrophobic |
| B:9 | E | vdW | B:59 | L | Hydrophobic |
| B:43 | H | vdW | | | |

## 4.4 s967366\_mpnn11 (10 interface residues contacting hotspots)

| Res | AA | Interactions |
|-----|-----|------|
| B:10 | F | Hydrophobic |
| B:13 | M | Hydrophobic |
| B:14 | **F** | **H-bond**, Hydrophobic |
| B:15 | F | vdW |
| B:17 | **D** | **H-bond**, Hydrophobic |
| B:18 | Y | Hydrophobic |
| B:20 | Y | vdW |
| B:21 | A | Hydrophobic |
| B:24 | Y | Hydrophobic |
| B:25 | R | vdW |

## 4.5 s311665\_mpnn6 (13 interface residues contacting hotspots)

| Res | AA | Interactions |
|-----|-----|------|
| B:1 | **M** | **H-bond**, Hydrophobic |
| B:2 | T | vdW |
| B:3 | R | vdW |
| B:6 | L | Hydrophobic |
| B:7 | T | vdW |
| B:11 | F | Hydrophobic |
| B:12 | M | Hydrophobic |
| B:15 | **D** | **H-bond**, Hydrophobic |
| B:16 | M | Hydrophobic |
| B:19 | H | Hydrophobic |
| B:20 | L | Hydrophobic |
| B:32 | Y | Hydrophobic |
| B:36 | I | Hydrophobic |

\newpage

# 5. Design Comparison \& Recommendations

## 5.1 Ranking by Application

| Application | Best design | Why |
|-------------|-------------|-----|
| Overall lead | s120913\_mpnn1 | Highest i\_pTM (0.81), 14/18 hotspots, 4 salt bridges, clean |
| Strongest binding | s120913\_mpnn2 | dG=-98.9, 11.5 H-bonds, 3146 \AA$^2$ BSA |
| Broadest chain G coverage | s716952\_mpnn20 | 6/6 on chain G, only design contacting G:H13+H14 |
| Highest confidence | s967366\_mpnn11 | pLDDT=0.94, B\_pLDDT=0.95, B\_RMSD=1.11 |
| Bispecific fusion | s311665\_mpnn6 | Smallest (68 aa), lowest surf.hydro (0.30), clean |
| Structural consistency | s480128\_mpnn17 | B\_RMSD=0.90 \AA, most stable fold |

## 5.2 Key Observations

\begin{itemize}
\item \textbf{4 unique scaffolds} produced 7 accepted designs (s120913: 2, s480128: 2, s967366: 1, s311665: 1, s716952: 1).
\item \textbf{All designs are helical} (65--85\% helix), with no significant beta-sheet content.
\item \textbf{Salt bridges only in s120913 scaffold} --- B:18 R with G:Q15 and B:79 E with E:K16. These electrostatic interactions likely contribute to its superior i\_pTM.
\item \textbf{Q15 and K16 are universal anchor points} --- contacted by every design on every chain.
\item \textbf{H13/H14 are druggability gaps} --- only 2 of 7 designs contact them. Designs with these contacts (s120913, s716952) have the broadest hotspot coverage.
\item \textbf{Binding is predominantly hydrophobic} --- only 2/7 designs have salt bridges. H-bond counts range 4--13, while hydrophobic contact pairs range 142--203.
\end{itemize}

# 6. File Locations

| File | Path |
|------|------|
| Accepted PDBs | \texttt{bindcraft/designs/Accepted/*.pdb} |
| Full metrics | \texttt{bindcraft/designs/final\_design\_stats.csv} |
| This report | \texttt{docs/accepted\_models\_info.pdf} |
| Design report (full campaign) | \texttt{docs/bindcraft\_design\_report.pdf} |
