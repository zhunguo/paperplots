
'''
    Draw 2D plots for CLM
    Zhun Guo 
'''
import Ngl
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import scipy as sp
import pylab
import math
import os
import Common_functions
from subprocess import call


def draw_clm_plot (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 if not os.path.exists(casedir+"/2D"):
        os.mkdir(casedir+"/2D") 

 _Font   = 25
 interp = 2
 extrap = False
 mkres = Ngl.Resources()
 mkres.gsMarkerIndex = 2
 mkres.gsMarkerColor = "Red"
 mkres.gsMarkerSizeF = 15.   
 infiles  = ["" for x in range(ncases)] 
 ncdfs    = ["" for x in range(ncases)] 
 varis    = ["SOILWATER_10CM",     "QBOT"]
 varisobs = ["PRECT"              ,"PRECT"]
 alpha    = ["A","B","C","D","E","F"]
 nvaris = len(varis)
 cunits = [""]
 cscale = [1,1,1,86400000, 1,  1,1,100,100,1,1,1000,1,1,1,1]
 cscaleobs =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# cntrs = [[0 for col in range(11)] for row in range(nvaris)]
 cntrs = np.zeros((nvaris,11),np.float32)

 obsdataset=  ["GPCP","GPCP", "NCEP", "ERAI", "CALIPSOCOSP","CALIPSOCOSP","NCEP","NCEP","NVAP"]
 
 plotclm=["" for x in range(nvaris)]
 for iv in range(0, nvaris):
# make plot for each field 
   if(varis[iv] == "SOILWATER_10CM" or varis[iv] == "QBOT" ):
       cntrs[iv,:] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]






#  Observational data
   if(obsdataset[iv] =="CCCM"):
       if(cseason == "ANN"):
           fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-"+cseason+".nc"
       else:
           fileobs = "/Users/guoz/databank/CLD/CCCm/cccm_cloudfraction_2007-2010-"+cseason+".nc"
   else:
       if (varisobs[iv] =="PRECT"):
           fileobs = filepathobs+'/GPCP_'+cseason+'_climo.nc'
       else:
           fileobs = filepathobs + obsdataset[iv]+'_'+cseason+'_climo.nc'

#       infiles[im]=filepath[im]+cases[im]+'/run/'+cases[im]+'_'+cseason+'_climo.nc'


   inptrobs = Dataset(fileobs,'r') 
   latobs=inptrobs.variables['lat'][:]
   lonobs=inptrobs.variables['lon'][:]
   if (varisobs[iv] =="U10"):
      B0=inptrobs.variables[varisobs[iv]][0,:,:] 
      B1=inptrobs.variables["V10"][0,:,:]
      B=(B0*B0+B1*B1)
      B=B * cscaleobs[iv]
      B=np.sqrt(B)
   else:
      B=inptrobs.variables[varisobs[iv]][0,:,:]
      B=B * cscaleobs[iv]

   #************************************************
   # create plot
   #************************************************
   plotname = casedir+'/2D/Land_'+varis[iv]+'_'+cseason
   plotclm[iv] = 'Land_'+varis[iv]+'_'+cseason
   wks= Ngl.open_wks(ptype,plotname)
   Ngl.define_colormap(wks,"cmocean_thermal")
 
#   ngl_define_colormap(wks,"prcp_1")
   plot = []

   textres               = Ngl.Resources()
   textres.txFontHeightF = 0.02   # Size of title.
   textres.txFont        = _Font
   Ngl.text_ndc(wks,varis[iv],0.1,.97,textres)

   pres            = Ngl.Resources()
   pres.nglMaximize = True
   pres.nglPanelYWhiteSpacePercent = 5
   pres.nglPanelXWhiteSpacePercent = 5
   pres.nglPanelBottom = 0.20
   pres.nglPanelTop = 0.9
   pres.pmLabelBarWidthF        = 0.8
   pres.nglFrame         = False
   pres.nglPanelLabelBar                 = True     # Turn on panel labelbar
   pres.nglPanelLabelBarLabelFontHeightF = 0.015    # Labelbar font height
   pres.nglPanelLabelBarHeightF          = 0.0750   # Height of labelbar
   pres.nglPanelLabelBarWidthF           = 0.700    # Width of labelbar
   pres.lbLabelFont                      = "helvetica-bold" # Labelbar font
   pres.nglPanelTop                      = 0.935
   pres.nglPanelFigureStrings            = alpha
   pres.nglPanelFigureStringsJust        = "BottomRight"


   res = Ngl.Resources()
   res.nglDraw         =  False            #-- don't draw plots
   res.nglFrame        =  False  
   res.cnFillOn     = True
   res.cnFillMode   = "RasterFill"
   res.cnLinesOn    = False
   res.nglMaximize = True
   res.mpFillOn     = True
   res.mpCenterLonF = 180
   res.tiMainFont                     = _Font
   res.tiMainFontHeightF              = 0.025
   res.tiXAxisString                  = ""
   res.tiXAxisFont                    = _Font
   res.tiXAxisFontHeightF             = 0.025
   res.tiYAxisString                  = ""
   res.tiYAxisFont                    = _Font
   res.tiYAxisOffsetXF                = 0.0
   res.tiYAxisFontHeightF             = 0.025       
   res.tmXBLabelFont = _Font
   res.tmYLLabelFont = _Font
   res.tiYAxisFont   = _Font
   res.vpWidthF         = 0.80                      # set width and height
   res.vpHeightF        = 0.40
   res.vpXF             = 0.04
   res.vpYF             = 0.30

   res.cnInfoLabelOn                  = False  
   res.cnFillOn                       = True
   res.cnLinesOn                      = False
   res.cnLineLabelsOn                 = False
   res.lbLabelBarOn                   = False
 
   res.mpFillOn                   = False
   
   res.cnLevelSelectionMode = "ExplicitLevels"

   res.cnLevels      = cntrs[iv][:]

   for im in range(0, ncases):
       ncdfs[im]  = './data/'+cases[im]+'_site_location.nc' 
       infiles[im]= filepath[im]+cases[im]+'/'+cases[im]+'_'+cseason+'_clm.nc'
       inptrs = Dataset(infiles[im],'r')       # pointer to file1
       lat=inptrs.variables['lat'][:]
       nlat=len(lat)
       lon=inptrs.variables['lon'][:]
       nlon=len(lon)
       area=inptrs.variables['area'][:]

       area_wgt = np.zeros(nlat)

       sits=np.linspace(0,nsite-1,nsite)
       ncdf= Dataset(ncdfs[im],'r')
       n   =ncdf.variables['n'][:]
       idx_cols=ncdf.variables['idx_cols'][:]
       if (varis[iv] == 'PRECT'):
           A = inptrs.variables['PRECC'][0,:]+inptrs.variables['PRECL'][0,:]
       else:
           A = inptrs.variables[varis[iv]][0,:]

       if (varis[iv] == 'FLUT'):
           A = inptrs.variables['FLUT'][0,:]-inptrs.variables['FLNS'][0,:]
       else:
           A = inptrs.variables[varis[iv]][0,:]

       if (varis[iv] == 'U10'):
           A = inptrs.variables['U10'][0,:]*inptrs.variables['U10'][0,:]
           A = np.sqrt(A)
       else:
           A = inptrs.variables[varis[iv]][0,:]


       A_xy=A
       A_xy = A_xy * cscale[iv]
       ncdf.close()
       inptrs.close()

       if im == 0 :
           dsizes = len(A_xy)
           field_xy = [[0 for col in range(dsizes)] for row in range(ncases)] 
       
       field_xy[im][:] = A_xy
  
       res.lbLabelBarOn = False 
       if(np.mod(im,2)==0): 
           res.tiYAxisOn  = True
       else:
           res.tiYAxisOn  = False
  
       res.tiXAxisOn  = False 
       res.sfXArray     = lon
       res.sfYArray     = lat
       res.mpLimitMode  = "LatLon"
       res.mpMaxLonF    = max(lon) 
       res.mpMinLonF    = min(lon) 
       res.mpMinLatF    = min(lat) 
       res.mpMaxLatF    = max(lat) 
       res.tiMainString    =  "GLB="+str(np.sum(A_xy[:]*area[:]/np.sum(area)))
       textres.txFontHeightF = 0.015
       Ngl.text_ndc(wks,alpha[im]+"  "+ casenames[im],0.3,.135-im*0.03,textres)

       
#       varM = A_xy
#       for ix in range(0, nlon-1):
#         if ( np.isnan(A_xy[ix]) or not np.isfinite(A_xy[ix])):
#            varM[ix]=0.0

       p = Ngl.contour_map(wks,A_xy,res)
       plot.append(p)

   res.lbLabelFont          = _Font
   res.tiYAxisOn  = True
   res.tiXAxisOn  = True
   res.tiXAxisFont = _Font
   rad    = 4.0*np.arctan(1.0)/180.0
   re     = 6371220.0
   rr     = re*rad

   dlon   = abs(lonobs[2]-lonobs[1])*rr
   dx     = dlon* np.cos(latobs*rad)
   jlat   = len(latobs )
   dy     = np.zeros(jlat,dtype=float)
                                                            # close enough
   dy[0]  = abs(lat[2]-lat[1])*rr
   dy[1:jlat-2]  = abs(lat[2:jlat-1]-lat[0:jlat-3])*rr*0.5
   dy[jlat-1]    = abs(lat[jlat-1]-lat[jlat-2])*rr
   area_wgt   = dx*dy  # 
   is_SE= False

   sum1 = 0 
   sum2 = 0 

   for j in range(0, jlat-1):
      for i in range(0, len(lonobs)-1):
        if (np.isnan(B[j][i]) != "--"):
           sum1= sum1+area_wgt[j]*B[j][i]
           sum2= sum2+area_wgt[j]
   
   glb=sum1/sum2
   res.sfXArray     = lonobs
   res.sfYArray     = latobs
   res.mpLimitMode  = "LatLon"
   res.mpMaxLonF    = max(lonobs)
   res.mpMinLonF    = min(lonobs)
   res.mpMinLatF    = min(latobs)
   res.mpMaxLatF    = max(latobs)
   res.tiMainString   =  "GLB="+str(glb)


   p =Ngl.contour_map(wks,B,res)
   plot.append(p)

   if(np.mod(ncases+1,2)==1):
      Ngl.panel(wks,plot[:],[(ncases+1)/2+1,2],pres) 
   else:
      Ngl.panel(wks,plot[:],[(ncases+1)/2,2],pres)
   Ngl.frame(wks)
   Ngl.destroy(wks)

#   Ngl.end()
 return plotclm


