import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def SongSim(lyr, show_table = True, fig_size = (8, 8), ticks = False, title = "SongSim Table"):
    
    """
    SongSim is a method that creates a similarity matrix for n length text.
    I inspired by Collin Morris and when I looked his github page for the source code
    for this but I did not know that it written in css and javascript 
    so I created a python version for SongSim.
    Github link of actual SongSim: https://github.com/colinmorris/SongSim
    """
    
    if type(lyr) is str:
        
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        lyrics = ""
        for char in lyr:
            if char not in punctuations:
                lyrics = lyrics + char
                
        lyrics = lyrics.lower()
        lyrics = lyrics.split()
        
    raw_corrs = []
    for current_word in lyrics:
        for word in lyrics:
            if current_word == word:
                raw_corrs.append(1)

            else:
                raw_corrs.append(0)

    corrs = []
    for length, _ in enumerate(lyrics, start = 1):
        length *= len(lyrics)
        corrs.append(raw_corrs[(length - len(lyrics)):length])

    corrs = np.array(corrs)

    uniq, count = np.unique(lyrics, return_counts = True)
    freq_names = {}
    for name, freq in zip(uniq, count):
        freq_names[name] = freq

    freq_names2 = freq_names.copy()

    corrs_dict = {}
    for indx, c_name in enumerate(lyrics):
        if c_name in corrs_dict:
            freq_names2[c_name] -= 1 
            label = freq_names[c_name] - freq_names2[c_name]
            corrs_dict[c_name + str(label)] = corrs[indx]

        else:
            corrs_dict[c_name] = corrs[indx]

    corrs_df = pd.DataFrame(data = corrs_dict)

    songsim = corrs_df.corr()
    for colmn in songsim.columns:
        for indx, corr_val in enumerate(songsim[colmn]):
            if corr_val != 1:
                songsim[colmn][indx] = 0

            else:
                continue
                
    if show_table == True:
        f,ax = plt.subplots(figsize = fig_size)
        res = sns.heatmap(songsim,linecolor = "none", xticklabels = ticks, yticklabels = ticks, ax=ax,cmap = "Greys", cbar = False)
        plt.title(title)

        for _, spine in res.spines.items(): 
            spine.set_visible(True) 
            spine.set_linewidth(2) 

        plt.show()
    
    return songsim
