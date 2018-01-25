# Original author: Sadjad Fouladi

set terminal svg enhanced size 1500, 500 background rgb 'white' font 'Arial,18'
set output 'graph.svg'

unset clip points
set clip one
unset clip two
set bar 1.000000 front
set border 9 front lt black lc '#000000' linewidth 0.5 dashtype solid

set zdata
set ydata
set xdata
set y2data
set x2data
set boxwidth 0.9
set style fill solid 1.00 noborder
set style rectangle back fc  bgnd fillstyle   solid 1.00 border lt -1
set style circle radius graph 0.02, first 0.00000, 0.00000
set style ellipse size graph 0.05, 0.03, first 0.00000 angle 0 units xy
set dummy x, y
set format x "% h"
set format y "% h"
set format x2 "% h"
set format y2 "% h"
set format z "% h"
set format cb "% h"
set format r "% h"
set timefmt "%d/%m/%y,%H:%M"
set angles radians
set tics back
unset grid
set raxis
set style parallel front  lt black linewidth 2.000 dashtype solid
set key left top inside Left reverse font "Arial, 20" samplen 1.5 spacing 1
#unset label
#unset arrow
set style increment default
unset style line
unset style arrow
set style histogram rowstacked title textcolor lt -1
unset object
set style textbox transparent margins  1.0,  1.0 border
unset logscale
set offsets 0, 0, 0, 0
set pointsize 1
set pointintervalbox 1
set encoding default
unset polar
unset parametric
unset decimalsign
#unset minussign
set view 60, 30, 1, 1
set samples 100, 100
set isosamples 10, 10
set surface
unset contour
set cntrlabel  format '%8.3g' font '' start 5 interval 20
set mapping cartesian
set datafile separator whitespace
unset hidden3d
set cntrparam order 4
set cntrparam linear


set cntrparam levels auto 5
set cntrparam points 5
set size ratio 0 1,1
set origin 0,0
set style data histograms
set style function lines
unset xzeroaxis
unset yzeroaxis
unset zzeroaxis
unset x2zeroaxis
unset y2zeroaxis
set xyplane relative 0.5
set tics scale  1, 0.5, 1, 1, 1
set mxtics default
set mytics default
set mztics default
unset mx2tics
unset my2tics
set mcbtics default
set mrtics default
set xtics border in scale 0,0 nomirror norotate  autojustify
set y2tics border in scale 0,0 nomirror norotate  autojustify
set ztics border in scale 1.5,0.5 nomirror norotate  autojustify
set ztics  norangelimit autofreq
set xtics font "Arial, 24"
set y2tics font "Arial, 24"
unset x2tics
unset ytics
set cbtics border in scale 1,0.5 mirror norotate  autojustify
set cbtics  norangelimit autofreq
set rtics axis in scale 1,0.5 nomirror norotate  autojustify
set rtics  norangelimit autofreq
unset paxis 1 tics
unset paxis 2 tics
unset paxis 3 tics
unset paxis 4 tics
unset paxis 5 tics
unset paxis 6 tics
unset paxis 7 tics
set title ""
set title  font "" norotate
set timestamp bottom
set timestamp ""
set timestamp  font "" norotate
set rrange [ * : * ] noreverse nowriteback
set trange [ * : * ] noreverse nowriteback
set urange [ * : * ] noreverse nowriteback
set vrange [ * : * ] noreverse nowriteback
set xlabel "worker #"
set xlabel  font "Arial, 28" textcolor lt -1 norotate  offset 0, 0

set x2label ""
set x2label  font "" textcolor lt -1 norotate
set x2range [ * : * ] noreverse nowriteback
set y2label "time (s)"
set y2label font "Arial, 28" textcolor lt -1 rotate by -270 offset -1, 0
set ylabel ""
set ylabel  font "" textcolor lt -1 rotate by -270
set yrange [ * : * ] noreverse nowriteback
set y2range [ * : * ] noreverse nowriteback
set zlabel ""
set zlabel  font "" textcolor lt -1 norotate
set zrange [ * : * ] noreverse nowriteback
set cblabel ""
set cblabel  font "" textcolor lt -1 rotate by -270
set cbrange [ * : * ] noreverse nowriteback
set paxis 1 range [ * : * ] noreverse nowriteback
set paxis 2 range [ * : * ] noreverse nowriteback
set paxis 3 range [ * : * ] noreverse nowriteback
set paxis 4 range [ * : * ] noreverse nowriteback
set paxis 5 range [ * : * ] noreverse nowriteback
set paxis 6 range [ * : * ] noreverse nowriteback
set paxis 7 range [ * : * ] noreverse nowriteback
set zero 1e-08
set lmargin  -1
set bmargin  -1
set rmargin  6.5
set tmargin  -1
set locale "en_US.UTF-8"
set pm3d explicit at s
set pm3d scansautomatic
set pm3d interpolate 1,1 flush begin noftriangles noborder corners2color mean
set palette positive nops_allcF maxcolors 0 gamma 1.5 color model RGB
set palette rgbformulae 7, 5, 15
set colorbox default
#set colorbox vertical origin screen 0.9, 0.2, 0 size screen 0.05, 0.6, 0 front  noinvert bdefault
set style boxplot candles range  1.50 outliers pt 7 separation 1 labels auto unsorted
set loadpath
set fontpath
set psdir
set fit brief errorvariables nocovariancevariables errorscaling prescale nowrap v5

x = 0.0
## Last datafile plotted: "timing_data"
plot "timing_data" using 2 t "" lc rgb "white", \
                "" using 3 t "" lc rgb "#377eb8", \
                "" using 4 t "" lc rgb "#377eb8", \
                "" using 5 t "Fetching dependencies" lc rgb "#377eb8", \
                "" using 6 t "Executing the thunk" lc rgb "#4daf4a", \
                "" using 7 t "" lc rgb "#e41a1c", \
		"" using 8 t "Uploading the results" lc rgb "#e41a1c"

