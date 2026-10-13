### Author: JD Elberse
### Date: 09/07/24
### This code uses Dipy to estimate the Free Water level in the White Matter (FW-WM) of DTI scans

# Packages
import os, sys
import numpy as np
import pandas as pd
import dipy.reconst.fwdti as fwdti
import nibabel as nib
from dipy.core.gradients import gradient_table

# Parameters
sub = sys.argv[1]
ses = sys.argv[2]
root = sys.argv[3]

# Scan suffixes
dwi = f"{root}/derivatives/qsiprep/{sub}/{ses}/dwi/{sub}_{ses}_dir-AP_space-ACPC"
anat = f"{root}/derivatives/qsiprep/{sub}/anat/{sub}_space-ACPC"

if not os.path.exists(f"{dwi}_desc-preproc_dwi.nii.gz"): # If the extension is not correct
    dwi = f"{root}/derivatives/qsiprep/{sub}/{ses}/dwi/{sub}_{ses}_space-ACPC" # It is probably this

# Load DWI image and image data
img = nib.load(f"{dwi}_desc-preproc_dwi.nii.gz")
data = np.asarray(img.dataobj)
        
# Load gradient table
gtab = gradient_table(bvals = f"{dwi}_desc-preproc_dwi.bval", bvecs = f"{dwi}_desc-preproc_dwi.bvec")

# Load mask and mask data
mask_path = f"{dwi}_desc-brain_mask.nii.gz"
if not os.path.exists(mask_path):
    mask_path = f"{anat}_desc-brain_mask.nii.gz"
mask = nib.load(mask_path)
mask = mask.get_fdata()

# Train FWDTI model
fwdtimodel = fwdti.FreeWaterTensorModel(gtab)
fwdtifit = fwdtimodel.fit(data, mask=mask)

# Obtain indices
FA = fwdtifit.fa # Fractional anisotropy
MD = fwdtifit.md # Mean diffusivity
FW = fwdtifit.f # Free water level
TS = fwdtifit.model_params # Free water-corrected tensor

# Load WM segmentation
#WM = nib.load(f"{anat}_WM.nii.gz")
#WM_data = WM.get_fdata()

# Crop WM_data
#TODO: Is there an automated way to do this?
#dist = [c / 2 for c in FW.shape]
#coords = [c / 2 for c in WM.shape]

#x_start, x_end = int(coords[0]-dist[0]), int(coords[0]+dist[0]) # Center Crop
#y_start, y_end = int(coords[1]-dist[1]), int(coords[1]+dist[1]) # Center crop
#z_start, z_end = int(0), int(FW.shape[2]) # Top Crop (Crop Top?)

#WMC_data = WM_data[x_start:x_end, y_start:y_end, z_start:z_end] # Crop array
#WMC_data = shift(WMC_data, shift=(0, 0, 2), mode='nearest') # Z-shift by 2 voxels to obtain right alignment
#WMC = nib.Nifti1Image(WMC_data, FW.affine) # Restore image

#nib.save(WMC, f"{anat}_space-T1w_desc-preproc_WM.nii.gz") # Save cropped WM segmentation

# Mask FW image
#FW_WM = FW * WMC_data

# Store as images
FA_img = nib.Nifti1Image(FA, img.affine)
MD_img = nib.Nifti1Image(MD, img.affine)
FW_img = nib.Nifti1Image(FW, img.affine)
TS_img = nib.Nifti1Image(TS, img.affine)

# Save in subject folder
nib.save(FA_img, f"{dwi}_FA.nii.gz")
nib.save(MD_img, f"{dwi}_MD.nii.gz")
nib.save(FW_img, f"{dwi}_FW.nii.gz")
nib.save(TS_img, f"{dwi}_FWTensor.nii.gz")

print(f"FA, MD, and FW scalars saved to {dwi}")




