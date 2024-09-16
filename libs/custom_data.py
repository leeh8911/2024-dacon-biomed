import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, path:str, whole_encoding=True):
        df = pd.read_csv(path)
        
        self.total_mutate_dict = None
        if whole_encoding:
            self.total_mutate_dict = self.whole_encoding(df)
        else:
            self.total_mutate_dict = self.partial_encoding(df)
        
        new_df = df.copy()
        for k, s in df.items():
            if k == "ID" or k == "SUBCLASS":
                continue
            for i, e in enumerate(s):
                new_df[k][i] = self.total_mutate_dict[k][e]
            
    def partial_encoding(self, df):
        total_mutate_dict = dict()
        for k, v in df.items():
            mutate_set = v.unique()
            mutate_set.remove('WT')
            mutate_dict = dict({'WT':0})
            for i, m in enumerate(mutate_set):
                mutate_dict.update({m:i+1})
            total_mutate_dict[k] = mutate_dict
            
        return total_mutate_dict
        
        
    def whole_encoding(self, df):
        mutate_set = set()
        for k, v in df.items():
            mutate_set.update(v.unique())
            
        mutate_dict = dict({'WT':0})
        mutate_set.remove('WT')
        for i, m in enumerate(mutate_set):
            mutate_dict.update({m:i+1})
            
        total_mutate_dict = dict()
        for k in df.keys():
            total_mutate_dict[k] = mutate_dict
            
        return mutate_dict
            
        
    
    def __len__(self):
        pass
    
    def __getitem__(self, idx):
        pass
    
    
if __name__ == "__main__":
    ds = CustomDataset("data/train.csv", whole_encoding=True)