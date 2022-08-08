# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 18:10:44 2022

@author: corentin.cou
"""

import numpy as np
import spectral.io.envi as envi
from os import path
import cv2
import csv
import matplotlib.pyplot as plt

# --------------------------------------------------
# Two case : choose if you prefer multiple reference 
# spectra from the same hyperspectral image ('OneImg')
# or one reference spectra per image ('multipleImg')
typ = 'OneImg'

# File folder
filename = "D://Spectral//Aubusson//Gaude sur laine//"

# If one img, give a string. If multiple img, give
# a list of strings 
img_nbr = "001"

# If your image is too big, choose 'yes' to create 
# a simple array for white and dark reference
big = 'yes'

# Label for each of the reference spectra
label = ['17 A']

# Name of the data you want to save
name = 'database' 
# --------------------------------------------------

# Case of a big image (for example taken
# with Specim VNIR)
if big =='yes':
    if path.exists(filename+'array_white.txt') == False :
        # Creation of white and dark reference
        white_nparr = np.array(envi.open(filename+"WHITEREF_"+img_nbr+".hdr", filename+"WHITEREF_"+img_nbr+".raw").load())

        white_val = []
        for i in range(840):
            white_val.append(np.mean(white_nparr[:,:, i]))
        file1 = open(filename+'array_white.txt',"w")
        np.savetxt(file1, [white_val])
        file1.close()
        
        
        #dark_file = open(filename+'array_dark.txt',"r")
        dark_nparr = np.array(envi.open(filename+"DARKREF_"+img_nbr+".hdr", filename+"DARKREF_"+img_nbr+".raw").load())
        print(np.min(dark_nparr))
        dark_val = []
        for i in range(840):
            dark_val.append(np.mean(dark_nparr[:,:, i]))
        dark_val[0] = dark_val[1]
        file1 = open(filename+'array_dark.txt',"w")
        np.savetxt(file1, [dark_val])
        file1.close()
        
        del white_nparr, white_val, dark_nparr, dark_val
    
    bands = np.array(np.genfromtxt('bands_long.csv', delimiter=','))
    
    spectra = []
    # --------------------------------------------------
    # Case of unique image
    if typ == 'OneImg':  
        data_nparr = (envi.open(filename+img_nbr+".hdr", filename+img_nbr+".raw").load())

        # White and dark reference import
        white_file = open(filename+'array_white.txt',"r")
        white_val = np.loadtxt(white_file)
        
        dark_file = open(filename+'array_dark.txt',"r")
        dark_val = np.loadtxt(dark_file)
        dark_val[0] = dark_val[1]
        
        # Select by hand each of the zone for spectra selection
        specImg =  data_nparr[:,:,[23*4, 52*4, 73*4]]/255
        specImg = cv2.resize(specImg, (int(np.shape(specImg)[1]/4), int(np.shape(specImg)[0]/4)))
        
        for i in range(len(label)):
            ROI = cv2.selectROI("Spectra number : "+str(label[i]), specImg)
            cv2.destroyAllWindows()
            
            specEmVal = []
            for k in range(np.shape(data_nparr)[2]):
                specEmVal.append(np.nanmean(data_nparr[ROI[1]*4:(ROI[1]+ROI[3])*4,
                                                       ROI[0]*4:(ROI[0]+ROI[2])*4,k]))
            corrected_nparr = np.divide(
                    np.subtract(np.array(specEmVal), dark_val),
                    np.subtract(white_val, dark_val))
            spectra.append(corrected_nparr)
    
    # --------------------------------------------------    
    elif typ == 'MultipleImg':
        i = 0
        for elt in img_nbr:
            data_nparr = (envi.open(filename+elt+".hdr", filename+elt+".raw").load())
    
            # White and dark reference import
            white_file = open(filename+'array_white.txt',"r")
            white_val = np.loadtxt(white_file)
            
            dark_file = open(filename+'array_dark.txt',"r")
            dark_val = np.loadtxt(dark_file)
            dark_val[0] = dark_val[1]
            
            # Select by hand each of the zone for spectra selection
            specImg =  data_nparr[:,:,[23*4, 52*4, 73*4]]/255
            specImg = cv2.resize(specImg, (int(np.shape(specImg)[1]/4), int(np.shape(specImg)[0]/4)))
            
            ROI = cv2.selectROI("Spectra number : "+str(label[i]), specImg)
            cv2.destroyAllWindows()
            
            specEmVal = []
            for k in range(np.shape(data_nparr)[2]):
                specEmVal.append(np.nanmean(data_nparr[ROI[1]*4:(ROI[1]+ROI[3])*4,
                                                       ROI[0]*4:(ROI[0]+ROI[2])*4,k]))
            corrected_nparr = np.divide(
                    np.subtract(np.array(specEmVal), dark_val),
                    np.subtract(white_val, dark_val))
            spectra.append(corrected_nparr)
        
            del data_nparr, white_val, dark_val
            i += 1
    # --------------------------------------------------    
    else : 
        print("Please choose between 'MultipleImg' or 'OneImg' for 'typ'")
        
# --------------------------------------------------         
# Case of a big image (for example taken
# with Specim IQ)
elif big =='no':
    bands = np.array(np.genfromtxt('bands.csv', delimiter=','))
    
    spectra = []
    # --------------------------------------------------   
    if typ == 'OneImg':  
        dark_ref = envi.open(filename+img_nbr+"//capture//DARKREF_"+img_nbr+".hdr",
                             filename+img_nbr+"//capture//DARKREF_"+img_nbr+".raw")
        white_ref = envi.open(filename+img_nbr+"//capture//WHITEREF_"+img_nbr+".hdr",
                              filename+img_nbr+"//capture//WHITEREF_"+img_nbr+".raw")
        data_ref = envi.open(filename+img_nbr+'//capture//'+img_nbr+".hdr",
                             filename+img_nbr+'//capture//'+img_nbr+".raw")
        
        white_nparr = np.array(white_ref.load())
        dark_nparr = np.array(dark_ref.load())
        data_nparr = np.array(data_ref.load())
            
        corrected_nparr = np.divide(
            np.subtract(data_nparr, dark_nparr),
            np.subtract(white_nparr, dark_nparr))
            
        # Select by hand each of the zone for spectra selection
        specImg =  corrected_nparr[:,:,[23, 52, 73]]
        
        for i in range(len(label)):
            ROI = cv2.selectROI("Spectra number : "+str(label[i]), specImg)
            cv2.destroyAllWindows()
            
            specEmVal = []
            for k in range(np.shape(data_nparr)[2]):
                specEmVal.append(np.nanmean(corrected_nparr[ROI[1]:ROI[1]+ROI[3]+1,
                                                       ROI[0]:ROI[0]+ROI[2]+1,k]))
            spectra.append(specEmVal)
    # --------------------------------------------------    
    elif typ == 'MultipleImg':
        i = 0
        for elt in img_nbr:
            dark_ref = envi.open(filename+elt+"//capture//DARKREF_"+elt+".hdr",
                                 filename+elt+"//capture//DARKREF_"+elt+".raw")
            white_ref = envi.open(filename+elt+"//capture//WHITEREF_"+elt+".hdr",
                                  filename+elt+"//capture//WHITEREF_"+elt+".raw")
            data_ref = envi.open(filename+elt+'//capture//'+elt+".hdr",
                                 filename+elt+'//capture//'+elt+".raw")
            
            white_nparr = np.array(white_ref.load())
            dark_nparr = np.array(dark_ref.load())
            data_nparr = np.array(data_ref.load())
                
            corrected_nparr = np.divide(
                np.subtract(data_nparr, dark_nparr),
                np.subtract(white_nparr, dark_nparr))
                
            # Select by hand each of the zone for spectra selection
            specImg =  corrected_nparr[:,:,[23, 52, 73]]
        
            ROI = cv2.selectROI("Spectra number : "+str(label[i]), specImg)
            cv2.destroyAllWindows()
            
            specEmVal = []
            for k in range(np.shape(data_nparr)[2]):
                specEmVal.append(np.nanmean(corrected_nparr[ROI[1]:ROI[1]+ROI[3]+1,
                                                       ROI[0]:ROI[0]+ROI[2]+1,k]))
            spectra.append(specEmVal)
            del data_nparr, white_val, dark_val
            i += 1
    # --------------------------------------------------    
    else : 
        print("Please choose between 'MultipleImg' or 'OneImg' for 'typ'")
        
# --------------------------------------------------            
else : 
    print("Please choose between 'yes' or 'no' for 'big'")
    
    
# --------------------------------------------------        
# Plot the spectra
plt.figure()
for i in range(len(spectra)):
    plt.plot(bands, spectra[i], label=label[i])
plt.legend()

# --------------------------------------------------        
# Save the reference spectra as a dictionnary
dictionnary = {label[i]: spectra[i] for i in range(len(spectra))}
with open(name+'.csv', 'w') as f:
    for key in dictionnary.keys():
        f.write("%s, %s\n" % (key, dictionnary[key]))

