import numpy as np #USE to calculate STD for volatility adjusted lookback link

class MultidimensionalTransdimensionalSplitter(QCAlgorithm): 
    def Initialize(self):
        self.SetStartDate(2020, 3, 20) #SET start date 
        self.SetEndDate(2021, 3, 20) #SET end date 
        
        self.SetCash(10000) #SET strategy cash 
        
        self.Symbol = self.AddEquity("SPY", Resolution.Minute).symbol
        
        self.LookBack = 20 #ARBIITARY; subjected to change
        self.Ceiling, self.Floor = 30. 10 #10 days is lower and 30 days is upper limits to prevent burden
        self.InitialStopRisk = 0.9 #10% loss before it gets hit 
        self.TrailingStopRisk = 0.85 #adjusted for typical pullback 
        
        #20 minutes after opening to generate trends for the day
        self.Schedule.On(self.DataRules.Everyday(self.Symbol), self.TimeRules.AfterMarketOpen(self.Symbol, 20), Action(self.EverydayMarketOpen))
    
    def OnData(self, data):
        self.Plot("Data Chart", self.Symbol, self.Securities[self.Symbol].close)
    
    def EveryMarketOpen(): 
        close = self.History(self.Symbol, 31, Resolution.Daily)["close"]
        todayvol = np.std(close[1:31])
        yesterdayvol = np.std(close[0:30])
        deltavol = (todayvol - yesterdayvol) / todayvol
        self.LookBack = round(self.LookBack * (1+ deltavol))

        if self.LookBack > self.ceiling: 
            self.LookBack = self.ceiling

        elif self.LookBack < self.Floor:
            self.LookBack = self.Floor

        self.high = self.History(self.Symbol, self.LookBack, Resolution.Daily)["high"]

        if not self.Securities[self.Symbol].Invested and 
                                self.Securities[self.Symbol].Close >= max(self.high[:-1]): 
                                #don't want to compare yesteday highs and yesterday's lows
        self.SetHoldings(self.Symbol, 1) #focusing solely on SPY levels so it will be 1
        self.breakoutlevel = max(self.high[:-1])
        self.highestPrice = self.breakoutlevel

        if self.Securities[self.Symbol].Invested: 
            if not self.Transactions.GetOpenOrders(self.symbol): 
                self.stopMarketTicker = self.StopMarketOrder(self.Symbol, -self.Portfolio[self.Symbol].Quantity, self.InitialStopRisk * self.breakoutlevel)

            if self.Securities[self.symbol].Close > self.highestPrice and 
                                self.InitialStopRisk * self.breakoutlevel < self.Securities[self.Symbol].Close * self.TrailingStopRisk: 
                self.highestPrice = self.Securities[self.Symbol].close
                updateFields = UpdateOrderFields() 
                updateFields.StopPrice = self.Securities[self.symbol].Close * self.TrailingStopRisk
                self.stopMarketTicker.Update(updateFields)

                self.Debug(updateFields.StopPrice) #Quants equivalent to print

        self.Plot("Data Chart", "Stop Price", self.stopMarketTicker.Get(OrderField.StopPrice))