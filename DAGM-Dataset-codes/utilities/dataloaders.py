import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms as T
import torchvision
import torch.nn.functional as F
from torch.autograd import Variable

from PIL import Image
import cv2
import albumentations as A

import time
import os
from tqdm.notebook import tqdm


from torchsummary import summary
import segmentation_models_pytorch as smp

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMAGE_PATH = '/.../data/DAGM_data/Train/Images/'
MASK_PATH = '/.../data/DAGM_data/Train/Labels/' 

n_classes = 7

def create_df():
    name = []
    for dirname, _, filenames in os.walk(IMAGE_PATH):
        for filename in filenames:
            name.append(filename.split('.')[0])
    
    return pd.DataFrame({'id': name}, index = np.arange(0, len(name)))

df = create_df()
print('Total Train Images: ', len(df))


#split data
XXT_train, X_test = train_test_split(df['id'].values, test_size=0.20, random_state=69)
XT_train, X_val = train_test_split(XXT_train, test_size=0.15, random_state=45)
X_train, X_untrain = train_test_split(XT_train, test_size=0.9, random_state=45) #proportion of training data

print('Train Size   : ', len(X_train))
print('Unlabeled_Train Size   : ', len(X_untrain))
print('Val Size     : ', len(X_val))
print('Test Size    : ', len(X_test))

class DAGM_Dataset(Dataset):
    
    def __init__(self, img_path, mask_path, X, mean, std, transform=None, patch=False):
        self.img_path = img_path
        self.mask_path = mask_path
        self.X = X
        self.transform = transform
        self.patches = patch
        self.mean = mean
        self.std = std
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        img = cv2.imread(self.img_path + self.X[idx] + '.PNG', cv2.IMREAD_GRAYSCALE)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(self.mask_path + self.X[idx] + '.PNG', cv2.IMREAD_GRAYSCALE)
        
        if self.transform is not None:
            aug = self.transform(image=img, mask=mask)
            img = Image.fromarray(aug['image'])
            mask = aug['mask']
        
        if self.transform is None:
            img = Image.fromarray(img)
        
        t = T.Compose([T.ToTensor(), T.Normalize(self.mean, self.std)])
        img = t(img)
        mask = torch.from_numpy(mask).long()
        
        
        return img, mask
    

# mean=[0.485, 0.456, 0.406]
# std=[0.229, 0.224, 0.225]
mean=[0.5314]
std=[0.1357]

t_train = A.Compose([A.Resize(256, 256, interpolation=cv2.INTER_NEAREST), A.HorizontalFlip(p=0.5), A.VerticalFlip(p=0.5), 
                     A.RandomBrightnessContrast((0,0.5),(0,0.5))])

t_untrain = A.Compose([A.Resize(256, 256, interpolation=cv2.INTER_NEAREST), A.HorizontalFlip(p=0.5), A.VerticalFlip(p=0.5)])
t_val = A.Compose([A.Resize(256, 256, interpolation=cv2.INTER_NEAREST)])
t_test = A.Compose([A.Resize(256, 256, interpolation=cv2.INTER_NEAREST)])

#datasets
train_set = DAGM_Dataset(IMAGE_PATH, MASK_PATH, X_train, mean, std, t_train, patch=False)
unlabeled_train_set = DAGM_Dataset(IMAGE_PATH, MASK_PATH, X_untrain, mean, std, t_train, patch=False)
val_set = DAGM_Dataset(IMAGE_PATH, MASK_PATH, X_val, mean, std, t_val, patch=False)
test_set = DAGM_Dataset(IMAGE_PATH, MASK_PATH, X_test, mean, std, t_test, patch=False)

#dataloader
batch_size= 16

train_loader = DataLoader(train_set, batch_size=batch_size, num_workers = 6, pin_memory=True, shuffle=True, drop_last = True)
unlabeled_loader = DataLoader(unlabeled_train_set, batch_size=batch_size, num_workers = 8, pin_memory=True, shuffle=True, drop_last = True)
val_loader = DataLoader(val_set, batch_size=batch_size, num_workers = 6, pin_memory=True, shuffle=True)  
test_loader = DataLoader(test_set, batch_size=batch_size, num_workers = 6, pin_memory=True, shuffle=False, drop_last = True) 



