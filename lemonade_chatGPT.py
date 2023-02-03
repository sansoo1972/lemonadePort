class App(Application):
    kFileQuitShortcut = ""
    kFileQuit = "Quit"
    kEditClea = None

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


class MainWindow:
    def open(self, event):
        self.init_game(1)
        self.start_new_day()

    def start_new_day(self):
        self.day += 1
        self.make_weather()
        self.weather_title_txt.text = "Weather Report for Day " + str(self.day)
        self.cost_label_txt.text = "On day " + str(self.day) + ", the cost of lemonade is:"
        special_event = self.do_random_events()
        if special_event != "":
            self.weather_txt.text = self.weather_txt.text + "\n" + special_event
        self.show_decision_page()

    def init_game(self, qty):
        self.qty_players = qty
        self.assets = [0.0] * (self.qty_players - 1)
        self.glasses_made = [0] * (self.qty_players - 1)
        self.glasses_sold = [0] * (self.qty_players - 1)
        self.price_per_glass = [0.0] * (self.qty_players - 1)
        self.signs_made = [0] * (self.qty_players - 1)
        for i in range(self.qty_players):
            self.assets[i] = kStartingAssets
        self.weather_factor = 1.0

def CalculateResults():
    # calculate how many glasses are sold
    specialResult = ""
    N1 = 0.0
    if pricePerGlass(CurPlayer) >= kP9:
        N1 = ((kP9 ** 2) * kS2 / pricePerGlass(CurPlayer) ** 2)
    else:
        N1 = (kP9 - pricePerGlass(CurPlayer)) / kP9 * 0.8 * kS2 + kS2
    W = -signsMade(CurPlayer) * kC9
    # % increase in sales due to ads
    adBenefit = 1 - (math.exp(W) * kC2)
    N2 = math.floor(WeatherFactor * N1 * (1 + adBenefit))
    if StormBrewing:
        Weather = kWeatherStorm
        UpdateWeatherReport()
        PlayThunderClap()
        Player.PlaySong(100, 180, "0,8 55,2 67,3 64,1 62,2 60,1 57,6 55,2 60,4 60,1 62,2 64,1 67,4")
        N2 = 0
        if glassesMade(CurPlayer) > 0:
            specialResult = "All lemonade was ruined."
    elif StreetCrewThirsty:
        N2 = glassesMade(CurPlayer)
        specialResult = "The street crews bought all your lemonade at lunchtime!"
    GlassesSold[CurPlayer] = min(N2, glassesMade(CurPlayer))
    # calculate income and expenses
    expenses = glassesMade(CurPlayer) * CostPerGlass/100 + signsMade(CurPlayer) * kSignCost
    income = GlassesSold[CurPlayer] * pricePerGlass(CurPlayer) / 100
    # adjust assets
    Assets[CurPlayer] = Assets[CurPlayer] + income - expenses
    # put all this into the results display
    SpecialResultTxt.text = specialResult
    GlassesSoldTxt.text = str(GlassesSold[CurPlayer])
    if GlassesSold[CurPlayer] == 1:
        GlassesSoldLbl.text = "Glass Sold"
    else:
        GlassesSoldLbl.text = "Glasses Sold"
    PricePerGlassTxt.text = DFormat(pricePerGlass(CurPlayer) / 100)
    SalesIncTxt.text = DFormat(GlassesSold[CurPlayer] * pricePerGlass(CurPlayer) / 100)
    GlassesMadeTxt.text = str(glassesMade(CurPlayer))
    if glassesMade(CurPlayer) == 1:
        GlassesMadeLbl.text = "Glass Made"
    else:
        GlassesMadeLbl.text = "Glasses Made"
    CostPerGlassTxt.text = DFormat(CostPerGlass / 100)
    LemonadeExpTxt.text = DFormat(glassesMade(CurPlayer) * CostPerGlass / 100)
    SignsMadeTxt.text = str(signsMade(CurPlayer))
    if signsMade(CurPlayer) == 1:
        SignsMadeLbl.text = "Sign Made"
    else:
        SignsMadeLbl.text = "Signs Made"
    CostPerSignTxt.text = DFormat(kSignCost)
    AdExpTxt.text = DFormat(signsMade

def ShowResults(self):
    DayTxt.text = "Day " + str(Day)
    StandTxt.text = "Stand " + str(CurPlayer + 1)
    Panel.Value = kResultsPage
    if Profitable:
        Player.PlaySong(4, 125, "64,2 67,3 64,1 65,2 67,4")

def DFormat(value):
  if value < 0.00:
    return "$-" + format(value, "0.00")
  else:
    return "$" + format(value, "0.00")

def MakeWeather(self):
    r = random.random()
    if r < 0.6:
        self.Weather = kWeatherSunny
    elif r < 0.8:
        self.Weather = kWeatherCloudy
    else:
        if self.Day < 3: 
            self.Weather = kWeatherSunny 
        else: 
            self.Weather = kWeatherHot
    self.ChanceOfRain = 0
    if self.Weather == kWeatherCloudy:
        self.ChanceOfRain = 30 + int(random.random() * 5) * 10
        self.WeatherFactor = 1.0 - self.ChanceOfRain / 100
        Player.PlaySong(97, 175, "64,3 64,2 64,1 65,2 64,1 62,2 60,1 64,5")
    elif self.Weather == kWeatherHot:
        self.WeatherFactor = 2.0
        Player.PlaySong(20, 175, "69,2 67,1 69,5 67,2 65,1 67,2 69,2 65,3 62,3 57,5")
    else:
        self.WeatherFactor = 1.0
        Player.PlaySong(76, 250, "72,3 74,1 67,1 72,1 76,1 67,1 72,5")
    self.UpdateWeatherReport()

def update_weather_report(self):
    report = ""
    if weather == "kWeatherSunny":
        report = "Sunny"
        self.weather_canv.backdrop = "SunnyPic"
    elif weather == "kWeatherCloudy":
        report = "Cloudy\nThere is a {}% chance of light rain, and the weather is cooler today.".format(chance_of_rain)
        self.weather_canv.backdrop = "CloudyPic"
    elif weather == "kWeatherHot":
        report = "Hot and Dry\nA heat wave is predicted for today!"
        self.weather_canv.backdrop = "HotAndDryPic"
    elif weather == "kWeatherStorm":
        report = "Thunderstorms!\nA severe thunderstorm hit Lemonsville earlier today, just as the lemonade stands were being set up. Unfortunately, everything was ruined!"
        self.weather_canv.backdrop = "StormPic"

    self.weather_txt.text = report

    def do_random_events(self):
    special_desc = ""
    street_crew_thirsty = False
    storm_brewing = False
    if weather == "kWeatherCloudy":
        if random.random() < 0.25:
            storm_brewing = True
    elif weather == "kWeatherHot":
        # heat wave (see original source line 2410)...
        # already handled in MakeWeather
        pass
    else:
        if random.random() >= 0.25:
            return ""  # no special event today
        # street department is working (original source line 2210)
        special_desc = "The street department is working today. There will be no traffic on your street."
        if random.random() < 0.5:
            street_crew_thirsty = True
        else:
            weather_factor = 0.1
    return special_desc

def validate(self):
    # Make sure the user's inputs are reasonable.
    valid = True
    glasses = int(self.inp_glass_fld.text)
    if glasses < 0 or glasses > 1000:
        valid = False
    signs = int(self.inp_sign_fld.text)
    if signs < 0 or signs > 50:
        valid = False
    price = int(self.inp_price_fld.text)
    if price < 0 or price > 100:
        valid = False
    if glasses * cost_per_glass / 100 + signs * k_sign_cost > assets[cur_player]:
        valid = False
    self.decision_ok_butn.enabled = valid

class MainWindow:
    def play_thunder_clap(self):
        note_player_1 = NotePlayer()
        note_player_1.instrument = 118
        note_player_1.play_note(20, 60)
        note_player_1.instrument = 123
        note_player_1.play_note(21, 120)
        note_player_1.instrument = 122
        note_player_1.play_note(22, 100)

    def set_qty_players(self, new_qty_players):
        init_game(new_qty_players)

def ShowDecisionPage(self):
    self.DecisionTitleTxt.text = "Decisions for Lemonade Stand " + str(self.CurPlayer + 1)
    explanation = ""
    if self.Day < 3:
        self.CostPerGlass = 2
    elif self.Day < 7:
        self.CostPerGlass = 4
        if self.Day == 3:
            explanation = "(Your mother quit giving you free sugar.)"
    else:
        self.CostPerGlass = 5
        if self.Day == 7:
            explanation = "(The price of lemonade mix just went up.)"
    self.CostTxt.text = "$.0" + str(self.CostPerGlass)
    self.CostExpTxt.text = explanation
    self.AssetsTxt.text = "$" + format(self.Assets[self.CurPlayer], "-0.00")
    self.InpGlassLabel.text = "How many glasses of lemonade (" + format(self.CostPerGlass, "0") + " cents each) do you wish to make?"
    self.InpSignLabel.text = "How many advertising signs (" + format(self.kSignCost * 100, "0") + " cents each) do you want to make?"
    self.InpGlassFld.text = str(self.GlassesMade[self.CurPlayer])
    self.InpSignFld.text = str(self.SignsMade[self.CurPlayer])
    self.InpPriceFld.text = str(self.PricePerGlass[self.CurPlayer])
    self.Validate()
    self.Panel.Value = self.kNewDayPage
    self.InpGlassFld.SetFocus()
    self.InpGlassFld.SelStart = 0
    self.InpGlassFld.SelLength = 99999


class MainWindow:
    CostPerGlass = None # Cost of lemonade per glass, in cents.
    Day = None # Which day of the game we're on.

    class WeatherCanv:
        def paint(self, g):
            g.draw_rect(0, 0, self.width, self.height)

    class DecisionOKButn:
        def action(self):
            GlassesMade[CurPlayer] = float(InpGlassFld.text)
            SignsMade[CurPlayer] = float(InpSignFld.text)
            PricePerGlass[CurPlayer] = float(InpPriceFld.text)
            CurPlayer = CurPlayer + 1
            if CurPlayer >= QtyPlayers:
                CurPlayer = 0
                CalculateResults
                ShowResults
            else:
                ShowDecisionPage

    class InpGlassFld:
        def text_change(self):
            Validate

    class InpSignFld:
        def text_change(self):
            Validate

    class InpPriceFld:
        def text_change(self):
            Validate

    class ResultsOKButn:
        def action(self):
            CurPlayer = CurPlayer + 1
            if CurPlayer >= QtyPlayers:
                CurPlayer = 0
                StartNewDay
            else:
                CalculateResults

