class App(Application):
    kFileQuitShortcut = ""
    kFileQuit = "Quit"
    kEditClea = ""

class MainWindow(Window):
    kStartingAssets = 2.00
    kSignCost = 0.15
    kNewDayPage = 0
    kResultsPage = 1
    kP9 = 10
    kS2 = 30
    kC9 = 0.5
    kC2 = 1
    kWeatherSunny = 2
    kWeatherHot = 7
    kWeatherCloudy = 10
    kWeatherStorm = 5
    
    def Open(self, Event):
        self.InitGame(1)
        self.StartNewDay()

    def StartNewDay(self):
        self.Day += 1
        self.MakeWeather()
        self.WeatherTitleTxt.text = "Weather Report for Day " + str(self.Day)
        self.CostLabelTxt.text = "On day " + str(self.Day) + ", the cost of lemonade is:"
        specialEvent = self.DoRandomEvents()
        if specialEvent != "":
            self.WeatherTxt.text = self.WeatherTxt.text + "\n" + specialEvent
        self.ShowDecisionPage()

    def InitGame(self, qty):
        self.QtyPlayers = qty
        self.Assets = [None] * qty
        self.GlassesMade = [None] * qty
        self.GlassesSold = [None] * qty
        self.PricePerGlass = [None] * qty
        self.SignsMade = [None] * qty
        for i in range(qty):
            self.Assets[i] = self.kStartingAssets
        self.WeatherFactor = 1.0
    
    def CalculateResults(self):
        specialResult = ""
        N1 = 0
        if self.PricePerGlass[self.CurPlayer] >= self.kP9:
            N1 = ((self.kP9 ** 2) * self.kS2 / self.PricePerGlass[self.CurPlayer] ** 2)
        else:
            N1 = (self.kP9 - self.PricePerGlass[self.CurPlayer]) / self.kP9 * 0.8 * self.kS2 + self.kS2
        W = -self.SignsMade[self.CurPlayer] * self.kC9
        adBenefit = 1 - (math.exp(W) * self.kC2)
        N2 = math.floor(self.WeatherFactor * N1 * (1 + adBenefit))
        if self.StormBrewing:
            self.Weather = self.kWeatherStorm
            self.UpdateWeatherReport()
            self.PlayThunderClap()
            self.Player.PlaySong(100, 180, "0,8 55,2 67,3 64,1 62,2 60,1 57,6 55,2 60,4 60,1 62,2 64,1 67,4")
            N2 = 0
            if self.GlassesMade[self.CurPlayer] > 0:
                specialResult = "All lemonade was ruined."
        elif self.StreetCrewThirsty:
            N2 = self.GlassesMade
