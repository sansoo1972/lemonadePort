#Lemonade Port

#Lemonade Source Code
#1 LOMEM: 14080
5 GOSUB 10000: GOSUB 11000: GOSUB 16000: GOTO 135
# <<< LEMONADE STAND >>>
# FROM AN ORIGINAL PROGRAM
# BY BOB JAMISON, OF THE
# MINNESOTA EDUCATIONAL
# COMPUTING CONSORTIUM
# * * *
# MODIFIED FOR THE APPLE
# FEBRUARY, 1979
# BY CHARLIE KELLNER

# Set Initial Values - commented out original Array
#135 DIM A(30),L(30),H(30),B(30),S(30),P(30),G(30)
#150 P9 = 10
#160 S3 = .15
#170 S2 = 30
#175 A2 = 2.00
#194 C9 = .5
#195 C2 = 1
startingAssets = 2.00
signCost = .15
s2 = 30
a2 = 2.00
c9 = .5
c2 = 1

# REM START OF GAME
310 GOSUB 12000: FOR I = 1 TO N:B(I) = 0:A(I) = A2: NEXT
710 IF D > 2 THEN 2000
800 REM INPUT VALUES
805 PRINT : POKE 34, PEEK (37)
810 FOR I = 1 TO N
815 A(I) = A(I) + .000000001
820 G(I) = 1:H(I) = 0
850 STI = A(I): GOSUB 4000: PRINT "LEMONADE STAND ";I; TAB( 26);"ASSETS ";STI$
855 PRINT
860 IF B(I) = 0 THEN 890
870 PRINT "YOU ARE BANKRUPT, NO DECISIONS"
875 PRINT "FOR YOU TO MAKE."
876 IF N = 1 AND A(1) < C THEN 31111
880 GOTO 1050

890 PRINT "HOW MANY GLASSES OF LEMONADE DO YOU"
895 PRINT "WISH TO MAKE ";
900 INPUT L(I)
901 IF L(I) < 0 OR L(I) > 1000 THEN 903
902 GOTO 906

903 PRINT "COME ON, LET'S BE REASONABLE NOW!!!"
904 PRINT "TRY AGAIN"
905 GOTO 890

906 IF L(I) < > INT (L(I)) THEN 903
910 IF L(I) * C1 < = A(I) THEN 950
920 PRINT "THINK AGAIN!!! YOU HAVE ONLY ";STI$
930 PRINT "IN CASH AND TO MAKE ";L(I);" GLASSES OF"
932 PRINT "LEMONADE YOU NEED $";L(I) * C1;" IN CASH."
940 GOTO 890

950 PRINT
951 PRINT "HOW MANY ADVERTISING SIGNS (";S3 * 100;" CENTS"
952 PRINT "EACH) DO YOU WANT TO MAKE ";
960 INPUT S(I)
961 IF S(I) < 0 OR S(I) > 50 THEN 963
962 GOTO 965
963 PRINT "COME ON, BE REASONABLE!!! TRY AGAIN."
964 GOTO 950

965 IF S(I) < > INT (S(I)) THEN 963
970 IF S(I) * S3 < = A(I) - L(I) * C1 THEN 1010
975 PRINT
980 STI = A(I) - L(I) * C1: GOSUB 4000
985 PRINT "THINK AGAIN, YOU HAVE ONLY ";STI$
990 PRINT "IN CASH LEFT AFTER MAKING YOUR LEMONADE."
1000 GOTO 950

1010 PRINT : PRINT "WHAT PRICE (IN CENTS) DO YOU WISH TO"
1012 PRINT "CHARGE FOR LEMONADE ";
1015 INPUT P(I)
1020 IF P(I) < 0 OR P(I) > 100 THEN 1022
1021 GOTO 1024

1022 PRINT "COME ON, BE REASONABLE!!! TRY AGAIN."
1023 GOTO 1010

1024 IF P(I) < > INT (P(I)) THEN 1022
1025 IF C5 = 1 THEN 1050
1050 VTAB 23: INPUT "WOULD YOU LIKE TO CHANGE ANYTHING
1290 P1 = M - E
1300 A(I) = A(I) + P1
1310 IF H(I) = 1 THEN 2300
1320 PRINT
1321 IF B(I) < > 1 THEN 1330
1326 PRINT "STAND ";I;: PRINT " BANKRUPT": GOSUB 18000
1327 GOTO 1390

1330 GOSUB 5000

1350 IF A(I) > C / 100 THEN 1390
1360 PRINT "STAND ";I
1365 HOME : PRINT " ...YOU DON'T HAVE ENOUGH MONEY LEFT"
1370 PRINT " TO STAY IN BUSINESS YOU'RE BANKRUPT!"
1380 B(I) = 1
1382 GOSUB 18000: HOME

1385 IF N = 1 AND B(1) = 1 THEN 31111
1390 NEXT I
1395 R1 = 1
1396 R2 = 0
1400 GOTO 400

2000 REM RANDOM EVENTS
2010 IF SC = 10 THEN 2110
2030 IF SC = 7 THEN 2410
2040 IF RND (1) < .25 THEN 2210
2050 GOTO 805

2100 IF X1 = 1 THEN 805 { unreachable }

2110 J = 30 + INT ( RND (1) * 5) * 10
2112 PRINT "THERE IS A ";J;"% CHANCE OF LIGHT RAIN,"
2115 PRINT "AND THE WEATHER IS COOLER TODAY."
2120 R1 = 1 - J / 100
2130 X1 = 1
2140 GOTO 805

2200 IF X2 = 1 THEN 805 { unreachable }

2210 PRINT "THE STREET DEPARTMENT IS WORKING TODAY."
2220 PRINT "THERE WILL BE NO TRAFFIC ON YOUR STREET."
2230 IF RND ( - 1) < .5 THEN 2233 { bug? rnd(-1) is a constant! }
2231 R2 = 2
2232 GOTO 2250
2233 R1 = .1
2250 X2 = 1
2260 GOTO 805
2
290 PRINT "THE STREET CREWS BOUGHT ALL YOUR"
2295 PRINT "LEMONADE AT LUNCHTIME!!"
2297 GOTO 1185

2300 REM THUNDERSTORM!
2310 X3 = 1:R3 = 0
2320 SC = 5: GOSUB 15000: TEXT : HOME
2330 PRINT "WEATHER REPORT: A SEVERE THUNDERSTORM"
2340 PRINT "HIT LEMONSVILLE EARLIER TODAY, JUST AS"
2350 PRINT "THE LEMONADE STANDS WERE BEING SET UP."
2360 PRINT "UNFORTUNATELY, EVERYTHING WAS RUINED!!"
2370 FOR J = 1 TO N:G(J) = 0: NEXT
2380 GOTO 1185

2400 IF X4 = 1 THEN 805
2410 X4 = 1
2430 PRINT "A HEAT WAVE IS PREDICTED FOR TODAY!"
2440 R1 = 2
2450 GOTO 805
3000 END

4000 REM STI => DOLLARS.CENTS
4010 STI = INT (STI * 100 + .5) / 100
4020 STI$ = "$" + STR$ (STI)
4030 IF STI = INT (STI) THEN STI$ = STI$ + ".0"
4040 IF STI = INT (STI * 10 + .5) / 10 THEN STI$ = STI$ + "0"
4050 RETURN

5000 VTAB 6: POKE 34,5
5002 PRINT " DAY ";D; TAB( 30);"STAND ";I: PRINT : PRINT
5010 PRINT " ";N2; TAB( 7);"GLASSES SOLD": PRINT
5012 STI = P(I) / 100: GOSUB 4000: PRINT STI$; TAB( 7);"PER GLASS";
5014 STI = M: GOSUB 4000: PRINT TAB( 27);"INCOME ";STI$
5016 PRINT : PRINT : PRINT " ";L(I); TAB( 7);"GLASSES MADE": PRINT
5020 STI = E: GOSUB 4000: PRINT " ";S(I); TAB( 7);"SIGNS MADE"; TAB( 25);"EXPENSES ";STI$: PRINT : PRINT
5030 STI = P1: GOSUB 4000: PRINT TAB( 16);"PROFIT ";STI$: PRINT
5040 STI = A(I): GOSUB 4000: PRINT TAB( 16);"ASSETS ";STI$
5060 GOSUB 18000

5070 REM
5090 HOME : RETURN

10000 REM INITIALIZE
10010 IN# 0: PR# 0
10100 POKE 770,173: POKE 771,48: POKE 772,192: POKE 773,136: POKE 774,208: POKE 775,5: POKE 776,206: POKE 777,1: POKE 778,3: POKE 779,240: POKE 780,9: POKE 781,202
10110 POKE 782,208: POKE 783,245: POKE 784,174: POKE 785,0: POKE 786,3: POKE 787,76: POKE 788,2: POKE 789,3: POKE 790,96: POKE 791,0: POKE 792,0
10190 RETURN

11000 REM INTRODUCTION
11100 TEXT : HOME : GR : COLOR= 12: FOR I = 0 TO 39: HLIN 0,39 AT I: NEXT : VTAB 2
11110 PRINT ";LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL;LLLLL";
11120 PRINT ";LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL;LLLLL";
11130 PRINT ";LLLL;;;;L;;;;;L;;;;L;;;;L;;;;L;;;;L;;;;";
11140 PRINT ";LLLL;LL;L;L;L;L;LL;L;LL;LLLL;L;LL;L;LL;";
11150 PRINT ";LLLL;;;;L;L;L;L;LL;L;LL;L;;;;L;LL;L;;;;";
11160 PRINT ";LLLL;LLLL;L;L;L;LL;L;LL;L;LL;L;LL;L;LLL";
11170 PRINT ";;;;L;;;;L;LLL;L;;;;L;LL;L;;;;L;;;;L;;;;";
11200 VTAB 11
11210 PRINT "LLLLLLLL;;;;;LL;LLLLLLLLLLLLLLL;LLLLLLLL";
11220 PRINT "LLLLLLLL;LLLLLL;LLLLLLLLLLLLLLL;LLLLLLLL";
11230 PRINT "LLLLLLLL;LLLLL;;;L;;;;L;;;;L;;;;LLLLLLLL";
11240 PRINT "LLLLLLLL;;;;;LL;LLLLL;L;LL;L;LL;LLLLLLLL";
11250 PRINT "LLLLLLLLLLLL;LL;LL;;;;L;LL;L;LL;LLLLLLLL";
11260 PRINT "LLLLLLLLLLLL;LL;LL;LL;L;LL;L;LL;LLLLLLLL";
11270 PRINT "LLLLLLLL;;;;;LL;LL;;;;L;LL;L;;;;LLLLLLLL";
11280 VTAB 23: PRINT " COPYRIGHT 1979 APPLE COMPUTER INC."
11300 GOSUB 11700: FOR I = 1 TO 2000: NEXT
11310 POKE 33,1: POKE 34,9: POKE 35,19
11320 FOR I = 39 TO 7 STEP - 1: COLOR= 15: VLIN 18,37 AT I: COLOR= 12: IF I < 39 THEN VLIN 18,36 AT I + 1
11330 COLOR= 15: IF I < 30 THEN VLIN 18,36 AT I + 10
11340 COLOR= 12: IF I < 29 THEN VLIN 18,37 AT I + 11: POKE 32,I + 11: VTAB 11: HTAB I + 12: PRINT : READ A$: PRINT A$;
11350 FOR J = 14 TO I + I: NEXT : NEXT : FOR I = 1 TO 1000: NEXT
11360 COLOR = 13: VLIN 14,36 AT 12: FOR I = 36 TO 20 STEP - 1: HLIN 8,16 AT I
11370 FOR J = 1 TO 50: NEXT : POKE 768,I * 3 - 12: POKE 769,12: CALL 770: NEXT : COLOR= 12: VLIN 14,19 AT 12
11400 POKE 32,0: POKE 33,40: POKE 34,20: POKE 35,23: VTAB 22
11410 FOR I = 1 TO 4000: NEXT :I = FRE (0)
11490 RETURN

11500 REM DATA
11510 DATA 96,180,128,60,114,60,128,120,144,60,152,60,128,255,128,60,114,60,85,120,96,60,102,60,114,120,102,60,96,255,0,0
11520 DATA ,,,,,,L;LL;,L;LL;,;;LL;;,L;LL;,L;;;;,,,;L;;;;,;L;LL;,;L;LL;,;L;LL;,;;;LL;,,,,,*
11530 DATA 96,16,85,4,128,4,96,4,76,4,128,4,96,16,0,0
11540 DATA 114,120,144,60,114,255,1,120,128,120,144,60,128,120,114,60,144,120,171,255,228,255,0,0
11550 DATA 152,180,152,120,152,60,144,120,152,60,171,120,192,60,152,255,0,0
11560 DATA 0,160,128,255,152,40,171,80,192,40,228,255,1,40,0,160,192,255,192,40,171,80,152,4 0,128,255,0,0

11700 REM MUSIC
11710 READ I,J: IF J = 0 THEN RETURN
11720 POKE 768,I: POKE 769,J: CALL 770
11730 GOTO 11710

12000 REM TITLE PAGE
12100 TEXT : HOME : PRINT CHR$ (7);
12110 PRINT "HI! WELCOME TO LEMONSVILLE, CALIFORNIA!": PRINT
12120 PRINT "IN THIS SMALL TOWN, YOU ARE IN CHARGE OF"
12130 PRINT "RUNNING YOUR OWN LEMONADE STAND. YOU CAN"
12140 PRINT "COMPETE WITH AS MANY OTHER PEOPLE AS YOU"
12150 PRINT "WISH, BUT HOW MUCH PROFIT YOU MAKE IS UP"
12160 PRINT "TO YOU (THE OTHER STANDS' SALES WILL NOT"
12170 PRINT "AFFECT YOUR BUSINESS IN ANY WAY). IF YOU"
12180 PRINT "MAKE THE MOST MONEY, YOU'RE THE WINNER!!": PRINT
12190 PRINT "ARE YOU STARTING A NEW GAME? (YES OR NO)"
12200 VTAB 21: CALL - 958: INPUT "TYPE YOUR ANSWER AND HIT RETURN ==> ";A$
12210 A$ = LEFT$ (A$,1): IF A$ < > "Y" AND A$ < > "N" THEN PRINT CHR$ (7);: GOTO 12200
12220 VTAB 23: CALL - 958: INPUT "HOW MANY PEOPLE WILL BE PLAYING ==> ";N$
12230 N = VAL (N$): IF N < 1 OR N > 30 THEN PRINT CHR$ (7);: GOTO 12220
12240 RETURN

13000 REM NEW BUSINESS
13100 HOME
13110 PRINT "TO MANAGE YOUR LEMONADE STAND, YOU WILL "
13120 PRINT "NEED TO MAKE THESE DECISIONS EVERY DAY: ": PRINT
13130 PRINT "1. HOW MANY GLASSES OF LEMONADE TO MAKE (ONLY ONE BATCH IS MADE EACH MORNING)"
13140 PRINT "2. HOW MANY ADVERTISING SIGNS TO MAKE (THE SIGNS COST FIFTEEN CENTS EACH) "
13150 PRINT "3. WHAT PRICE TO CHARGE FOR EACH GLASS ": PRINT
13160 PRINT "YOU WILL BEGIN WITH $2.00 CASH (ASSETS)."
13170 PRINT "BECAUSE YOUR MOTHER GAVE YOU SOME SUGAR,"
13180 PRINT "YOUR COST TO MAKE LEMONADE IS TWO CENTS "
13190 PRINT "A GLASS (THIS MAY CHANGE IN THE FUTURE).": PRINT
13200 GOSUB 18000

13202 HOME
13210 PRINT "YOUR EXPENSES ARE THE SUM OF THE COST OF"
13220 PRINT "THE LEMONADE AND THE COST OF THE SIGNS. ": PRINT
13230 PRINT "YOUR PROFITS ARE THE DIFFERENCE BETWEEN "
13240 PRINT "THE INCOME FROM SALES AND YOUR EXPENSES.": PRINT
13250 PRINT "THE NUMBER OF GLASSES YOU SELL EACH DAY "
13260 PRINT "DEPENDS ON THE PRICE YOU CHARGE, AND ON "
13270 PRINT "THE NUMBER OF ADVERTISING SIGNS YOU USE.": PRINT
13280 PRINT "KEEP TRACK OF YOUR ASSETS, BECAUSE YOU "
13290 PRINT "CAN'T SPEND MORE MONEY THAN YOU HAVE! ": PRINT
13300 GOSUB 18000

13302 HOME : RETURN

14000 REM CONTINUE OLD GAME
14100 CALL - 936: PRINT CHR$ (7);:I = 0
14110 PRINT "HI AGAIN! WELCOME BACK TO LEMONSVILLE! ": PRINT
14120 PRINT "LET'S CONTINUE YOUR LAST GAME FROM WHERE"
14130 PRINT "YOU LEFT IT LAST TIME. DO YOU REMEMBER "
14140 PRINT "WHAT DAY NUMBER IT WAS? ";
14150 INPUT "";A$:A = VAL (A$): PRINT : IF A < > 0 THEN 14200
14160 A$ = LEFT$ (A$,1): IF A$ = "Y" THEN PRINT "GOOD! WHAT DAY WAS IT? ";:I = I + 1: GOTO 14150
14170 IF A$ = "N" OR I > 0 THEN 14300
14180 PRINT CHR$ (7);"YES OR NO? ";:I = I + 1: GOTO 14150

14200 IF A < 1 OR A > 99 OR A < > INT (A) THEN 14300
14210 D = A

14300 PRINT "OKAY - WE'LL START WITH DAY NO. ";D + 1: PRINT
14400 FOR I = 1 TO N: PRINT : PRINT
14410 PRINT "PLAYER NO. ";I;", HOW MUCH MONEY (ASSETS)": PRINT
14420 PRINT "DID YOU HAVE? ";
14430 INPUT "";A$:A = VAL (A$): PRINT
14440 IF A < 2 THEN PRINT "O.K. - WE'LL START YOU OUT WITH $2.00":A = 2: GOTO
14490
14450 IF A > 40 THEN PRINT "JUST TO BE FAIR, LET'S MAKE THAT $10.00":A = 10
14490 A(I) = INT (A * 100 + .5) / 100: NEXT
14500 PRINT : PRINT CHR$ (7): INPUT "...READY TO BEGIN? ";A$
14510 IF LEFT$ (A$,1) = "N" THEN 13000
14520 RETURN

15000 REM WEATHER DISPLAY
15100 GR : HOME
15110 COLOR= SC: FOR I = 0 TO 25: HLIN 0,39 AT I: NEXT I
15120 COLOR= 12: FOR I = 26 TO 39: HLIN 0,39 AT I: NEXT I
15130 COLOR= 8: FOR I = 24 TO 32: HLIN 15,25 AT I: NEXT I
15150 COLOR= 13: FOR I = 17 TO 23 STEP 2: VLIN 22,23 AT I: NEXT I
15151 IF SC = 2 OR SC = 7 THEN 15160
15152 IF SC = 10 THEN COLOR= 15
15157 IF SC = 5 THEN COLOR= 0
15158 HLIN 6,10 AT 2: HLIN 4,14 AT 3: HLIN 7,12 AT 4: HLIN 22,30 AT 4: HLIN 20,36 AT 5: HLIN 23,33 AT 6::: GOSUB 17000: GOTO 15170
15160 IF SC = 7 THEN COLOR= 9
15162 HLIN 3,5 AT 1: HLIN 2,6 AT 2: FOR I = 3 TO 6: HLIN 1,7 AT I: NEXT : HLIN 2,6 AT 7: HLIN 3,5 AT 8
15170 VTAB 22: HTAB 8: PRINT " LEMONSVILLE WEATHER REPORT ": PRINT
15175 VTAB 22: HTAB 8: PRINT " LEMONSVILLE WEATHER REPORT ": PRINT
15180 IF SC = 2 THEN HTAB 18: PRINT " SUNNY ";
15182 IF SC = 7 THEN HTAB 15: PRINT " HOT AND DRY ";
15184 IF SC = 10 THEN HTAB 17: PRINT " CLOUDY ";
15186 IF SC = 5 THEN HTAB 14: PRINT " THUNDERSTORMS! ";: GOSUB 17000
15200 RESTORE
15210 READ A$: IF A$ < > "*" THEN 15210
15220 IF SC < > 2 THEN 15300
15230 READ I,J: IF J = 0 THEN 15500
15240 FOR K = 1 TO J: POKE 768,I: POKE 769,10: CALL 770
15250 FOR L = K TO J: NEXT : NEXT : GOTO 15230
15300 READ I,J: IF J < > 0 THEN 15300
15310 IF SC = 7 THEN 15400
15320 READ I,J: IF J < > 0 THEN 15320
15330 IF SC = 10 THEN 15400
15340 READ I,J: IF J < > 0 THEN 15340
15400 READ I,J: IF J = 0 THEN 15500
15410 IF I = 1 THEN FOR I = 1 TO J: NEXT : GOTO 15400
15420 POKE 768,I: POKE 769,J: CALL 770
15430 GOTO 15400
15440 IF SC = 5 THEN GOSUB 17000
15500 IF SC = 5 THEN GOSUB 17000
15510 I = FRE (0): FOR I = 1 TO 2000: NEXT : RETURN
16000 POKE 13824,76: POKE 13825,108: POKE 13826,54: POKE 13827,165: POKE 13828,48: POKE 13829,41: POKE 13830,15: POKE 13831,141: POKE 13832,160: POKE 13833,54:
16010 POKE 13834,165: POKE 13835,48: POKE 13836,41: POKE 13837,240: POKE 13838,141: POKE 13839,161: POKE 13840,54: POKE 13841,165: POKE 13842,36: POKE 13843,141:
16020 POKE 13844,162: POKE 13845,54: POKE 13846,165: POKE 13847,37: POKE 13848,141: POKE 13849,163: POKE 13850,54: POKE 13851,169: POKE 13852,0: POKE 13853,133:
16030 POKE 13854,36: POKE 13855,133: POKE 13856,37: POKE 13857,72: POKE 13858,32: POKE 13859,193: POKE 13860,251: POKE 13861,133: POKE 13862,40: POKE 13863,164:
16040 POKE 13864,36: POKE 13865,177: POKE 13866,40: POKE 13867,41: POKE 13868,15: POKE 13869,205: POKE 13870,164: POKE 13871,54: POKE 13872,208: POKE 13873,10:
16050 POKE 13874,177: POKE 13875,40: POKE 13876,41: POKE 13877,240: POKE 13878,24: POKE 13879,109: POKE 13880,160: POKE 13881,54: POKE 13882,145: POKE 13883,40:
16060 POKE 13884,177: POKE 13885,40: POKE 13886,41: POKE 13887,240: POKE 13888,205: POKE 13889,165: POKE 13890,54: POKE 13891,208: POKE 13892,10: POKE 13893,177:
16070 POKE 13894,40: POKE 13895,41: POKE 13896,15: POKE 13897,24: POKE 13898,109: POKE 13899,161: POKE 13900,54: POKE 13901,145: POKE 13902,40: POKE 13903,200:
16080 POKE 13904,192: POKE 13905,40: POKE 13906,144: POKE 13907,213: POKE 13908,160: POKE 13909,0: POKE 13910,104: POKE 13911,105: POKE 13912,0: POKE 13913,197:
16090 POKE 13914,34: POKE 13915,144: POKE 13916,196: POKE 13917,32: POKE 13918,193: POKE 13919,251: POKE 13920,133: POKE 13921,40: POKE 13922,173: POKE 13923,162:
16100 POKE 13924,48: POKE 13925,133: POKE 13926,36: POKE 13927,173: POKE 13928,163: POKE 13929,54: POKE 13930,133: POKE 13931,37: POKE 13932,165: POKE 13933,48:
16110 POKE 13934,41: POKE 13935,15: POKE 13936,141: POKE 13937,164: POKE 13938,54: POKE 13939,165: POKE 13940,48: POKE 13941,41: POKE 13942,240: POKE 13943,141:
16120 POKE 13944,165: POKE 13945,54: POKE 13946,96: POKE 13947,0:
16130 RETURN

17000 IF SC < > 5 THEN RETURN
17001 COLOR= 10: VLIN 7,9 AT 29: HLIN 30,31 AT 9: VLIN 9,14 AT 32: HLIN 33,34 AT 14: VLIN 14,25 AT 35
17005 VLIN 5,8 AT 8: PLOT 9,8: VLIN 8,13 AT 10: PLOT 11,13: VLIN 13,17 AT 12
17010 FOR RPT = 1 TO 5
17020 CALL 13824
17030 COLOR= 7: CALL 13827
17040 CALL 13824
17050 COLOR= 9: CALL 13827
17060 NEXT RPT
17070 CALL 13824
17080 COLOR= 5: CALL 13827
17090 RETURN

18000 VTAB 24: PRINT " PRESS SPACE TO CONTINUE, ESC TO END...";
18010 GET IN$: IF IN$ < > " " AND ASC (IN$) < > 27 THEN 18010
18020 IF ASC (IN$) = 27 THEN 31111
18030 RETURN

31111 FOR I = 1 TO 2000: NEXT : HOME : VTAB 10: PRINT "WOULD YOU LIKE TO PLAY AGAIN ";
31112 GET IN$: IF IN$ = "Y" THEN 150
31113 IF PEEK (994) + PEEK (1001) = 192 THEN CALL 976
31114 TEXT : HOME : TEXT : END
