# -*- coding: utf-8 -*-
"""
============================================
This code is used for demonstrating simulation decomposition (SD)
approach for IFEWs system

# Created: May/27/2021
# Author: Vishal R
============================================
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import collections
import seaborn as sns

# other codes
from codes.prob_distrs import gen_exp
from IFEWs_model_v3_1 import IFEW

if __name__ == '__main__':

    # x = [RCN_c, RCN_s, Hog   , CAtt_B , CAtt_M , CAtt_O] 
    # w = [May_P,Jul_T,Jul_ppt,Jul_ppt_sq,June_ppt ]
    
    ## input variables [RCN_c, RCN_s, Hog   , CAtt_B , CAtt_M , CAtt_O]
    RCN_c = 185  # Sawyer(2018) Avg (155-215)
    RCN_s = 17 # Avg=17.7 kg/ha std=4.8kg/ha based on the fertilizer use and price data between 2008-2018 (USDA, 2019)
    x = np.array([RCN_c  , RCN_s, 20441028, 773914 , 316411 , 1090324])
    
    # %% Generate sampling plan ----------------    
    
    x_sample = {'LHS' : 100000}     # 'MCS': Monte Carlo Sampling
                                  # 'LHS': Latin Hypercube Sampling
                                  # value is used as the NO. of sample points   
    # probability distributions (Uniform, Gaussian, Lognorm )                                  
    x_prob = collections.OrderedDict([('Gaussian_1', (74, 2)),
                                      ('Lognorm_1', (0.4,0, 4))  # shape,location, median
                                     ])                           
    w12 = gen_exp(x_sample, x_prob)
    
    # %% Case generation for SD ----------------    
    
    data = np.empty(shape=(1,3),dtype='object')
    May_P = 80  # May planting progress 80% average (2009-2019)
    June_ppt = 5.5  # in of ppt 
    
    for i in range(len(w12)):         
        if i%1000==0 :  print('\n------ smpl-{} ------\n'.format(i))
        Jul_T = w12[i,0]
        Jul_ppt = w12[i,1]        
        w = np.array([May_P, Jul_T, Jul_ppt, Jul_ppt**2, June_ppt])
        N_surplus,yc,ys,CN,MN,FN,GN = IFEW(x,w, display=False)        
        
        if i ==0 :
            data = np.array([Jul_T, Jul_ppt, N_surplus, yc, ys, CN, MN, FN, GN]).reshape(1,9)
        else:
            data =np.append(data, np.array([Jul_T, Jul_ppt, N_surplus, yc, ys, CN, MN, FN, GN]).reshape(1,9), axis=0 )
        
    n = data.shape[1]
    ## seperate data in different categories -----------
    data1 = np.empty(shape=[0,n])
    data2 = np.empty(shape=[0,n])
    data3 = np.empty(shape=[0,n])
    data4 = np.empty(shape=[0,n])
    
    july_T = 76  
    july_P = 2.5 
    for i in range(len(data)):
        if data[i][0] <=july_T and  data[i][1] < july_P: # <76 , <2.5
            data1 = np.append(data1, data[i].reshape(-1,n), axis=0 ) 
        
        elif data[i][0] <=july_T and  data[i][1] >=july_P: # <76 , >2.5
            data2 = np.append(data2, data[i].reshape(-1,n), axis=0 ) 
        
        elif data[i][0] > july_T and  data[i][1] < july_P: # >76 , <2.5
            data3 = np.append(data3, data[i].reshape(-1,n), axis=0 ) 
             
        elif data[i][0] > july_T and data[i][1] >=july_P: # >76 , >2.5
            data4 = np.append(data4, data[i].reshape(-1,n), axis=0 ) 
     
    # probability computation
    print('---- Probability-------')
    print('case-1 : ', round((data1.shape[0]/data.shape[0]),2))
    print('case-2 : ', round((data2.shape[0]/data.shape[0]),2))
    print('case-3 : ', round((data3.shape[0]/data.shape[0]),2))
    print('case-4 : ', round((data4.shape[0]/data.shape[0]),2))

     
     
    # %% Create dataframe for plotting with seaborn ----------- 
    
    df0 = pd.DataFrame(data, columns = ['Jul_T','Jul_ppt','N_surplus','y_corn','y_soy','CN','MN','FN','GN'])
    df1 = pd.DataFrame(data1, columns = ['Jul_T','Jul_ppt','N_surplus','y_corn','y_soy','CN','MN','FN','GN'])
    df2 = pd.DataFrame(data2, columns = ['Jul_T','Jul_ppt','N_surplus','y_corn','y_soy','CN','MN','FN','GN'])
    df3 = pd.DataFrame(data3, columns = ['Jul_T','Jul_ppt','N_surplus','y_corn','y_soy','CN','MN','FN','GN'])
    df4 = pd.DataFrame(data4, columns = ['Jul_T','Jul_ppt','N_surplus','y_corn','y_soy','CN','MN','FN','GN'])

    case = ['case1']*len(df1) + ['case2']*len(df2) + ['case3']*len(df3) + ['case4']*len(df4)    
    dfo = pd.concat([df1,df2,df3,df4], ignore_index=True)
    dfo['case'] = case
    
    sns.set_palette("pastel")
    fig, ax = plt.subplots(figsize=(14,8),dpi=50)
    a = sns.histplot(df0, x="N_surplus", stat="probability", multiple="stack", ax=ax, legend=False, element="step")
    plt.xlabel("N surplus [kg/ha]")
    plt.tight_layout()  
    fig.savefig('plots/Nsurplus_pdf_full', dpi=400)   
    
    
    sns.set_palette("bright")  #husl bright pastel dark brg
    sns.set_style("white")
    sns.set_context("notebook", font_scale=2, rc={"lines.linewidth": 3.5})
    
    # Create an array with the colors you want to use
    colors = ["#0C39F9", "#F3B712", "#F00000", "#08B61C", "#7E2F8E", "#FF00FF", "#4DBEEE", "#A2142F"]
    # 1st - 1st blue, 2nd orange, 3rd red, 4th green ----reverse in legend 
    # Set your custom color palette
    sns.set_palette(sns.color_palette(colors))
    
    fig = plt.figure(figsize=(8,7),dpi=50)
    a1 = sns.histplot(dfo, x="Jul_T", hue="case", stat="probability", multiple="stack", legend=True, element="step")  
    sns.move_legend(a1, "upper right")
    plt.xlabel("July temperature [$F^\circ$]")
#    plt.legend(labels=['Sc4','Sc3','Sc2','Sc1'])
    # plt.legend(labels=['$Sc_4$','$Sc_3$','$Sc_2$','$Sc_1$'])
    plt.axvline(july_T, color='k',linestyle='--',lw=4)
    # plt.text(67, 0.012,"Regular", fontsize = 25)
    # plt.text(78.5, 0.012,"High", fontsize = 25)
    plt.tight_layout()
    fig.savefig('plots/Jul_T_pdf.png', dpi=400)

    fig = plt.figure(figsize=(8,7),dpi=50)
    a1 = sns.histplot(dfo, x="Jul_ppt", hue="case", stat="probability", multiple="stack", legend=True, element="step" )
    sns.move_legend(a1, "upper right")
    plt.xlabel("July precipitation [in.]")
    plt.axvline(july_P, color='k',linestyle='--',lw=4)
#    plt.legend(labels=['Sc4','Sc3','Sc2','Sc1'])
    # plt.text(10, 0.012,"Regular", fontsize = 25)
    # plt.text(-0.5, 0.012,"Low", fontsize = 25)
    plt.tight_layout()
    fig.savefig('plots/Jul_ppt_pdf.png', dpi=400)
    
    # fig = plt.figure(figsize=(8,7),dpi=100)
    # a = sns.histplot(dfo, x="y_corn", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("Corn yield [bu/acre]")
    # plt.legend(labels=['$Sc_4$','$Sc_3$','$Sc_2$','$Sc_1$'])
    # plt.tight_layout()
    # # fig.savefig('plots/corn_yield_pdf.png', dpi=400)
    
    # fig = plt.figure(figsize=(8,7),dpi=100)
    # a = sns.histplot(dfo, x="y_soy", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("Soybean yield [bu/acre]")
    # plt.tight_layout()
    # # fig.savefig('plots/soy_yield_pdf.png', dpi=400)    
       
    # fig = plt.figure(figsize=(8,7),dpi=100)
    # a = sns.histplot(dfo, x="FN", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("FN [kg/ha]")
    # plt.tight_layout()
    # # fig.savefig('plots/FN_pdf.png', dpi=400)

    # fig = plt.figure(figsize=(8,7),dpi=100)
    # a = sns.histplot(dfo, x="GN", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("GN [kg/ha]")
    # plt.tight_layout()
    # # fig.savefig('plots/GN_pdf.png', dpi=400)

    # fig = plt.figure(figsize=(8,7),dpi=100)
    # a = sns.histplot(dfo, x="CN", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("CN [kg/ha]")
    # plt.tight_layout()

    # fig = plt.figure(figsize=(8,7),dpi=100)
    # sns.histplot(dfo, x="MN", hue="case", stat="probability", multiple="stack", legend=False, element="step")
    # plt.xlabel("MN [kg/ha]")
    # plt.tight_layout()

    fig = plt.figure(figsize=(14,8),dpi=50)
    a = sns.histplot(dfo, x="N_surplus", hue="case", stat="probability", multiple="stack", legend=True, element="step")
    # plt.xlabel("N surplus [kg/ha]")
    plt.xlabel("N surplus ($N_s$) [kg/ha]")   
    # plt.legend(labels=['$Sc_4$: High-T Regular-PPT','$Sc_3$: High-T Low-PPT (Dry)','$Sc_2$: Regular-T Regular-PPT (Regular)','$Sc_1$: Low-PPT Regular-T'])
    # plt.xlim(-10,50)
    plt.tight_layout()    
    fig.savefig('plots/Nsurplus_pdf.png', dpi=400)    

    
    # # Subplot figures ------------------    
    # fig = plt.figure(figsize=(20,20),dpi=100)
    # gs = gridspec.GridSpec(nrows=4, ncols=2)

    # fig.add_subplot(gs[0,0], frameon=False)
    # sns.histplot(dfo, x="Jul_T", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.axvline(july_T, color='k',linestyle='-',lw=1.5)
    # plt.xlabel("July T [$F^\circ$]",fontweight='bold')
        
    # fig.add_subplot(gs[0,1], frameon=False)
    # sns.histplot(dfo, x="Jul_ppt", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.axvline(july_P, color='k',linestyle='-',lw=1.5)
    # plt.xlabel("July ppt [in.]",fontweight='bold')
    
    # fig.add_subplot( gs[1,0], frameon=False)
    # sns.histplot(dfo, x="y_corn", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.xlabel("Corn yield [bu/acre]",fontweight='bold')

    # fig.add_subplot( gs[1,1], frameon=False)
    # sns.histplot(dfo, x="y_soy", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.xlabel("Soybean yield [bu/acre]",fontweight='bold')

    # fig.add_subplot( gs[2,0], frameon=False)
    # a = sns.histplot(dfo, x="FN", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.xlabel("FN [kg/ha]",fontweight='bold')

    # fig.add_subplot( gs[2,1], frameon=False)
    # sns.histplot(dfo, x="GN", hue="case", stat="probability", multiple="stack", legend=False )
    # plt.xlabel("GN [kg/ha]",fontweight='bold')

    # fig.add_subplot( gs[3,:], frameon=False)
    # a = sns.histplot(dfo, x="N_surplus", hue="case", stat="probability", multiple="stack")
    # plt.xlabel("N surplus [kg/ha]",fontweight='bold')   
    # # plt.legend(labels=['Low PPT Regular T', 'Regular', 'Dry', 'Regular PPT High T'])
    # plt.legend(labels=['High-T Regular-PPT','High-T Low-PPT (Dry)','Regular-T Regular-PPT (Regular)','Low-PPT Regular-T'])
    
    # plt.tight_layout()
    # # fig.savefig('plots/combined_plot.png', dpi=400)

