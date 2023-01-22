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


# This class stores a dataframe of stock info and marks whether it is stock or benchmark data
class PriceInfo:
    
    # The constructor calculates the initial and final balances, compound annual growth rate and best and worst
    # performances for all stocks right at the outset
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
            
            
    # Getter function         
    def GetData(self):
        return self.__Data
        
    # Plots the stock data for all stocks in the dataframe
    def DataPlot(self):

        if(self.__IsStockData):
            self.__Data.plot(title = 'Stock Data', subplots = True)
            
        else:
            self.__Data.plot(title = 'S&P 500')
            
            
    # Calculates the initial balance of all stocks in the dataframe, rounded to two decimal points           
    def _CalculateInitialBalance(self):
        for index in self.__Data:
            self.__InitialBalance[index] = round(self.__Data[index][0], 2)        
        
    # Prints the initial balance of a selected stock
    def PrintInitialBalance(self, index):
        print("Initial Balance:", index)
        print("$", self.__InitialBalance[index])
        
        
    # Calculates the final balance of all stocks in the dataframe, rounded to two decimal points 
    def _CalculateFinalBalance(self):
        for index in self.__Data:
            self.__FinalBalance[index] = round(self.__Data[index][-1], 2)
     
    # Prints the initial balance of a selected stock
    def PrintFinalBalance(self, index):
        print("Final Balance:", index)
        print("$", self.__FinalBalance[index])
        
        
            
    # Calculates the compound annual growth rate for every stock in the dataframe
    # which is ((final value/initial value)^(1/# of years) - 1) * 100%
    def _CalculateCompoundAnnualGrowthRate(self):
        self.__Data = self.__Data.reset_index()
        NumberOfYears = self.__Data['Date'][len(self.__Data['Date']) - 1].year - self.__Data['Date'][0].year + 1
        
        for index in self.__Data:
            if index != "Date":
                self.__CAGR[index] = round(100 * pow((self.__FinalBalance[index] / self.__InitialBalance[index]), (1 / NumberOfYears)) - 1, 2)
                
        self.__Data = self.__Data.set_index('Date')
                
    # Prints the Compound Annual Growth Rate for a selected stock
    def PrintCompoundAnnualGrowthRate(self, index):
        print("CAGR:", index)
        print(self.__CAGR[index], "%")
        
    
    # Calculates the annual performance for every stock in the dataframe
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
      
    # Prints the annual performance for a selected stock
    def PrintAnnualPerformances(self, index):
        print("Best Annual Performance:", index)
        print(self.__BestPerformance[index] * 100, "%")
        print("Worst Annual Peformance:", index)
        print(self.__WorstPerformance[index] * 100, "%")
        
    
    def RollingAverageAlarm(self):
        print(self.__Data['Amazon'].rolling(3).mean())
        
        
        

    
    
    
# This class calculates various statistics for stocks    
class StatisticsCalculator:
    
    # This constructor calculates the percent change, excess return (relative to the benchmark),
    # mean, standard deviationand Sharpe and Sortino ratios for all stocks right at the outset
    def __init__(self, StockData, BenchmarkData):
        self.__StockData = StockData
        self.__BenchmarkData = BenchmarkData
        
        self.__MarketCorrelations = dict()
        self.__MaximumDrawdowns = dict()        
        
        self._CalculatePercentChange(IsStockData = True)
        self._CalculatePercentChange(IsStockData = False)
        self._CalculateExcessReturns()
        self._CalculateMeanExcessReturns()
        self._CalculateStandardDeviationExcessReturns()
        self._CalculateSharpeRatio()
        self._CalculateSortinoRatio()
        self._CalculateMarketCorrelations()
        # self._CalculateMaximumDrawdown()
        
        
    # Calculates the daily percent change for all stocks in the dataframe  
    def _CalculatePercentChange(self, IsStockData):
        
        if(IsStockData):
            self.__StockReturns = self.__StockData.GetData().pct_change()
            self.__StockReturns.plot(title = 'Daily Percent Change')
        
        else:
            self.__BenchmarkReturns = self.__BenchmarkData.GetData().pct_change()
            self.__BenchmarkReturns.plot(title = 'Daily Percent Change')
            
            
    # Calculates the excess returns for all stocks in the dataframe relative to the benchmark
    def _CalculateExcessReturns(self):
        self.__BenchmarkReturns = self.__BenchmarkReturns['S&P 500'].squeeze()
        self.__ExcessReturns = self.__StockReturns.sub(self.__BenchmarkReturns, axis = 0)
        
    # Plots the excess returns for all stocks
    def PlotExcessReturns(self):
        self.__ExcessReturns.plot(title = 'Excess Returns')
        
        
    # Calculates the mean of the excess returns of all stock in the dataframe 
    def _CalculateMeanExcessReturns(self):
        self.__MeanExcessReturn = self.__ExcessReturns.mean().to_frame()
    
    # Prints the mean of the excess returns of a selected stock
    def PrintMeanExcessReturns(self, index):
        print("Mean:", index)
        print(self.__MeanExcessReturn.loc[index][0])

    # Plots the mean of the excess returns of all stocks        
    def PlotMeanExcessReturns(self):
        self.__MeanExcessReturn.plot.bar(title = 'Mean of the Return Difference', legend = None)
        
        
    # Calculates the standard deviation of the excess returns (and of the excess returns when
    # the excess returns are negative) of all stocks in the dataframe
    def _CalculateStandardDeviationExcessReturns(self):
        self.__StandardDeviationExcessReturn = self.__ExcessReturns.std().to_frame()
        self.__StandardDeviationNegativeExcessReturn = self.__ExcessReturns[self.__ExcessReturns < 0].std(skipna = True).to_frame()

    # Prints the standard deviation of the excess returns of a selected stock        
    def PrintStandardDeviationExcessReturns(self, index):
        print("Standard Deviation:", index)
        print(self.__StandardDeviationExcessReturn.loc[index][0])
        
    # Plots the standard deviation of the excess returns of all stocks
    def PlotStandardDeviationExcessReturns(self):
        self.__StandardDeviationExcessReturn.plot.bar(title = 'Standard Deviation of the Return Difference', legend = None)
        
        
    # Calculates the Sharpe ratio of all stocks in the datframe (mean/standard deviation) * sqrt(252),
    # where 252 is the typical number of trading days in a year    
    def _CalculateSharpeRatio(self):
        self.__DailySharpeRatio = self.__MeanExcessReturn.div(self.__StandardDeviationExcessReturn)
        self.__AnnualFactor = np.sqrt(252)
        self.__AnnualSharpeRatio = self.__DailySharpeRatio.mul(self.__AnnualFactor)
        
    # Prints the Sharpe ratio of a selected stock
    def PrintSharpeRatio(self, index):
        print("Sharpe Ratio:", index)
        print(self.__AnnualSharpeRatio.loc[index][0])
      
    # Plo the Sharpe ratio of all stocks
    def PlotSharpeRatio(self):
        self.__AnnualSharpeRatio.plot.bar(title = 'Annualized Sharpe Ratio: Stocks vs S&P 500', legend = None)
        
        
    # Calculates the Sortino ratio of all stocks in the dataframe (mean/standard deviation of ne) * sqrt(252),
    # where 252 is the typical number of trading days in a year
    def _CalculateSortinoRatio(self):
        self.__DailySortinoRatio = self.__MeanExcessReturn.div(self.__StandardDeviationNegativeExcessReturn)
        self.__AnnualFactor = np.sqrt(252)
        self.__AnnualSortinoRatio = self.__DailySortinoRatio.mul(self.__AnnualFactor)
        
    # Prints the Sortini ratio of a selected stock  
    def PrintSortinoRatio(self, index):
        print("Sortino Ratio:", index)
        print(self.__AnnualSortinoRatio.loc[index][0])
        
    # Plots the Sortini ratio of all stocks  
    def PlotSortinoRatio(self):
        self.__AnnualSortinoRatio.plot.bar(title = 'Annualized Sortino Ratio: Stocks vs S&P 500', legend = None)
        
        
    # Calculates the market correlations of all stocks in the dataframe
    def _CalculateMarketCorrelations(self):
        temp = pd.DataFrame()
        
        for index in self.__StockData.GetData():
            temp[index] = self.__StockData.GetData()[index]
        temp['S&P 500'] = self.__BenchmarkData.GetData()
        
        for index in temp:
            self.__MarketCorrelations[index] = temp[index].corr(temp['S&P 500'])
    
    # Prints the market correlation of a selected stock
    def PrintMarketCorrelations(self, index):
        print("Market Correlation:", index)
        print(self.__MarketCorrelations[index])
        
        
        
    # def _CalculateMaximumDrawdown(self):
    #     temp = pd.DataFrame()
    #     CumulativeMaxima = []
    #     Drawdowns = []
    #     FiveLargestDrawdowns = []
        
    #     for index in self.__StockData.GetData():
                
    #         temp[index] = self.__StockData.GetData()[index]

    #         for i in range(len(temp[index])):
    #             for j in range(i + 1, len(temp[index])):
    #                 if temp[index][j] < temp[index][i]:
    #                     Drawdowns.append(1 - (temp[index][j]/temp[index][i]))
                        
    #         for k in range(5):
    #             FiveLargestDrawdowns.append(max(Drawdowns) * -100)
    #             Drawdowns.remove(max(Drawdowns))
            
    #         self.__MaximumDrawdowns[index] = FiveLargestDrawdowns
    #         print("Maximum Drawdowns:", index)
    #         print(self.__MaximumDrawdowns[index])
    #         FiveLargestDrawdowns.clear()
    #         Drawdowns.clear()
        
    # def PrintMaximumDrawdown(self, index):
    #     print("Maximum Drawdown:", index)
    #     print(self.__MaximumDrawdowns[index], "%")

        
        
        
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
    
    sd.RollingAverageAlarm()
    
    
    
    
    
    sr = StatisticsCalculator(sd, bd)
    
    sr.PlotExcessReturns()
    
    sr.PrintMeanExcessReturns("Amazon")
    sr.PrintMeanExcessReturns("Facebook")
    sr.PlotMeanExcessReturns()
    
    sr.PrintStandardDeviationExcessReturns("Amazon")
    sr.PrintStandardDeviationExcessReturns("Facebook")
    sr.PlotStandardDeviationExcessReturns()
    
    sr.PrintSharpeRatio("Amazon")
    sr.PrintSharpeRatio("Facebook")
    sr.PlotSharpeRatio()
    
    
    sr.PrintSortinoRatio("Amazon")
    sr.PrintSortinoRatio("Facebook")
    sr.PlotSortinoRatio()
    sr.PrintMarketCorrelations("Amazon")
    sr.PrintMarketCorrelations("Facebook")
#    sr.PrintMaximumDrawdown("Amazon")
#    sr.PrintMaximumDrawdown("Facebook")
    
Main()