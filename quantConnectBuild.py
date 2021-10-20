##Data --> Algo --> API --> Broker = Trade execution 
##Quantpedia.com to check for strategies to be defined and for backtesting; alphas can CHANGE 
##Backtesting results < real results --> overfitting biases, look ahead biases, etc 

######################
##### FLOW CHART #####
######################

##Research --> Coding --> Backtesting --> Optimizing --> Paper trading --> Live trading --> Monitoring 
##Bull trend = SMA20 > SMA50 > SMA200 
##Use lean engine; access the past and the present but can lead to some confusion 

##QuantConnect --> Has two types of data: tick (start and end time are the same) and bar data (start time and end time)
##QC recalls the END time; cannot access data beyond the time frontier 

""" Symbol objects 
Value 
SecurityType
Market 
HasUnderlying 
Date 
OptionType
OptionRight
StrikePrice  """

######## Buy and hold SPY ##################
######## Closes for loss/profit 10% ########
######## Reinvest ##########################

from os import stat_result


class MeasuredOrangeFish(QCAlgorithm)
    def Initialize(self): 
        self.SetStartDate(2020 10, 30) ### SET START DATE
        self.SetEndDate(2021,10,30)
        self.SetCash(10000) ### SET STRATEGY CASH
        
        tsla = self.AddEquity("TSLA", Resolution.Minute)
        #SPY = self.AddEquity("SPY", Rsolution.Daily)
        """ Alternative security types: self.AddForex, self.AddFuture... """

        TSLA.SetDataNormalizationMode(DataNormalizationMode.Raw)
        ## OPTIONS ONLY SUPPORT RAW; DEFAULT IS DIVIDEND ADJUSTED AND SMOOTHED OUT ##
        ## CHANGING NORMALIZATION TO RAW FOR OPTIONS ##

        self.tsla = tsla.symbol

        self.SetBenchmark("QQQ")
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        ## CASH ACCOUNT WORKS TOO BUT NEED TO FACTOR IN T+3 SETTLEMENT RULES TO AVOID PDT ##

        self.entryPrice = 0 
        self.period = timedelta(1) #One day; can change to 31 if looking at daily
        self.nextEntryTime = self.Time
        ## Initialize next entry based on time ## 

    def OnData(self,data):
        """ data = slice object
        class Slice: TradeBars, quoteBars, ticks, optionChains, futureCHains, dividends, delisting, symbolChangedEvents 
        ticks contains last price; be cautious when using
        tradeBars contains candles; shows open, close, high, low, volume <-- equities, options, futures 
        quoteBars contains bid and asks prices; shows open, high, low, close <-- ALL assets """

        if not self.tsla in data: 
            return 

        #price = data.Bars[self.tsla].Close 
        price = data[self.data].Close 
        #price = self.Securities[self.tsla].Close

        if not self.Portfolio.Invested: 
            if self.nextEntryTime <= self.Time:
                 self.SetHoldings(self.tsla, 1) ## 1 here means using 100% ## 
                #self.MarketOrder(self.tsla, int(self.Portfolio.Cash / price) )
                self.Log("BUY TSLA @" + str(price))
                price = self.entryPrice

        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price: 
            self.liquidate()
            self.Log("SELL TSLA @" + str(price))
            self.nextEntryPrice = self.Time + self.period 

######## Conclusion from backtesting ################
######## IT doesn't work well with BEAR markets #####
######## Arbitary; waiting for one day ##############
######## after a 10% move is not EFFECTIVE ##########
        
""" self.Portfolio.
                #Invested = hold at least one stock 
                #Cash = sum of all currencies in account (only settled) 
                #UnsettledCash = sum of all currencies in account (only unsettled)
                #TotalFees = fees incurred since backtest start 
                #TotalHoldingsValue = absolute sum of portfolio 
                #MarginRemaining = remaining margin on the account 
                #TotalPortfolioValue = portfolio equity 
                #TotalProfit = sum of all gross profit 
                #TotalUnrealizedProfit = holdings profit/loss """