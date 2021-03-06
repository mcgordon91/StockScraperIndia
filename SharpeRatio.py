# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


plt.style.use("fivethirtyeight")


class PriceInfo:
    
    def __init__(self, Data):
        self.__Data = Data
    
    def SetData(self, Data):
        self.__Data = Data

    def GetData(self):
        return self.__Data
    
    def DataSummary(self):
        print(self.__Data.head())
        print(self.__Data.info())
        
    def DataPlot(self, IsStockData):

        if(IsStockData):
            self.__Data.plot(title = 'Stock Data', subplots = True)
            
        else:
            self.__Data.plot(title = 'S&P 500')
        
    def DataDescription(self):
        self.__Data.describe()
    
    
    
class SharpeRatioCalculator:
    
    def __init__(self, StockData, BenchmarkData):
        self.__StockData = StockData
        self.__BenchmarkData = BenchmarkData
        
    def _CalculatePercentChange(self, IsStockData):
        
        if(IsStockData):
            self.__StockReturns = self.__StockData.GetData().pct_change()
            self.__StockReturns.plot(title = 'Daily Percent Change')
        
        else:
            self.__BenchmarkReturns = self.__BenchmarkData.GetData().pct_change()
            self.__BenchmarkReturns.plot(title = 'Daily Percent Change')

    def _CalculateExcessReturns(self):
        self.__BenchmarkReturns = self.__BenchmarkReturns['S&P 500'].squeeze()
        self.__ExcessReturns = self.__StockReturns.sub(self.__BenchmarkReturns, axis = 0)
        self.__ExcessReturns.plot(title = 'Excess Returns')
        
    def _CalculateMean(self):
        self.__MeanExcessReturn = self.__ExcessReturns.mean().to_frame()
        self.__MeanExcessReturn.plot.bar(title = 'Mean of the Return Difference', legend = None)
        
    def _CalculateStandardDeviation(self):
        self.__StandardDeviationExcessReturn = self.__ExcessReturns.std().to_frame()
        self.__StandardDeviationExcessReturn.plot.bar(title = 'Standard Deviation of the Return Difference', legend = None)
        
    def CalculateSharpeRatio(self):
        self._CalculatePercentChange(IsStockData = True)
        self._CalculatePercentChange(IsStockData = False)
        self._CalculateExcessReturns()
        self._CalculateMean()
        self._CalculateStandardDeviation()
        
        
        self.__DailySharpeRatio = self.__MeanExcessReturn.div(self.__StandardDeviationExcessReturn)
        self.__AnnualFactor = np.sqrt(252)
        self.__AnnualSharpeRatio = self.__DailySharpeRatio.mul(self.__AnnualFactor)
        self.__AnnualSharpeRatio.plot.bar(title = 'Annualized Sharpe Ratio: Stocks vs S&P 500', legend = None)
        



def Main():
    StockData = pd.read_csv('C:\\Users\\mcgor\\Documents\\Machine Learning Project\\Data\\stock_data.csv', parse_dates = ['Date'], index_col = 'Date').dropna()
    BenchmarkData = pd.read_csv('C:\\Users\\mcgor\\Documents\\Machine Learning Project\\Data\\benchmark_data.csv', parse_dates = ['Date'], index_col = 'Date').dropna()
    
    sd = PriceInfo(StockData)
    bd = PriceInfo(BenchmarkData)
    
    #sd.DataSummary()
    #bd.DataSummary()
    
    sd.DataPlot(True)
    bd.DataPlot(False)
    
    #sd.DataDescription()
    #bd.DataDescription()
    
    sr = SharpeRatioCalculator(sd, bd)
    
    sr.CalculateSharpeRatio()
    
Main()