import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def trend_analysis(x,data,order=8):
    coeffs = np.polyfit(list(x),list(data), order)
    return coeffs

def trend_indicator(data):
    df1 = pd.pivot_table(data, values='VOL_SQCM', index=pd.to_datetime(data['PERIOD']).dt.to_period("M") ,columns=['PUBLICATION'],aggfunc='sum')
    dd_p1 = df1.get('PLAYER 1').tolist()
    dd_p2 = df1.get('PLAYER 2').tolist()

    dt=pd.PeriodIndex(df1.index, freq='M').to_timestamp()
    x=mdates.date2num(dt)

    xx = np.linspace(x.min(), x.max(), 100)
    fitted_curve_p1 = np.poly1d(trend_analysis(x,dd_p1))(xx)

    xx = np.linspace(x.min(), x.max(), 100)
    fitted_curve_p2 = np.poly1d(trend_analysis(x,dd_p2))(xx)

    slope_pl1 = trend_analysis(x,dd_p1)[-2]
    slope_pl2 = trend_analysis(x,dd_p2)[-2]

    if slope_pl1<0:
        slope_p1 = "downward"
    elif slope_pl1>0:
        slope_p1 = "upward"
    else:
        slope_p1 = "0"

    if slope_pl2<0:
        slope_p2 = "downward"
    elif slope_pl2>0:
        slope_p2 = "upward"
    else:
        slope_p2 = "0"

    fig, axes = plt.subplots(nrows=2, ncols=1)
    
    axes[0].scatter(x, dd_p1, label="observed")
    axes[0].plot(xx, fitted_curve_p1, c="red", label="fitted")
    axes[0].legend()
    axes[0].set_xticklabels([])
    axes[0].set_xlabel('Period 2018-2020')
    axes[0].set_ylabel('sum(VOL_SQCM)')
    axes[0].set_title("PLAYER 1")
    
    axes[1].scatter(x, dd_p2, label="observed")
    axes[1].plot(xx, fitted_curve_p2, c="red", label="fitted")
    axes[1].legend()
    axes[1].set_xticklabels([])
    axes[1].set_xlabel('Period 2018-2020')
    axes[1].set_ylabel('sum(VOL_SQCM)')
    axes[1].set_title("PLAYER 2")
    plt.tight_layout()
    plt.show(block=False)
    
    slope = [slope_p1,slope_p2]
    return slope

def best_supercategory_advertiser(data,n=5):
    fig, axes = plt.subplots(nrows=2, ncols=1)
    super_cat = data.groupby([data['PUBLICATION'],data['SUPER CATEGORY']]).agg({'VOL_SQCM':sum})
    g = super_cat['VOL_SQCM'].groupby('PUBLICATION', group_keys=False)
    res = g.apply(lambda x: x.sort_values(ascending=False).head(n))
    res.plot(ax=axes[0],kind='barh',title="5 best super category for each player")
    
    ##5 best advertisers for each player
    advertiser = data.groupby([data['PUBLICATION'],data['ADVERTISER']]).agg({'VOL_SQCM':sum})
    g = advertiser['VOL_SQCM'].groupby('PUBLICATION', group_keys=False)
    res = g.apply(lambda x: x.sort_values(ascending=False).head(n))
    res.plot(ax=axes[1],kind='barh',title="5 best advertisers for each player")
    plt.xticks(fontsize=6,rotation='vertical')
    plt.yticks(fontsize=6)
    
    plt.tight_layout()
    plt.show(block=False)

def supporting_advertisers_player1(data,n=10):
    player1 = data.loc[data.PUBLICATION == 'PLAYER 1']
    adv1 = player1.groupby([pd.to_datetime(player1['PERIOD']).dt.year,player1['ADVERTISER']]).agg({'VOL_SQCM':sum})
    g_adv1 = adv1['VOL_SQCM'].groupby('PERIOD', group_keys=False)
    res_adv1 = g_adv1.apply(lambda x: x.sort_values(ascending=False).head(20))
    player1_10_adv = res_adv1.groupby('ADVERTISER').agg(['sum','count']).sort_values(by = ['count','sum'],ascending=False).head(10)
##    print("10 best ,great support advertisers of Player 1 are as follows:\n")
##    for i in range(len(player1_10_adv)):print(player1_10_adv.index[i])
    player1_10_adv.plot(kind='barh',legend=False,title="10 best ,great support advertisers of player 1")
    plt.xticks(fontsize=6,rotation='vertical')
    plt.yticks(fontsize=6)
    plt.tight_layout()
    plt.show(block=False)


if __name__ == "__main__":
    data = pd.read_csv("CaseStudy1.csv",engine='python')
    slope = trend_indicator(data)
    print("Performance of PLAYER 1 has %s trend"%slope[0])
    print("Performance of PLAYER 2 has %s trend"%slope[1])
    best_supercategory_advertiser(data)
    supporting_advertisers_player1(data)

