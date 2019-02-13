import pandas as pd
import glob

# this script collates all resultant beer styles into one file for potentially easier uploading to a sqlite database

path =r'/Users/evangrandfield/Desktop/BeerMe/Beer Files' # use your path
allFiles = glob.glob(path + "/*.csv")

list_ = []

for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)

frame = pd.concat(list_, axis = 0, ignore_index = True)


frame.to_csv('/Users/evangrandfield/Desktop/BeerMe/all_beers.csv')
