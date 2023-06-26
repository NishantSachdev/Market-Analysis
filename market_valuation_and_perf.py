import pandas as pd

avg = pd.read_csv('I:\\NISHANT\\Market\\market data\\nifty100.csv')
returns = pd.read_csv('I:\\NISHANT\\Market\\market data\\data.csv')

nifty200day_avg=str(returns["Close"].tail(200).mean())+"000"
nifty150day_avg=str(returns["Close"].tail(150).mean())+"000"
nifty90day_avg=str(returns["Close"].tail(90).mean())+"000"
nifty60day_avg=str(returns["Close"].tail(60).mean())+"000"
nifty30day_avg=str(returns["Close"].tail(30).mean())+"000"
niftylatest=(returns["Close"].tail(1))

print("\n")
print("NIFTY 100 DATA : ")
print("200 day avg" + " " + ":" + " " + nifty200day_avg[0:8])
print("150 day avg" + " " + ":" + " " + nifty150day_avg[0:8])
print("90 day avg" + "  " + ":" + " " + nifty90day_avg[0:8])
print("60 day avg" + "  " + ":" + " " + nifty60day_avg[0:8])
print("30 day avg" + "  " + ":" + " " + nifty30day_avg[0:8])
print("latest data : " + str(niftylatest.tolist()[0]))
print("\n")
val1=(niftylatest.tolist()[0]-float(nifty200day_avg))/float(nifty200day_avg)*100
val2=(niftylatest.tolist()[0]-float(nifty150day_avg))/float(nifty150day_avg)*100
val3=(niftylatest.tolist()[0]-float(nifty90day_avg))/float(nifty90day_avg)*100
val4=(niftylatest.tolist()[0]-float(nifty60day_avg))/float(nifty60day_avg)*100
val5=(niftylatest.tolist()[0]-float(nifty30day_avg))/float(nifty30day_avg)*100
print("PERCENTAGE INCREASE OF NIFTY 100 VALUE :")
print("from 200 day average" + " " + ":" + " " + str(val1)[0:5] + " " + "%")
print("from 150 day average" + " " + ":" + " " + str(val2)[0:5] + " " + "%")
print("from 90 day average" + "  " + ":" + " " + str(val3)[0:5] + " " + "%")
print("from 60 day average" + "  " + ":" + " " + str(val4)[0:5] + " " + "%")
print("from 30 day average" + "  " + ":" + " " + str(val5)[0:5] + " " + "%")
print("\n")
print("---------------------------------------------------------------")

day200avg = avg[["P/E","P/B"]].tail(200).mean()
day90avg = avg[["P/E","P/B"]].tail(90).mean()
day30avg = avg[["P/E","P/B"]].tail(30).mean()
latest = avg[["P/E","P/B"]].tail(1)
var1=day200avg.tolist()
var2=day90avg.tolist()
var3=day30avg.tolist()
var4=latest.values.tolist()

print("\n")
print("200 DAY AVERAGE")
print("P/E"+" "+":"+" "+str(var1[0])[0:8]+"\n"+"P/B"+" "+":"+" "+str(var1[1])[0:8])
print("\n")
print("90 DAY AVERAGE")
print("P/E"+" "+":"+" "+str(var2[0])[0:8]+"\n"+"P/B"+" "+":"+" "+str(var2[1])[0:8])
print("\n")
print("30 DAY AVERAGE")
print("P/E"+" "+":"+" "+str(var3[0])[0:8]+"\n"+"P/B"+" "+":"+" "+str(var3[1])[0:8])
print("\n")
print("LATEST DATA")
print("P/E"+" "+":"+" "+str(var4[0][0])+"\n"+"P/B"+" "+":"+" "+str(var4[0][1]))
print("\n")

print("---------------------------------------------------------------")
print("\n")
par1 = day200avg["P/E"]-latest["P/E"]
par1 = par1.tolist()
par1 = par1[0]
par1 = par1/day200avg["P/E"]*100
par1 = str(par1) + "00000"
par1 = par1[0:6] + " " + "%"

par2 = day90avg["P/E"]-latest["P/E"]
par2 = par2.tolist()
par2 = par2[0]
par2 = par2/day90avg["P/E"]*100
par2 = str(par2) + "00000"
par2 = par2[0:6] + " " + "%"

par3 = day30avg["P/E"]-latest["P/E"]
par3 = par3.tolist()
par3 = par3[0]
par3 = par3/day30avg["P/E"]*100
par3 = str(par3) + "00000"
par3 = par3[0:6] + " " + "%"

print("Percentage change of P/E :")
print("from 200 day average" + " " + ":" + " " + par1)
print("from 90 day average" + " " + ":" + " " + par2)
print("from 30 day average" + " " + ":" + " " + par3)
print("\n")

print("---------------------------------------------------------------")
print("\n")
par4 = day200avg["P/B"]-latest["P/B"]
par4 = par4.tolist()
par4 = par4[0]
par4 = par4/day200avg["P/B"]*100
par4 = str(par4) + "00000"
par4 = par4[0:6] + " " + "%"

par5 = day90avg["P/B"]-latest["P/B"]
par5 = par5.tolist()
par5 = par5[0]
par5 = par5/day90avg["P/B"]*100
par5 = str(par5) + "00000"
par5 = par5[0:6] + " " + "%"


par6 = day30avg["P/B"]-latest["P/B"]
par6 = par6.tolist()
par6 = par6[0]
par6 = par6/day30avg["P/B"]*100
par6 = str(par6) + "00000"
par6 = par6[0:6] + " " + "%"

print("Percentage change of P/B :")
print("from 200 day average" + " " + ":" + " " + par4)
print("from 90 day average" + " " + ":" + " " + par5)
print("from 30 day average" + " " + ":" + " " + par6)
print("\n")