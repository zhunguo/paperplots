'''
    Large-scale variables (compared with observations)
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''


import Ngl
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
#import pylab
import Common_functions
import os
from subprocess import call

def large_scale_prf (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs, casedir):


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
 mkres.gsMarkerColor = 'Red'
 mkres.gsMarkerSizeF = 15.
 infiles  = ['' for x in range(ncases)]
 ncdfs    = ['' for x in range(ncases)]
 nregions = nsite
 localnames=np.append('ERAI',casenames)
 varis    = [ 'CLOUD'  , 'CLDLIQ', 'THETA','RELHUM']
 varisobs = ['CC_ISBL', 'CLWC_ISBL', 'THETA','RELHUM' ]
 alphas   = ['a) ','b) ','c) ','d) ','e) ','f) ','g) ','h) ','i) ', 'j) ', 'k) ', 'l) ', 'm) ', 'n) ', 'o) ', 'p) ', 'q) ', 'r) ', 's) ', 't) ', 'u) ', 'v) ', 'w) ', 'x) ', 'y) ', 'z) ']

 nvaris = len(varis)
 cunits = ['%','g/kg','K', '%' ]
 cscale = [100, 1000 , 1.,   1 ]
 cscaleobs = [100, 1000 , 1.,   1,     1,   1000,     1,1,1,1,1,1,1]
 obsdataset =['ERAI', 'ERAI', 'ERAI', 'ERAI', 'ERAI', 'ERAI', 'ERAI', 'ERAI','ERAI','ERAI']

 plotlgs=['' for x in range(nsite)]


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/Largescale_'+str(lons[ire])+'E_'+str(lats[ire])+'N_'+cseason
     plotlgs[ire] = 'Largescale_'+str(lons[ire])+'E_'+str(lats[ire])+'N_'+cseason

     wks= Ngl.open_wks(ptype,plotname)
     Ngl.define_colormap(wks,'GMT_paired')
     plot = []

     res     = Ngl.Resources()
     res.nglMaximize          =  False
     res.nglDraw              = False
     res.nglFrame             = False
     res.lgPerimOn              = False                 # no box around
     res.vpWidthF         = 0.30                      # set width and height
     res.vpHeightF        = 0.30

     res.tiYAxisString   = "Pressure [hPa]"

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

     res.tmXBLabelFontHeightF = 0.01
     res.tmXBLabelFontThicknessF = 1.0
     res.xyMarkLineMode      = 'Lines'
     res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,3.,3.,3.,3,3,3,3,3,3,3]

     res.xyDashPatterns    = np.arange(0,24,1)

     pres            = Ngl.Resources()
     pres.nglFrame = False
     pres.txFont     = _Font
     pres.nglPanelYWhiteSpacePercent = 5
     pres.nglPanelXWhiteSpacePercent = 5
#     pres.nglPanelTop = 0.88
     pres.wkPaperWidthF  = 17  # in inches
     pres.wkPaperHeightF = 28  # in inches
     pres.nglMaximize = True
     pres.nglPanelTop                      = 0.935
     pres.nglPanelFigureStrings            = alphas
     pres.nglPanelFigureStringsJust        = 'Topleft'
     pres.nglPanelFigureStringsFontHeightF = 0.015


     for iv in range (0, nvaris):   
         if(iv == nvaris-1):
             res.pmLegendDisplayMode    = 'NEVER'
             res.xyExplicitLegendLabels = casenames[:]
             res.pmLegendSide           = 'top'             
             res.pmLegendParallelPosF   = 0.6               
             res.pmLegendOrthogonalPosF = -0.5                  
             res.pmLegendWidthF         = 0.10              
             res.pmLegendHeightF        = 0.10          
             res.lgLabelFontHeightF     = .02               
             res.lgLabelFontThicknessF  = 1.5
             res.lgPerimOn              = True
         else:
             res.pmLegendDisplayMode    = 'NEVER'


         if(obsdataset[iv] =='CCCM'):
             if(cseason == 'ANN'):
                 fileobs = '/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-'+cseason+'.nc'
             else:
                 fileobs = '/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-2010-'+cseason+'.nc'
             inptrobs = Dataset(fileobs,'r')
             latobs=inptrobs.variables['lat'][:]
             latobs_idx = np.abs(latobs - lats[ire]).argmin()
             lonobs=inptrobs.variables['lon'][:]
             lonobs_idx = np.abs(lonobs - lons[ire]).argmin()

             B=inptrobs.variables[varisobs[iv]][:,latobs_idx,lonobs_idx]
         else:
             if (varisobs[iv] =='PRECT'):
                 fileobs = filepathobs+'/GPCP_'+cseason+'_climo.nc'
             else:
                 fileobs = filepathobs + obsdataset[iv]+'_'+cseason+'_climo.nc'
             inptrobs = Dataset(fileobs,'r')
             if (varisobs[iv] =='THETA'):
                 latobs=inptrobs.variables['lat'][:]
                 latobs_idx = np.abs(latobs - lats[ire]).argmin()
                 lonobs=inptrobs.variables['lon'][:]
                 lonobs_idx = np.abs(lonobs - lons[ire]).argmin()
                 B = inptrobs.variables['T'][0,:,latobs_idx,lonobs_idx]
                 pre1 = inptrobs.variables['lev'][:]
                 for il1 in range (0, len(pre1)):
                     B[il1] = B[il1]*(1000/pre1[il1])**0.286
             else: 
                 pre1 = inptrobs.variables['lev'][:]
                 latobs=inptrobs.variables['lat'][:]
                 latobs_idx = np.abs(latobs - lats[ire]).argmin()
                 lonobs=inptrobs.variables['lon'][:]
                 lonobs_idx = np.abs(lonobs - lons[ire]).argmin()

                 B = inptrobs.variables[varisobs[iv]][0,:,latobs_idx,lonobs_idx]

         B[:]=B[:] * cscaleobs[iv]


         for im in range (0,ncases):
             ncdfs[im]  = './data/'+cases[im]+'_site_location.nc'
             infiles[im]= filepath[im]+cases[im]+'/'+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             lev=inptrs.variables['lev'][:]
             nlev=len(lev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             ncdf.close()
             if (im ==0 ):
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
                     theunits=str(cscale[iv])+inptrs.variables['T'].units

                 else:
                     tmp=inptrs.variables[varis[iv]][0,:,npoint] 
                     theunits=str(cscale[iv])+inptrs.variables[varis[iv]].units
                 A_field[im,:] = (A_field[im,:]+tmp[:]/n[ire]).astype(np.float32 )

             A_field[im,:] = A_field[im,:] *cscale[iv]
             inptrs.close()

         textres               = Ngl.Resources()
         textres.txFontHeightF = 0.02   
         textres.txFont        = _Font
         textres.txFontHeightF = 0.015

         res.tiXAxisString   = varis[iv]+ "  Unit=  " + cunits[iv]
         res.trXMinF = min(np.min(A_field[0, :]),np.min(B))
         res.trXMaxF = max(np.max(A_field[0, :]),np.max(B))

         if(varis[iv] == 'CLOUD') :
            if (lats[ire] >= 0 and lons[ire]<230): 
               res.trXMinF = 0.
               res.trXMaxF = 50.
            else:
               res.trXMinF = 0.
               res.trXMaxF = 100.

         if(varis[iv] =='CLDLIQ') :
            if (lats[ire] >= 0):
               res.trXMinF = 0.
               res.trXMaxF = 0.1
            else:
               res.trXMinF = 0.
               res.trXMaxF = 0.1

         if(varis[iv] =='RELHUM') :
             res.trXMinF = 0.
             res.trXMaxF = 100.

         if(varis[iv] == 'THETA') :
            if (lats[ire] >= 0 and lons[ire]<230 ):
               res.trXMinF = 290.
               res.trXMaxF = 340.
            else:
               res.trXMinF = 280
               res.trXMaxF = 320

         if(varis[iv] == 'T') :
             res.trXMinF = 180
             res.trXMaxF = 300
         if(varis[iv] == 'U') :
             res.trXMinF = -40
             res.trXMaxF = 40
         res.trYReverse        = True
         res.xyLineColors      = np.arange(3,20,2)
         res.xyMarkerColors    = np.arange(2,20,2)
         p = Ngl.xy(wks,A_field,lev,res)
         
         res.trYReverse        = False
         res.xyLineColors      = ['black']
         pt = Ngl.xy(wks,B,pre1,res)

         Ngl.overlay(p,pt)
         plot.append(p)

     Ngl.panel(wks,plot[:],[nvaris/2,2],pres)
     txres = Ngl.Resources()
     txres.txFontHeightF = 0.02
     txres.txFont        = _Font
     Ngl.text_ndc(wks,'Large-scale VAR at '+ str(lons[ire])+'E,'+str(lats[ire])+'N',0.5,0.93,txres)
     Common_functions.create_legend(wks,localnames,0.02,np.append('black',np.arange(3,20,2)),0.25,0.85)


     Ngl.frame(wks)
     Ngl.destroy(wks)

 return plotlgs

     

