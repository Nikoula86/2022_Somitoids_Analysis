import glob, os, tqdm
import numpy as np
from skimage.io import imread
import pandas as pd

pxl_size = [0.3461,0.3461,2]

folders = [
    os.path.join('190835-10uM'),     
    os.path.join('195336-10uM'),    
    os.path.join('200421-10uM'),
    os.path.join('201742-10uM'),
    os.path.join('204011-10uM'),
    os.path.join('205431-10uM'),
    os.path.join('211940-7uM'),
    os.path.join('212715-7uM'),
    os.path.join('214629-7uM'),
    os.path.join('215233-7uM'),
    os.path.join('220010-5uM'),
    os.path.join('220509-5uM'),
    os.path.join('221019-5uM'),
    ]

conditions = [
    '10uM',
    '10uM',
    '10uM',
    '10uM',    
    '10uM',
    '10uM',
    '7uM',
    '7uM',
    '7uM',
    '7uM',
    '5uM',
    '5uM',
    '5uM',
                    
    ]

channel_orders = [
    ['TBX18','UNCX4.1','BRACHYURY','SOX2'] for i in folders
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
