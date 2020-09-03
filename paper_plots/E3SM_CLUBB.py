# -*- coding: utf-8 -*-
'''
E3SM CLUBB Diagnostics package 

Main code to make 1) 2D plots,2) profiles, 3) budgets on selected stations, 
         and then build up  webpages  etc
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''

## ==========================================================
# Begin User Defined Settings
# User defined name used for this comparison, this will be the name 
#   given the directory for these diagnostics
case='paper4' # A general case name
outdir='/lcrc/group/acme/zhun/plots/' # Location of plots

filepath=[ \
'/lcrc/group/acme/ac.zguo/E3SM_simulations/',\
'/lcrc/group/acme/ac.zguo/E3SM_simulations/',\
'/lcrc/group/acme/ac.zguo/E3SM_simulations/',\
'/lcrc/group/acme/ac.zguo/E3SM_simulations/',\
'/lcrc/group/acme/ac.zguo/E3SM_simulations/',\
'/lcrc/group/acme/zhun/E3SM_simulations/',\
          ]
cases=[ \
#'anvil.E3SM_v1.golaz.ne16_ne16',\
#'anvil.E3SM_v1.golaz.ne30_ne30',\
'anvil.EAMv1.F2010SC5-CMIP6_t1.ne30_ne30',\
#'anvil-centos7.base.revxp2_c15p5_all1_n2p65_wp2p2_bk1p5_alt.ne16_ne16',\
#'anvil-centos7.base.c15p5_all1_n2p65_bk1p5_alt.ne30_ne30',\
#'anvil-centos7.base2.wpxpri_3p5e4_1_2p5_0_12_C7ri.ne30_ne30',\
'anvil-centos7.base2.wpxpri_3p3e4_1_3_0_12_C7ri.ne30_ne30',\
#'anvil-centos7.base.wpxpxp2_c15p5_all1_n2p65_bk1p5_alt.ne16_ne16',\
#'anvil-centos7.base.damp5_cxminp8.ne16_ne16',\
#'anvil-centos7.base.damp5_cxminp6.ne16_ne16',\

]

       
# Give a short name for your experiment which will appears on plots

casenames=[
#'E3SMv1_2d',\
'EAM-def',\
#'base_20200608_2d',\
'EAM-taus',\
#'taus-sens',\
#'cxminp8',\
#'cxminp6',\

]

years=[\
        '1', '1','1', '1','1','1']
nyear=[\
        1, 1, 1, 1,1,1]
dpsc=[\
      'none','none','none','none','none','none']
# NOTE, dpsc,deep scheme, has to be 'none', if silhs is turned on. 

# Observation Data
#filepathobs='/global/project/projectdirs/m2689/zhun/amwg/obs_data_20140804/'
filepathobs='/blues/gpfs/home/ac.zguo/amwg_diag_20140804/obs_data_20140804/'
#------------------------------------------------------------------------
# Setting of plots.
ptype         ='eps'   # eps, pdf, ps, png, x11, ... are supported by this package
cseason       ='JJA' # Seasons, or others
casename      =case+'_'+cseason

#------------------------------------------------------------------------
calmean          = False       # make mean states
findout          = True        # pick out the locations of your sites
drawlarge        = True        # profiles for large-scale variable on your sites 
drawclubb        = True        # profiles for standard clubb output
drawtaubgt       = False
drawbgt          = False        # budgets of CLUBB prognostic Eqs 

makeweb          = False        # Make a webpage?
maketar          = False        # Tar them?

clevel = 500
area  = 1
# Note, this para helps to find out the 'ncol' within
# lats - area < lat(ncol) < lons + area .and. lons- area < lon(ncol) < lons + area
#------------------------------------------------------------------------
# Please give the lat and lon of sites here.
# sites    1    2    3   14    27   28   29
lats = [   20, 32,  2,  0,  27, 30]
lons = [  205,239,140,295, 240, 240]


#========================================================================

#------------------------------------------------------------------------
# Do not need to change
#------------------------------------------------------------------------

ncases =len(cases)
nsite  =len(lats)

casedir=outdir+casename
print(casedir)

import os
import function_cal_mean
import function_pick_out
import draw_large_scale
import draw_clubb_standard
import draw_clubb_budget
import draw_clubb_tau
import Common_functions
import Diagnostic_webpage

casedir=outdir+casename

if not os.path.exists(casedir):
    os.mkdir(casedir)

if calmean:
    print('Getting climatological mean')
    function_cal_mean.cal_mean(ncases, cases, years,nsite, lats, lons, area, filepath)

if findout:
    print('Find out the sites')
    function_pick_out.pick_out(ncases, cases, years, nsite, lats, lons, area, filepath,casedir)

if drawlarge:
    print('Drawing Large-scale variables on selected sites')
    plotlgs=draw_large_scale.large_scale_prf(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir)

if drawclubb:
    print('Drawing CLUBB standard variables on selected sites')

    pname = 'std1'
    varis    = [ 'wp2','wp3'] #'up2','vp2','rtp2','thlp2','wp3']
    vname   = [ "~V25~~F19~9~V-30~~H-40~~F10~w~N~'~S~~F25~2~N~","~V25~~F19~9~V-30~~H-40~~F10~w~N~'~S~~F25~3~N~"]
    cscale   = [  100,   100 ]
    chscale  = [   '10~S~-2~N~', '10~S~-2~N~']
    plotstd1=draw_clubb_standard.clubb_std_prf(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname)

    pname = 'std2'
    varis    = [ 'wpthlp', 'thlp2' ]
    vname    = [ "~V20~~F19~9~V-25~~H-50~~F10~w'~F8~q'~B~~F10~l~N~~F25~", "~V20~~F19~9~V-25~~H-40~~F8~q'~B~~F10~l~N~~S~2~N~~F25~" ]

    cscale   = [        1,  1 ]
    chscale  = [      '1',  '1' ]

    plotstd2=draw_clubb_standard.clubb_std_prf(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname)

if drawtaubgt:
    print('tau')
    pname = 'taubgt'

    vname   = [ "no_N2", "~F~w'x'~N~","~F~w~N~'~S~2~N~","~F~x~N~'~S~2~N~"]
    varis   = [ 'tau_no_N2_zm', 'tau_wp3_zm', 'tau_wp2_zm', 'tau_xp2_zm'] 

    cscale  = [               1E3,              1E3,            1E3,           1E3,     1E3,         1E3,         1E3,         1E3,            1E3]
    chscale = [            '10~S~-3~N~',      '10~S~-3~N~', '10~S~-3~N~',        '10~S~-3~N~',  '1E-3',      '1E-3',      '1E-3',      '1E-3',         '1E-3']
    plottaubgt=draw_clubb_tau.draw_clubb_tau(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname)


if drawbgt:
    print('Drawing CLUBB BUDGET')
    varis   = [ 'wp2','wp3']#,'up2','vp2']
    vname   = [ "~V20~~F19~9~V-25~~H-40~~F10~w~N~'~S~2~N~","~V20~~F19~9~V-25~~H-40~~F10~w~N~'~S~3~N~"]
    cscale  = [  1E3,  1E3,    1,    1]
    chscale = ['10~S~-3~N~','10~S~-3~N~',  '1',  '1']
    pname = 'Budget1'
#    plotbgt1=draw_clubb_budget.draw_clubb_bgt(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname)

    varis    = ['wpthlp',  'thlp2']
    vname    = [ "~V20~~F19~9~V-25~~H-50~~F10~w'~F8~q'~B~~F10~l~N~~F25~", "~V20~~F19~9~V-25~~H-40~~F8~q'~B~~F10~l~N~~S~2~N~~F25~" ]

    cscale   = [     1E3,      1E3]
    chscale  = [ '10~S~-3~N~', '10~S~-3~N~']
    pname = 'Budget2'
    plotbgt2=draw_clubb_budget.draw_clubb_bgt(ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname)   



if makeweb:
    print('Making webpages')
    Diagnostic_webpage.main_web(casename,casedir)

    Diagnostic_webpage.sets_web(casename,casedir,'diff.*.asc','txt',\
                                'Gitdiff','1000','1000')

    if (draw2d):
        plot2d.extend(plot3d[:])
        if (drawclm):
            plot2d.extend(plotclm[:])

        Diagnostic_webpage.sets_web(casename,casedir,plot2d,'2D',\
				'Horizontal Plots','1000','1000')



    for ire in range (0, nsite):
        plotclb=[]
        if (drawlarge):
           plotclb.append(plotlgs[ire])
        if (drawclubb):  
           plotclb.append(plotstd1[ire])
           plotclb.append(plotstd2[ire])
           plotclb.append(plotstd3[ire])
           plotclb.append(plotstd4[ire])
#           plotclb.append(plottau[ire])

        if (drawskw):
           plotclb.append(plotskw[ire])
        if (drawhf):
           plotclb.append(plothf[ire])
        if (drawrain):
           plotclb.append(plotrain[ire])
           plotclb.append(plotsnow[ire])
           plotclb.append(plotsnum[ire])
           plotclb.append(plotsqm[ire])

        if (drawaero):
           plotclb.append(plotsaero1[ire])
           plotclb.append(plotsaero2[ire])
           plotclb.append(plotsaero3[ire])


        if (drawmicrobgt):
           for im in range (0, ncases ):
               plotclb.append(plotmicrobgt1[ire*ncases+im])
#               plotclb.append(plotmicrobgt2[ire*ncases+im])

        if (drawe3smbgt):
           for im in range (0, ncases ):
               plotclb.append(plote3smbgt[ire*ncases+im])

        if (drawbgt):
           for im in range (0, ncases ):
               plotclb.append(plotbgt1[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt2[ire*ncases+im])
#           for im in range (0, ncases ):
#               plotclb.append(plotbgt3[ire*ncases+im])

        Diagnostic_webpage.sets_web(casename,casedir,plotclb,str(lons[ire])+'E_'+str(lats[ire])+'N',\
                                  'Profiles on '+str(lons[ire])+'E_'+str(lats[ire])+'N','908','636')

if maketar:
    print('Making tar file of case')
    Common_functions.make_tarfile(outdir+casename+'.tar',outdir+casename)
    
