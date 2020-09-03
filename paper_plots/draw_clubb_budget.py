'''
    CLUBB budgets
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''
  

import Ngl
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import os
import Common_functions

from subprocess import call

 
def draw_clubb_bgt (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)


 _Font   = 25
 interp = 2
 extrap = False
 mkres = Ngl.Resources()
 mkres.gsMarkerIndex = 2
 mkres.gsMarkerColor = "Red"
 mkres.gsMarkerSizeF = 15.   
 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite
 nvaris = len(varis)
 plotbgt=["" for x in range(nsite*ncases)] 
 alphas   = ['a) ','b) ','c) ','d) ','e) ','f) ','g) ','h) ','i) ', 'j) ', 'k) ', 'l) ', 'm) ', 'n) ', 'o) ', 'p) ', 'q) ', 'r) ', 's) ', 't) ', 'u) ', 'v) ', 'w) ', 'x) ', 'y) ', 'z) ']

 for ire in range (0, nsite):
     for im in range (0,ncases):
         if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
             os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

         plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
         plotbgt[im+ncases*ire] = pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

         wks= Ngl.open_wks(ptype,plotname)

         Ngl.define_colormap(wks,"radar")
         plot = []
         res     = Ngl.Resources()  
         res.nglDraw              = False
         res.nglFrame             = False
         res.nglScale               = False
#         res.vpWidthF         = 0.40                      # set width and height
#         res.vpHeightF        = 0.40
#         res.vpXF             = 0.04
#         res.vpYF             = 0.30
         res.nglMaximize          =  False
         if (lats[ire] > 0 and lons[ire]<230 ):
             res.trYMinF = 400.
             res.trYMaxF = 1000.
         else:
             res.trYMinF = 700.
             res.trYMaxF = 1000.


         res.tiMainFont        = _Font
         res.tmYLLabelFont  = _Font
         res.tmXBLabelFont  = _Font
         res.tiYAxisFont =  _Font
         res.tiXAxisFont =  _Font

         res.tmXBLabelFontHeightF = 0.02
         res.tmXBLabelFontThicknessF = 1.0
         res.xyMarkLineMode      = "MarkLines"
         res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,2.,2.,2.,2,2,2,2,2,2,2]
         res.xyLineColors      = np.arange(1,16,4)
         res.xyDashPatterns    = np.arange(0,24,1)
         res.xyMarkers         = np.arange(16,40,1)
         res.xyMarkerSizeF       = 0.005
         res.xyMarkerColors      = np.arange(1,16,4)

         res.pmLegendDisplayMode    = "NEVER"
         res.pmLegendSide           = "top"                 # Change location of
         res.pmLegendParallelPosF   = 0.75                  # move units right
         res.pmLegendOrthogonalPosF = -0.65                  # more neg = down
         res.pmLegendWidthF         = 0.05                   # Change width and
         res.pmLegendHeightF        = 0.06                  # height of legend.
         res.lgLabelFontHeightF     = 0.03                     # change font height
         res.lgLabelFontThicknessF  = 1.

#         res.lgBoxMinorExtentF      = 0.5
         res.lgPerimOn              = False
         res.tiYAxisString   = "Pressure [hPa]"
         res.tmYLLabelFontHeightF = 0.02

     
         res.trYReverse        = True

         res1 = Ngl.Resources()
         res1 = res

         pres            = Ngl.Resources() 
#         pres.gsnPaperOrientation= "Landscape"

#         pres.wkPaperWidthF  = 20  # in inches
#         pres.wkPaperHeightF = 28  # in inches

         pres.nglMaximize = False
#         pres.vpWidthF         = 0.40                      # set width and height
#         pres.vpHeightF        = 0.40

         pres.nglFrame = False
         pres.txFont = _Font
         pres.nglPanelYWhiteSpacePercent = 5
         pres.nglPanelXWhiteSpacePercent = 3
         pres.nglPanelTop    = .9
#         pres.nglPanelBottom=0.3
#         pres.nglPanelLeft= 0.2
#         pres.nglPanelRight= 0.95
         pres.nglPanelFigureStrings            = alphas
         pres.nglPanelFigureStringsJust        = 'Topleft'
         pres.nglPanelFigureStringsFontHeightF = 0.015



         for iv in range (0, nvaris):

             if (varis[iv] == "rtp2" or varis[iv] == "thlp2"):
                 budget_ends = ["_ta", "_tp", "_dp1"]
                 budget_name = ['~F10~turb adv', '~F10~turb prod','~F10~dissipation']
                 nterms = len (budget_ends)
             if (varis[iv] == "wprtp") :
                 budget_ends = ["_bt", "_ma", "_ta", "_tp", "_ac","_bp","_pr1","_pr2", "_pr3","_dp1","_mfl", "_cl", "_sicl","_pd", "_forcing"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)
             if (varis[iv] == "wpthlp") :
                 budget_ends = ["_tp","_bp","_pr1"]
                 budget_name = ['~F10~turb prod','~F10~buoy+pres','~F10~ret to iso']
                 nterms = len (budget_ends)

             if (varis[iv] == "rtpthlp") :
                 budget_ends = ["_bt", "_ma", "_ta", "_tp1","_tp2","_dp1","_dp2", "_cl", "_sf", "_forcing"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)
             if (varis[iv] == "wp2") :
                 budget_ends = [ "_ta", "_bp","_pr1","_dp1","_dp2"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)

             if (varis[iv] == "wp3") :
                 budget_ends = [ "_ta", "_tp", "_bp1","_bp2","_pr1","_pr2","_dp1"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)

             if (varis[iv] == "up2" or varis[iv] == "vp2") :
                 budget_ends = ["_bt", "_ma", "_ta", "_tp", "_dp1", "_dp2","_pr1","_pr2" ,"_cl", "_pd", "_sf"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)

             if (varis[iv] == "um" or varis[iv] == "vm") :
                 budget_ends = ["_bt", "_ma","_ta","_gf",  "_f"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)
         
             if (varis[iv] == "thlm" or varis[iv] == "rtm") :
                 budget_ends = ["_bt", "_ma","_ta","_cl",  "_mc"]
                 budget_name = budget_ends
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_no_N2_zm' ):
                 budget_ends = ['tau_no_N2_zm', 'bkgnd',  'sfc',  'shear']
                 budget_name = ['~F8~t~N~~F25~~B~noN2~N~','~F8~t~N~~F25~~B~bkgnd~N~','~F8~t~N~~F25~~B~shear~N~','~F8~t~N~~F25~~B~shear~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_xp2_zm' ):
                 budget_ends = [ 'tau_xp2_zm', 'tau_no_N2_zm']
                 budget_name = ['~F8~t~N~~F25~~B~x`~S~2~N~~N~','~F8~t~N~~F25~~B~noN2~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wp2_zm' ):
                 budget_ends = ['tau_wp2_zm',  'tau_no_N2_zm', 'bvpos']
                 budget_name = ['~F8~t~N~~F25~~B~w`~S~2~N~~N~','~F8~t~N~~F25~~B~noN2~N~','~F8~t~N~~F25~~B~bv~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wpxp_zm' ):
                 budget_ends = ['tau_wpxp_zm', 'tau_no_N2_zm', 'bvpos', 'clear']
                 budget_name = ['~F8~t~N~~F25~~B~w`x`~N~','~F8~t~N~~F25~~B~noN2~N~','~F8~t~N~~F25~~B~bv~N~','~F8~t~N~~F25~~B~clr~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wp3_zm' ):
                 budget_ends = [ 'tau_wp3_zm', 'tau_no_N2_zm', 'bvpos', 'clear']
                 budget_name = ['~F8~t~N~~F25~~B~w`~S~3~N~~N~','~F8~t~N~~F25~~B~noN2~N~','~F8~t~N~~F25~~B~bv~N~','~F8~t~N~~F25~~B~clr~N~']
                 nterms = len (budget_ends)



             ncdfs[im]  = './data/'+cases[im]+'_site_location.nc'
             infiles[im]= filepath[im]+cases[im]+'/'+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             ilev=inptrs.variables['ilev'][:]
             nilev=len(ilev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             ncdf.close()
             A_field = np.zeros((nterms,nilev),np.float32)

         
             for it in range(0, nterms):
                 for subc in range( 0, n[ire]):
                     npoint=idx_cols[ire,n[subc]-1]-1

                     varis_bgt=varis[iv]+budget_ends[it]
                     tmp0=inptrs.variables[varis[iv]][0,:,npoint]
                     theunits0="~F25~"+inptrs.variables[varis[iv]].units

                     if (varis[iv] == 'wpthlp' and budget_ends[it] == '_bp' ):
                        tmp=inptrs.variables[varis_bgt][0,:,npoint] +inptrs.variables['wpthlp_pr3'][0,:,npoint]
                     else:
                        tmp=inptrs.variables[varis_bgt][0,:,npoint] 
                     theunits=str(chscale[iv])+"~F25~"+inptrs.variables[varis[iv]+'_bt'].units
                         

                     if (varis[iv] == "wprtp" or varis[iv] == "thlp2") :
                         tmp [0:10] = 0.0
                         tmp0 [0:10] = 0.0
                     txres = Ngl.Resources()
                     txres.txFontHeightF = 0.02
                     txres.txFont        = _Font


                     tmp=tmp*cscale[iv]
                     A_field[it,:] = (A_field[it,:]+tmp[:]/n[ire]).astype(np.float32 )

             inptrs.close()
             res.tiXAxisString   = vname[iv]+'  Unit=  ' + theunits


             if (varis[iv] == "wpthlp" or varis[iv] == "thlp2" or varis[iv] == "wp3" or varis[iv] == "wp2") :
                res1.tiXAxisString   = vname[iv]+'  Unit=  ' + theunits0
                p0= Ngl.xy(wks,tmp0,ilev,res1)
                plot.append(p0)


             if(varis[iv] == 'wpthlp'):
               if ( lons[ire] < 230 ) :
                 res.trXMinF = -1.
                 res.trXMaxF =  1.
                 Common_functions.create_legend(wks,budget_name,0.013,np.arange(1,16,4),0.77,0.85-iv*0.45)
               else:
                 res.trXMinF = -0.4
                 res.trXMaxF =  0.4
                 Common_functions.create_legend(wks,budget_name,0.013,np.arange(1,16,4),0.77,0.85-iv*0.45)


             if(varis[iv] =='thlp2' ):
               if( lons[ire]< 230 ) :
                 res.trXMinF = -2.8
                 res.trXMaxF =  2.8
                 Common_functions.create_legend(wks,budget_name,0.013,np.arange(1,16,4),0.77,0.85-iv*0.45)
               else:
                 res.trXMinF = -1.
                 res.trXMaxF =  1.
                 Common_functions.create_legend(wks,budget_name,0.013,np.arange(1,16,4),0.77,0.85-iv*0.45)


             res.tiXAxisString   = vname[iv]+'  Unit=  ' + theunits
             p = Ngl.xy(wks,A_field,ilev,res)
             plot.append(p)

             del(res.trXMaxF)
             del(res.trXMinF)
             xp=np.mod(iv,2)
             yp=int(iv/2)

         Ngl.panel(wks,plot[:],[nvaris,2],pres)
         txres = Ngl.Resources()
         txres.txFont = _Font
         txres.txFontHeightF = 0.02
         
         Ngl.text_ndc(wks,casenames[im]+"  BUDGET at " +str(lons[ire])+"E,"+str(lats[ire])+"N",0.5,0.91,txres)
         Ngl.frame(wks)
         Ngl.destroy(wks) 

 return (plotbgt)

