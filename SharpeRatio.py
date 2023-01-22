# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


plt.style.use("fivethirtyeight")


class PriceInfo:
    
    def __init__(self, Data, IsStockData):
        self.__Data = Data
        self.__IsStockData = IsStockData

        self.__InitialBalance = dict()
        self.__FinalBalance = dict()     
        self.__CAGR = dict()     
        self.__AnnualPerformances = list()
        self.__BestPerformance = dict()
        self.__WorstPerformance = dict()
        
        self._CalculateInitialBalance()
        self._CalculateFinalBalance()
        self._CalculateCompoundAnnualGrowthRate()
        self._CalculateAnnualPerformances()
            
            
            
    def GetData(self):
        return self.__Data
        
    def DataPlot(self):

        if(self.__IsStockData):
            self.__Data.plot(title = 'Stock Data', subplots = True)
            
        else:
            self.__Data.plot(title = 'S&P 500')
            
            
            
    def _CalculateInitialBalance(self):
        for index in self.__Data:
            self.__InitialBalance[index] = round(self.__Data[index][0], 2)        
        
    def PrintInitialBalance(self, index):
        print("Initial Balance:", index)
        print("$", self.__InitialBalance[index])
        
        
        
    def _CalculateFinalBalance(self):
        for index in self.__Data:
            self.__FinalBalance[index] = round(self.__Data[index][-1], 2)
            
    def PrintFinalBalance(self, index):
        print("Final Balance:", index)
        print("$", self.__FinalBalance[index])
        
        
            
    def _CalculateCompoundAnnualGrowthRate(self):
        self.__Data = self.__Data.reset_index()
        NumberOfYears = self.__Data['Date'][len(self.__Data['Date']) - 1].year - self.__Data['Date'][0].year + 1
        
        for index in self.__Data:
            if index != "Date":
                self.__CAGR[index] = round(pow((self.__FinalBalance[index] / self.__InitialBalance[index]), (1 / NumberOfYears)) - 1, 2)
                
        self.__Data = self.__Data.set_index('Date')
                
    def PrintCompoundAnnualGrowthRate(self, index):
        print("CAGR:", index)
        print(self.__CAGR[index], "%")
        
    
    
    def _CalculateAnnualPerformances(self):
        self.__Data = self.__Data.reset_index()
        
        for index in self.__Data:

            if index != "Date":
                CurrentYear = self.__Data['Date'][0].year
                FinalYear = self.__Data['Date'][len(self.__Data) - 1].year
                StartPeriodIndex = 0
                CurrentIndex = 0
                
                while (CurrentYear != FinalYear):
                    
                    if (self.__Data['Date'][CurrentIndex].year == CurrentYear):
                        CurrentIndex = CurrentIndex + 1
                        
                    else:
                        self.__AnnualPerformances.append((self.__Data[index][CurrentIndex - 1] - self.__Data[index][StartPeriodIndex]) / (int((self.__Data['Date'][CurrentIndex] - self.__Data['Date'][StartPeriodIndex]).days)))
                        StartPeriodIndex = CurrentIndex
                
                if (CurrentYear == FinalYear):
                    self.__AnnualPerformances.append((self.__Data[index][len(self.__Data['Date']) - 1] - self.__Data[index][StartPeriodIndex]) / (int((self.__Data['Date'][len(self.__Data['Date']) - 1] - self.__Data['Date'][StartPeriodIndex]).days)))
            
                self.__BestPerformance[index] = max(self.__AnnualPerformances)
                self.__WorstPerformance[index] = min(self.__AnnualPerformances)
                
                self.__AnnualPerformances.clear()
            
        self.__Data = self.__Data.set_index('Date')
        
    def PrintAnnualPerformances(self, index):
        print("Best Annual Performance:", index)
        print(self.__BestPerformance[index] * 100, "%")
        print("Worst Annual Peformance:", index)
        print(self.__WorstPerformance[index] * 100, "%")
        
        
        

    
    
    
    
class StatisticsCalculator:
    
    def __init__(self, StockData, BenchmarkData):
        self.__StockData = StockData
        self.__BenchmarkData = BenchmarkData
        
        self.__MarketCorrelations = dict()
        self.__MaximumDrawdowns = dict()        
        
        self._CalculatePercentChange(IsStockData = True)
        self._CalculatePercentChange(IsStockData = False)
        self._CalculateExcessReturns()
        self._CalculateMean()
        self._CalculateStandardDeviation()
        self._CalculateSharpeRatio()
        self._CalculateSortinoRatio()
        self._CalculateMarketCorrelations()
        self._CalculateMaximumDrawdown()
        
        
        
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
        
    def PlotExcessReturns(self):
        self.__ExcessReturns.plot(title = 'Excess Returns')
        
        
        
    def _CalculateMean(self):
        self.__MeanExcessReturn = self.__ExcessReturns.mean().to_frame()
    
    def PrintMean(self, index):
        print("Mean:", index)
        print(self.__MeanExcessReturn.loc[index][0])
        
    def PlotMean(self):
        self.__MeanExcessReturn.plot.bar(title = 'Mean of the Return Difference', legend = None)
        
        
        
    def _CalculateStandardDeviation(self):
        self.__StandardDeviationExcessReturn = self.__ExcessReturns.std().to_frame()
        self.__StandardDeviationNegativeExcessReturn = self.__ExcessReturns[self.__ExcessReturns < 0].std(skipna = True).to_frame()
        
    def PrintStandardDeviation(self, index):
        print("Standard Deviation:", index)
        print(self.__StandardDeviationExcessReturn.loc[index][0] * 100, "%")
        
    def PlotStandardDeviation(self):
        self.__StandardDeviationExcessReturn.plot.bar(title = 'Standard Deviation of the Return Difference', legend = None)
        
        
        
    def _CalculateSharpeRatio(self):
        self.__DailySharpeRatio = self.__MeanExcessReturn.div(self.__StandardDeviationExcessReturn)
        self.__AnnualFactor = np.sqrt(252)
        self.__AnnualSharpeRatio = self.__DailySharpeRatio.mul(self.__AnnualFactor)
        
    def PrintSharpeRatio(self, index):
        print("Sharpe Ratio:", index)
        print(self.__AnnualSharpeRatio.loc[index][0])
        
    def PlotSharpeRatio(self):
        self.__AnnualSharpeRatio.plot.bar(title = 'Annualized Sharpe Ratio: Stocks vs S&P 500', legend = None)
        
        
        
    def _CalculateSortinoRatio(self):
        self.__DailySortinoRatio = self.__MeanExcessReturn.div(self.__StandardDeviationNegativeExcessReturn)
        self.__AnnualFactor = np.sqrt(252)
        self.__AnnualSortinoRatio = self.__DailySortinoRatio.mul(self.__AnnualFactor)
        
    def PrintSortinoRatio(self, index):
        print("Sortino Ratio:", index)
        print(self.__AnnualSortinoRatio.loc[index][0])
        
    def PlotSortinoRatio(self):
        self.__AnnualSortinoRatio.plot.bar(title = 'Annualized Sortino Ratio: Stocks vs S&P 500', legend = None)
        
        
        
    def _CalculateMarketCorrelations(self):
        temp = pd.DataFrame()
        
        for index in self.__StockData.GetData():
            temp[index] = self.__StockData.GetData()[index]
        temp['S&P 500'] = self.__BenchmarkData.GetData()
        
        for index in temp:
            self.__MarketCorrelations[index] = temp[index].corr(temp['S&P 500'])

    def PrintMarketCorrelations(self, index):
        print("Market Correlation:", index)
        print(self.__MarketCorrelations[index])
        
        
        
    def _CalculateMaximumDrawdown(self):
        temp = pd.DataFrame()
        CumulativeMaxima = []
        Drawdowns = []
        FiveLargestDrawdowns = []
        
        for index in self.__StockData.GetData():
                
            temp[index] = self.__StockData.GetData()[index]

            for i in range(len(temp[index])):
                for j in range(i + 1, len(temp[index])):
                    if temp[index][j] < temp[index][i]:
                        Drawdowns.append(1 - (temp[index][j]/temp[index][i]))
                        
            for k in range(5):
                FiveLargestDrawdowns.append(max(Drawdowns) * -100)
                Drawdowns.remove(max(Drawdowns))
            
            self.__MaximumDrawdowns[index] = FiveLargestDrawdowns
            print("Maximum Drawdowns:", index)
            print(self.__MaximumDrawdowns[index])
            FiveLargestDrawdowns.clear()
            Drawdowns.clear()
        
    def PrintMaximumDrawdown(self, index):
        print("Maximum Drawdown:", index)
        print(self.__MaximumDrawdowns[index], "%")

        
        
        
def Main():
    
    StockData = pd.read_csv('C:\\Users\\mcgor\\Documents\\Machine Learning Project\\Data\\stock_data.csv', parse_dates = ['Date'], index_col = 'Date').dropna()
    BenchmarkData = pd.read_csv('C:\\Users\\mcgor\\Documents\\Machine Learning Project\\Data\\benchmark_data.csv', parse_dates = ['Date'], index_col = 'Date').dropna()
    
    sd = PriceInfo(StockData, True)
    bd = PriceInfo(BenchmarkData, False)
    
    sd.DataPlot()
    bd.DataPlot()
    
    sd.PrintInitialBalance("Amazon")
    sd.PrintInitialBalance("Facebook")
    sd.PrintFinalBalance("Amazon")
    sd.PrintFinalBalance("Facebook")
    
    sd.PrintCompoundAnnualGrowthRate("Amazon")
    sd.PrintCompoundAnnualGrowthRate("Facebook")
    
    sd.PrintAnnualPerformances("Amazon")
    sd.PrintAnnualPerformances("Facebook")
    
    
    
    
    
    
    sr = StatisticsCalculator(sd, bd)
    
    sr.PlotExcessReturns()
    
    sr.PrintMean("Amazon")
    sr.PrintMean("Facebook")
    sr.PlotMean()
    
    sr.PrintStandardDeviation("Amazon")
    sr.PrintStandardDeviation("Facebook")
    sr.PlotStandardDeviation()
    
    sr.PrintSharpeRatio("Amazon")
    sr.PrintSharpeRatio("Facebook")
    sr.PlotSharpeRatio()
    
    
    sr.PrintSortinoRatio("Amazon")
    sr.PrintSortinoRatio("Facebook")
    sr.PlotSortinoRatio()
    sr.PrintMarketCorrelations("Amazon")
    sr.PrintMarketCorrelations("Facebook")
    sr.PrintMaximumDrawdown("Amazon")
    sr.PrintMaximumDrawdown("Facebook")
    
Main()