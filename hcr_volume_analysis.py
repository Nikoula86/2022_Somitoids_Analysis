import glob, os, tqdm
import numpy as np
from skimage.io import imread
import pandas as pd
# sys.path.append(os.path.join("Y:",os.sep,'Nicola_Gritti','analysis_code','scaling_analysis','funcs'))
# from _01_generate_masks import tif2binary
# from _02_compute_volumes import binary2volume

pxl_size = [0.3461,0.3461,2]

folders = [
    os.path.join('2021-06-06_190835-10uM-Mat'),     
    os.path.join('2021-06-06_195336-9uM-Mat'),    
    os.path.join('2021-06-06_200421-9uM-Mat'),
    os.path.join('2021-06-06_201742-9uM-Mat'),
    os.path.join('2021-06-06_204011-8uM-Mat'),
    os.path.join('2021-06-06_205431-8uM-Mat'),
    os.path.join('2021-06-06_211940-7uM-Mat'),
    os.path.join('2021-06-06_212715-7uM-Mat'),
    os.path.join('2021-06-06_214629-6uM-Mat'),
    os.path.join('2021-06-06_215233-6uM-Mat'),
    os.path.join('2021-06-06_220010-5uM-Mat'),
    os.path.join('2021-06-06_220509-5uM-Mat'),
    os.path.join('2021-06-06_221019-5uM-Mat'),
    ]

conditions = [
    '10uM',
    '9uM',
    '9uM',
    '9uM',    
    '8uM',
    '8uM',
    '7uM',
    '7uM',
    '6uM',
    '6uM',
    '5uM',
    '5uM',
    '5uM',
                    
    ]

channel_orders = [
    ['Tbx18','Uncx41','Bra','Sox2'] for i in folders
    ]

#############################################
voxel_size = np.prod(pxl_size)

df_all = pd.DataFrame({})

for sample, cond, ch_order in tqdm.tqdm(zip(folders, conditions, channel_orders)):

    # print(init)

    print(sample)
    
    mask_folder = os.path.join(sample,'tifs','masks')
    flist = glob.glob(os.path.join(mask_folder,'*.tif'))
    flist.sort()
    # print(flist)

    masks = np.stack([imread(i) for i in tqdm.tqdm(flist[:-1])])
    masks = masks>0
    mask_tot = imread(flist[-1])
    mask_tot = mask_tot>0
    
    # mask with the total
    masks = np.stack([i*mask_tot for i in masks])

    # compute volumes
    volumes = np.array([np.sum(m) for m in masks])*voxel_size
    tot_vol = np.sum(mask_tot)*voxel_size

    df = pd.DataFrame({
            'condition':cond,
            'sample':sample,
            'vol_%s'%ch_order[0]:volumes[0],
            'vol_%s'%ch_order[1]:volumes[1],
            'vol_%s'%ch_order[2]:volumes[2],
            'vol_%s'%ch_order[3]:volumes[3],
            'vol_tot':tot_vol,
            }, index=[0])

    # compute overlap
    for i in range(len(masks)):
        for j in range(i,len(masks)):
            overlap = np.sum(masks[i]*masks[j])
            df['overlap_%s_%s'%(ch_order[i],ch_order[j])] = overlap*voxel_size

    df_all = pd.concat([df_all, df], ignore_index=False)
            
df_all.to_csv('Volumes.csv', index=False)
# df_all.to_excel('Volumes.xlsx', index=False)
        
    
