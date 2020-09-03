'''
    CLUBB standard variables 
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


def clubb_std_prf (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs, casedir,varis,vname,cscale,chscale,pname):

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
 alphas   = ['a) ','b) ','c) ','d) ','e) ','f) ','g) ','h) ','i) ', 'j) ', 'k) ', 'l) ', 'm) ', 'n) ', 'o) ', 'p) ', 'q) ', 'r) ', 's) ', 't) ', 'u) ', 'v) ', 'w) ', 'x) ', 'y) ', 'z) ']

 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

 nvaris = len(varis)

 plotstd=["" for x in range(nsite)]


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     plotstd[ire] = pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     wks= Ngl.open_wks(ptype,plotname)

     Ngl.define_colormap(wks,"GMT_paired")
     plot = []
     res     = Ngl.Resources()
     res.nglMaximize          =  False
     if (lats[ire] > 0 and lons[ire]<230 ):
         res.trYMinF = 400.
         res.trYMaxF = 1000.
     else:
         res.trYMinF = 700.
         res.trYMaxF = 1000.

     res.nglDraw              = False
     res.nglFrame             = False
     res.lgLabelFontHeightF     = .02                   # change font height
     res.lgPerimOn              = False                 # no box around
     res.vpWidthF         = 0.30                      # set width and height
     res.vpHeightF        = 0.30
     res.vpXF             = 0.04
     res.vpYF             = 0.30
     res.tmYLLabelFont  = _Font
     res.tmXBLabelFont  = _Font
     res.tiYAxisFont =  _Font
     res.tiXAxisFont =  _Font

     res.tmXBLabelFontHeightF = 0.01
     res.tmXBLabelFontThicknessF = 2.0
     res.xyMarkLineMode      = "Lines"
     res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,3.,3.,3.,3,3,3,3,3,3,3]

     res.xyDashPatterns    = np.arange(0,24,1)
#     res.xyMarkers         = np.arange(16,40,1)
#     res.xyMarkerSizeF       = 0.005

     res.tiYAxisString   = "Pressure [hPa]"


     for iv in range (0, nvaris):   
         if(iv == nvaris-1):
             res.pmLegendDisplayMode    = "NEVER"
             res.xyExplicitLegendLabels = casenames[:]
             res.pmLegendSide           = "top"
             res.pmLegendParallelPosF   = 0.6
             res.pmLegendOrthogonalPosF = -0.5
             res.pmLegendWidthF         = 0.10
             res.pmLegendHeightF        = 0.10
             res.lgLabelFontHeightF     = .02
             res.lgLabelFontThicknessF  = 1.5
             res.lgPerimOn              = True
         else:
             res.pmLegendDisplayMode    = "NEVER"


#         if(obsdataset[iv] =="CCCM"):
#             if(cseason == "ANN"):
#                 fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-"+cseason+".nc"
#             else:
#                 fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-2010-"+cseason+".nc"
#             inptrobs = Dataset(fileobs,'r')
#             B=inptrobs.variables[varisobs[iv]][:,(lats[ire]),(lons[ire])]
#         else:
#             if (varisobs[iv] =="PRECT"):
#                 fileobs = filepathobs+'/GPCP_'+cseason+'_climo.nc'
#             else:
#                 fileobs = filepathobs + obsdataset[iv]+'_'+cseason+'_climo.nc'
#             inptrobs = Dataset(fileobs,'r')
#             if (varisobs[iv] =="THETA"):
#                 B = inptrobs.variables['T'][0,:,(lats[ire]),(lons[ire])]
#                 pre1 = inptrobs.variables['lev'][:]
#                 for il1 in range (0, len(pre1)):
#                     B[il1] = B[il1]*(1000/pre1[il1])**0.286
#             else: 
#                 pre1 = inptrobs.variables['lev'][:]
#                 B = inptrobs.variables[varisobs[iv]][0,:,(lats[ire]),(lons[ire])]
#
#         B[:]=B[:] * cscaleobs[iv]


         for im in range (0,ncases):
             ncdfs[im]  = './data/'+cases[im]+'_site_location.nc'
             infiles[im]= filepath[im]+cases[im]+'/'+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             lev=inptrs.variables['ilev'][:]
             nlev=len(lev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             ncdf.close()
             if (im ==0):
                 A_field = np.zeros((ncases,nlev),np.float32)

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if (varis[iv] == 'THETA'):
                     tmp = inptrs.variables['T'][0,:,npoint]
                     hyam =inptrs.variables['hyam'][:]
                     hybm =inptrs.variables['hybm'][:]
                     ps=inptrs.variables['PS'][0,npoint] 
                     ps=ps
                     p0=inptrs.variables['P0']
                     pre = np.zeros((nlev),np.float32)
                     for il in range (0, nlev):
                         pre[il] = hyam[il]*p0 + hybm[il] * ps
                         tmp[il] = tmp[il] * (100000/pre[il])**0.286
                     theunits=str(chscale[iv])+inptrs.variables['T'].units

                 else:
                     tmp=inptrs.variables[varis[iv]][0,:,npoint]
#                     tmp2=inptrs.variables['C6rt_Skw_fnc'][0,:,npoint]
#                     tmp3=inptrs.variables['tau_zm'][0,:,npoint]
#                     tmp4=inptrs.variables['tau_wpxp_zm'][0,:,npoint]
                     theunits=str(chscale[iv])+inptrs.variables[varis[iv]].units
                     if (varis[iv] == 'tau_zm' or varis[iv] == 'tau_wp2_zm' \
                        or varis[iv] == 'tau_wp3_zm' or varis[iv] == 'tau_xp2_zm' \
                        or varis[iv] == 'tau_no_N2_zm' or varis[iv] == 'tau_wpxp_zm'):
                        tmp=1/tmp
                        tmp [0:10] = 0.0
                        theunits=str(chscale[iv])+inptrs.variables[varis[iv]].units+'^-1'



                 A_field[im,:] = (A_field[im,:]+tmp[:]/n[ire]).astype(np.float32 )
             A_field[im,:] = A_field[im,:] *cscale[iv]

             inptrs.close()

         res.tiXAxisString   = vname[iv]+"  Unit=  " + theunits

         res.trYReverse        = True
         res.xyLineColors      = np.arange(3,20,2)
         res.xyMarkerColors    = np.arange(2,20,2)
         p = Ngl.xy(wks,A_field,lev,res)
         
         plot.append(p)


     pres            = Ngl.Resources()
     pres.nglFrame = False
     pres.txFont = _Font
     pres.nglMaximize = False
     pres.txFont     = _Font
#     pres.nglPanelYWhiteSpacePercent = 5
#     pres.nglPanelXWhiteSpacePercent = 5
#     pres.wkPaperWidthF  = 17  # in inches
#     pres.wkPaperHeightF = 28  # in inches
     pres.nglPanelTop                      = 0.935
     pres.nglPanelFigureStrings            = alphas
     pres.nglPanelFigureStringsJust        = 'Topleft'
     pres.nglPanelFigureStringsFontHeightF = 0.015

     pres.gsnPaperOrientation= "Landscape"

     txres = Ngl.Resources()
     txres.txFontHeightF = 0.02
     txres.txFont        = _Font
     Ngl.text_ndc(wks,"CLUBB VAR at "+ str(lons[ire])+"E,"+str(lats[ire])+"N",0.5,0.75,txres)
     Common_functions.create_legend(wks,casenames,0.015,np.arange(3,20,2),0.3,0.59+ncases*0.01)

     Ngl.panel(wks,plot[:],[nvaris/2,2],pres)
     Ngl.frame(wks)
     Ngl.destroy(wks)

 return plotstd


     

