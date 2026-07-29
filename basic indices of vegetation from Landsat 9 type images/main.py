import matplotlib.pyplot as plt
import numpy as np
import h5py
import cv2
import glob
import rasterio
import matplotlib.pylab as pylab
import scipy
import os
from scipy import stats
from ndvi import *
from evi2 import *
from savi import *
from ndmi import *
from ndwi import *
from colorimg import *
from Kiwifruit import *


params = {'legend.fontsize':5,
          'figure.figsize': (15, 5),
         'axes.labelsize': 10,
         'axes.titlesize':10,
         'xtick.labelsize':10,
         'ytick.labelsize':10}
pylab.rcParams.update(params)

def read_hdf5(path):
    hf = h5py.File(path, 'r')
    adict = {}
    # Read attrs
    for attr in hf.attrs:
        adict[attr] = hf.attrs[attr]
    # Read datasets
    for key in hf.keys():
        adict[key] = hf[key][:]
    # Finish up
    hf.close()
    return adict

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def signaltonoise(a, axis, ddof):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis = axis, ddof = ddof)
    return np.where(sd == 0, 0, m / sd)

### band information ###
'''
10m bands
Band 3 Blue (490 μm)
Band 4 Green (560 μm)
Band 7 Red (665 μm)
Band 10 NIR_Broad (842 μm)
Band 17 SWIR 1 (1610 μm)

20m bands
Band 2 Coastal Aerosol (433 μm)
Band 5 Orange (620 μm)
Band 6 Red 1 (650 μm)
Band 8 Red Edge 1 (705 μm)B
and 9 Red Edge 2 (740 μm)
Band 11 NIR 1 (865 μm)
Band 13 Liquid Water (985 μm)
Band 14 Snow/Ice 1 (1035 μm)
Band 15 Snow/Ice 2 (1090 μm)
Band 18 SWIR 2a (2100 μm)
Band 19 SWIR 2b (2210 μm)
Band 20 SWIR 2c (2260 μm)

60M bands
Band 1 Violet (410 μm)
Band 12 Water Vapor (945 μm)
Band 16 Cirrus (1375 μm)
'''



# find directory for target images
target_dir = 'flex_images/'
target_img = 'DN_10mBands_f110816t01p00r06rdn_c_sc01_ort_img_MSI_Lnext_psf'

flex_list = ['flex000_14bit-','flex005_14bit-','flex010_14bit-','flex020_14bit-','flex040_14bit-','flex080_14bit-',]


# compression paths
compression_paths = []

for i in range(len(flex_list)):
    compression_paths.append(target_dir+flex_list[i]+target_img)
    
test_paths = sorted(glob.glob(target_dir + '*.img'))
headers = sorted(glob.glob(target_dir + '/*.hdr'))

# images
img_list = 'f110816t01p00r06rdn_c','f120510t01p00r11rdn_a','f080630t01p00r13rdn_c','f111109t01p00r23rdn_c','f111102t01p00r11rdn_c',\
'f110803t01p00r11rdn_c','f110712t01p00r17rdn_c','f110712t01p00r14rdn_c','f100914t01p00r04rdn_b','f100908t01p00r02rdn_b','f070804t01p00r04rdn_c'


#output
output = 'flex_outputs/'

n = 0

name_list = ['rgb','ndvi','evi2','savi','ndmi','ndwi']

rgb0 = []
ndvi0 = []
evi20 = []
savi0 = []
ndmi0 = []
ndwi0 = []

rgb_mse = []
ndvi_mse = []
evi_mse = []
savi_mse = []
ndmi_mse = []
ndwe_mse = []

rgb_snr = []
ndvi_snr = []
evi_snr = []
savi_snr = []
ndmi_snr = []
ndwe_snr = []

rgb_diff = []
ndvi_diff = []
evi_diff = []
savi_diff = []
ndmi_diff = []
ndwe_diff = []

fin_list = [rgb0,ndvi0,evi20,savi0,ndmi0,ndwi0]

diff_list = [rgb_diff,ndvi_diff,evi_diff,savi_diff,ndmi_diff,ndwe_diff]


print(test_paths)

for path in test_paths:

        
    blue = path[0,:,:]
    green = path[1,:,:]
    red = path[2,:,:]
    NIR = path[3,:,:]
    SWIR = path[4,:,:]
    
    Coastal_Aerosol = path[:,:,0]
    Orange = path[:,:,1]
    Red_1 = path[:,:,2]
    Red_Edge_1 = path[:,:,3]
    Red_Edge_2 = path[:,:,4]
    NIR_1= path[:,:,5]
    Liquid_Water = path[:,:,6]
    SnowIce_1 = path[:,:,7]
    SnowIce_1 = path[:,:,8]
    SWIR_2a = path[:,:,9]
    SWIR_2b = path[:,:,10]
    SWIR_2c = path[:,:,11]

    Violet = path[:,:,0]
    Water_Vapor = path[:,:,1]
    Cirrus = path[:,:,2]



    L = .5

   
    rgb_out = makecolorimage(red,green,blue) # color image 
    rgb_out = np.ma.masked_where(rgb_out == np.nan, rgb_out)
    rgb_out = np.ma.masked_where(rgb_out == 0, rgb_out)

    ndvi_out = ndvi(NIR,red)  # Normalized difference vegetation index
    ndvi_out = np.ma.masked_where(ndvi_out == np.nan, ndvi_out)
    ndvi_out = np.ma.masked_where(ndvi_out == 0, ndvi_out)

    evi2_out = evi2(NIR,red)  # Enhanced Vegetation Index 2
    evi2_out = np.ma.masked_where(evi2_out == np.nan, evi2_out)
    evi2_out = np.ma.masked_where(evi2_out == 0, evi2_out)

    savi_out =  savi(NIR,red,L)  # Soil Adjusted Vegetation Index
    savi_out = np.ma.masked_where(savi_out == np.nan, savi_out)
    savi_out = np.ma.masked_where(savi_out == 0, savi_out)

    ndmi_out = ndmi(NIR,SWIR) # Normalized Difference Moisture Index
    ndmi_out = np.ma.masked_where(ndmi_out == np.nan, ndmi_out)
    ndmi_out = np.ma.masked_where(ndmi_out == 0, ndmi_out)

    ndwi_out = ndwi(green,NIR) # Normalized Difference Water Index
    ndwi_out = np.ma.masked_where(ndwi_out == np.nan, ndwi_out)
    ndwi_out = np.ma.masked_where(ndwi_out == 0, ndwi_out)

    rgb0.append(rgb_out)
    ndvi0.append(ndvi_out)
    evi20.append(evi2_out)
    savi0.append(savi_out)
    ndmi0.append(ndmi_out)
    ndwi0.append(ndwi_out)


    snr0 =  signaltonoise(rgb_out, axis=0, ddof=0)
    snr1 =  signaltonoise(ndvi_out, axis=0, ddof=0)
    snr2 =  signaltonoise(evi2_out, axis=0, ddof=0)
    snr3 =  signaltonoise(savi_out, axis=0, ddof=0)
    snr4 =  signaltonoise(ndmi_out, axis=0, ddof=0)
    snr5 =  signaltonoise(ndwi_out, axis=0, ddof=0)

    rgb_snr.append(snr0)
    ndvi_snr.append(snr1)
    evi_snr.append(snr2)
    savi_snr.append(snr3)
    ndmi_snr.append(snr4)
    ndwe_snr.append(snr5)


    if n > 0:


        mse0 = mse(rgb_out,rgb_old)
        mse1 = mse(ndvi_out,ndvi_old)
        mse2 = mse(evi2_out,evi2_old)
        mse3 = mse(savi_out,savi_old)
        mse4 = mse(ndmi_out,ndmi_old)
        mse5 = mse(ndwi_out,ndwi_old)

        difference_rgb = rgb_old - rgb_out
        difference_ndvi = ndvi_old - ndvi_out
        difference_evi2 = evi2_old - evi2_out
        difference_savi = savi_old - savi_out
        difference_ndmi = ndmi_old - ndmi_out
        difference_ndwi = ndwi_old - ndwi_out
        
        rgb_diff.append(difference_rgb)
        ndvi_diff.append(difference_ndvi)
        evi_diff.append(difference_evi2)
        savi_diff.append(difference_savi)
        ndmi_diff.append(difference_ndmi)
        ndwe_diff.append(difference_ndwi)

        rgb_mse.append(mse0)
        ndvi_mse.append(mse1)
        evi_mse.append(mse2)
        savi_mse.append(mse3)
        ndmi_mse.append(mse4)
        ndwe_mse.append(mse5)

        print('loop')

    else:
        rgb_old = rgb_out
        ndvi_old = ndvi_out
        evi2_old = evi2_out
        savi_old = savi_out
        ndmi_old = ndmi_out
        ndwi_old = ndwi_out

    n += 1

mse_list = [rgb_mse,ndvi_mse,evi_mse,savi_mse,ndmi_mse,ndwe_mse]

#plot indexes
for x in range(len(fin_list)):
    fig1, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(1,6)
    plt.suptitle(name_list[x])
    im1 = ax1.imshow((fin_list[x])[0])
    fig1.colorbar(im1,ax=ax1)
    ax1.set_title(flex_list[0])
    im2 = ax2.imshow((fin_list[x])[1])
    fig1.colorbar(im2,ax=ax2)
    ax2.set_title(flex_list[1])#+'\n'+str((mse_list[x])[0]))
    im3 = ax3.imshow((fin_list[x])[2])
    fig1.colorbar(im3,ax=ax3)
    ax3.set_title(flex_list[2])#+'\n'+str((mse_list[x])[1]))
    im4 = ax4.imshow((fin_list[x])[3])
    fig1.colorbar(im4,ax=ax4)
    ax4.set_title(flex_list[3])#+'\n'+str((mse_list[x])[2]))
    im5 = ax5.imshow((fin_list[x])[4])
    fig1.colorbar(im5,ax=ax5)
    ax5.set_title(flex_list[4])#+'\n'+str((mse_list[x])[3]))
    im6 = ax6.imshow((fin_list[x])[5])
    fig1.colorbar(im5,ax=ax6)
    ax6.set_title(flex_list[5])#+'\n'+str((mse_list[x])[4]))
    plt.tight_layout()
    plt.savefig(output+name_list[x]+'_graph1.png',dpi = 300)

print(rgb_mse,ndvi_mse,evi_mse,savi_mse,ndmi_mse,ndwe_mse)
print('snr')
#print(rgb_snr,ndvi_snr,evi_snr,savi_snr,ndmi_snr,ndwe_snr)


for x in range(len(fin_list)):
    fig1, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(1,6)
    plt.suptitle(name_list[x])
    im1 = ax1.imshow((fin_list[x])[0])#,vmin = np.percentile(((fin_list[x])[0]),5), vmax = np.percentile(((fin_list[x])[0]),95))
    fig1.colorbar(im1,ax=ax1)
    ax1.set_title(flex_list[0])
    im2 = ax2.imshow((diff_list[x])[0],vmin = np.percentile(((diff_list[x])[0]),5), vmax = np.percentile(((diff_list[x])[0]),95))
    fig1.colorbar(im2,ax=ax2)
    ax2.set_title(flex_list[1])
    im3 = ax3.imshow((diff_list[x])[1],vmin = np.percentile(((diff_list[x])[1]),5), vmax = np.percentile(((diff_list[x])[1]),95))
    fig1.colorbar(im3,ax=ax3)
    ax3.set_title(flex_list[2])
    im4 = ax4.imshow((diff_list[x])[2],vmin = np.percentile(((diff_list[x])[2]),5), vmax = np.percentile(((diff_list[x])[2]),95))
    fig1.colorbar(im4,ax=ax4)
    ax4.set_title(flex_list[3])
    im5 = ax5.imshow((diff_list[x])[3],vmin = np.percentile(((diff_list[x])[3]),5), vmax = np.percentile(((diff_list[x])[3]),95))
    fig1.colorbar(im5,ax=ax5)
    ax5.set_title(flex_list[4])
    im6 = ax6.imshow((diff_list[x])[4],vmin = np.percentile(((diff_list[x])[4]),15), vmax = np.percentile(((diff_list[x])[4]),95))
    fig1.colorbar(im5,ax=ax6)
    ax6.set_title(flex_list[5])
    plt.tight_layout()
    plt.savefig(output+'difference'+name_list[x]+'_graph1.png',dpi = 300)

    