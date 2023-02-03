# LEMONADE STAND - PYTHON VERSION
# Setting memory allocation
# LOMEM = 14080

# GOSUB calls
import random


def gosub_10000():
    pass


def gosub_11000():
    pass


def gosub_16000():
    pass


gosub_10000()
gosub_11000()
gosub_16000()

# Remarks
# <<< LEMONADE STAND >>>
# FROM AN ORIGINAL PROGRAM BY BOB JAMISON, OF THE MINNESOTA EDUCATIONAL COMPUTING CONSORTIUM
# *  *  *
# MODIFIED FOR THE APPLE FEBRUARY, 1979
# BY CHARLIE KELLNER

# Arrays
A = [0] * 30
L = [0] * 30
H = [0] * 30
B = [0] * 30
S = [0] * 30
P = [0] * 30
G = [0] * 30

# Constants
P9 = 10
S3 = 0.15
S2 = 30
A2 = 2.00
C9 = 0.5
C2 = 1

# Start of game


def gosub_12000():
    pass


def gosub_13000():
    pass


def gosub_14000():
    pass


gosub_12000()

for i in range(1, N + 1):
    B[i - 1] = 0
    A[i - 1] = A2

if A$ == "Y":
    gosub_13000()
else:
    gosub_14000()


# Weather report
SC = random.random()

if SC < 0.6:
    SC = 2
elif SC < 0.8:
    SC = 10
else:
    SC = 7

if D < 3:
    SC = 2


def gosub_15000():
    pass


gosub_15000()

# Start of new day
D = D + 1
print("ON DAY ", D, ", THE COST OF LEMONADE IS $.0", end="")

C = 2
if D > 2:
    C = 4
if D > 6:
    C = 5

print(C)

C1 = C * 0.01
R1 = 1

# Current events
if D < > 3:
    print("(YOUR MOTHER QUIT GIVING YOU FREE SUGAR)")
elif D < > 7:
    print("(THE PRICE OF LEMONADE MIX JUST WENT UP)")

# After 2 days things can happen
if D > 2:
    2000

n = int(input("Enter the number of values: "))

for i in range(1, n + 1):
    a[i] = a[i] + 0.000000001
    g[i] = 1
    h[i] = 0

    sti = a[i]
    print("LEMONADE STAND {}    ASSETS {}".format(i, sti))
    print()

    if b[i] == 0:
        print("YOU ARE BANKRUPT, NO DECISIONS TO MAKE.")
        if n == 1 and a[1] < c:
            pass
        continue

    print("How many glasses of lemonade do you wish to make?")
    l[i] = int(input())
    if l[i] < 0 or l[i] > 1000:
        print("Come on, let's be reasonable now!!!")
        print("Try again")
        i -= 1
        continue

    if l[i] * c1 <= a[i]:
        print("How many advertising signs do you want to make?")
        s[i] = int(input())
        if s[i] < 0 or s[i] > 50:
            print("Come on, be reasonable!!! Try again.")
            i -= 1
            continue

        if s[i] * s3 <= a[i] - l[i] * c1:
            print("What price (in cents) do you wish to charge for lemonade?")
            p[i] = int(input())
            if p[i] < 0 or p[i] > 100:
                print("Come on, be reasonable!!! Try again.")
                i -= 1
                continue

A = input("WOULD YOU LIKE TO CHANGE ANYTHING?")
if A[0].upper() == "Y":
    C5 = 1
    # HOME not defined
    # GOTO not supported in Python
else:
    C5 = 0
    # TEXT not defined
    # HOME not defined

if SC == 10 and random.random() < 0.25:
    # Go to line 2300

print("$$ LEMONSVILLE DAILY FINANCIAL REPORT $$")
print()


# Calculate Profits
if R2 == 2:
    goto 2290
if R3 == 3:
    goto 2350
for i in range(1, N+1):
    if A[i-1] < 0:
        A[i-1] = 0
    if R2 == 2:
        goto 1260
    if P[i-1] >= P9:
        N1 = (P9 - P[i-1]) / P9 * 0.8 * S2 + S2
        goto 1230
    N1 = (P9 ** 2 * S2) / (P[i-1] ** 2)
    W = -S[i-1] * C9
    V = 1 - (math.exp(W) * C2)
    N2 = R1 * (N1 + (N1 * V))
    N2 = int(N2 * G[i-1])
    if N2 <= L[i-1]:
        N2 = L[i-1]
    M = N2 * P[i-1] * 0.01
    E = S[i-1] * S3 + L[i-1] * C1
    P1 = M - E
    A[i-1] += P1
    if H[i-1] == 1:
        goto 2300
    print()
    if B[i-1] != 1:
        goto 1330
    print("STAND ", i)
    print("   BANKRUPT")
    goto 18000
    goto 1390
    if A[i-1] > C / 100:
        goto 1390
    print("STAND ", i)
    print("  ...YOU DON'T HAVE ENOUGH MONEY LEFT")
    print(" TO STAY IN BUSINESS  YOU'RE BANKRUPT!")
    B[i-1] = 1
    goto 18000
    if N == 1 and B[0] == 1:
        goto 31111
R1 = 1
R2 = 0
goto 400


def random_events(SC, X1, X2, R1, R2):
    if SC == 10:
        return light_rain(X1)
    if SC == 7:
        return 2410
    if random.random() < 0.25:
        return street_block(X2, R1, R2)
    return 805


def light_rain(X1):
    if X1 == 1:
        return 805
    J = 30 + int(random.random() * 5) * 10
    print("THERE IS A " + str(J) + "% CHANCE OF LIGHT RAIN,")
    print("AND THE WEATHER IS COOLER TODAY.")
    R1 = 1 - J / 100
    X1 = 1
    return 805


def street_block(X2, R1, R2):
    if X2 == 1:
        return 805
    print("THE STREET DEPARTMENT IS WORKING TODAY.")
    print("THERE WILL BE NO TRAFFIC ON YOUR STREET.")
    if random.random() < 0.5:
        R2 = 2
        return 2250
    R1 = 0.1
    X2 = 1
    return 2250


def street_crews(R1, R2):
    print("THE STREET CREWS BOUGHT ALL YOUR")
    print("LEMONADE AT LUNCHTIME!!")
    return 1185


x3 = 1
r3 = 0
sc = 5

print("WEATHER REPORT:  A SEVERE THUNDERSTORM")
print("HIT LEMONSVILLE EARLIER TODAY, JUST AS")
print("THE LEMONADE STANDS WERE BEING SET UP.")
print("UNFORTUNATELY, EVERYTHING WAS RUINED!!")

for j in range(1, n+1):
    g[j] = 0

if x4 == 1:
    goto 805

x4 = 1
print("A HEAT WAVE IS PREDICTED FOR TODAY!")
r1 = 2

goto 805


def dollars_cents(sti):
    sti = int(sti * 100 + 0.5) / 100
    sti_str = "$" + str(sti)
    if sti == int(sti):
        sti_str = sti_str + ".0"
    if sti == int(sti * 10 + 0.5) / 10:
        sti_str = sti_str + "0"
    return sti_str


def print_output(d, i, n2, p, m, l, s, p1, a):
    print("   DAY ", d, " STAND ", i, sep="")
    print()
    print("  ", n2, " GLASSES SOLD", sep="")
    sti = p[i] / 100
    sti_str = dollars_cents(sti)
    print(sti_str, " PER GLASS", sep="")
    sti = m
    sti_str = dollars_cents(sti)
    print("       INCOME ", sti_str, sep="")
    print()
    print("  ", l[i], " GLASSES MADE", sep="")
    sti = s[i]
    print("  ", s[i], " SIGNS MADE", end="")
    sti = e
    sti_str = dollars_cents(sti)
    print(" EXPENSES ", sti_str, sep="")
    print()
    sti = p1
    sti_str = dollars_cents(sti)
    print("    PROFIT ", sti_str, sep="")
    print()
    sti = a[i]
    sti_str = dollars_cents(sti)
    print("    ASSETS ", sti_str, sep="")


print_output(d, i, n2, p, m, l, s, p1, a)
