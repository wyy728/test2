
import pandas as pd
data=pd.read_csv(r"huanhuan/bilibili.csv")
up_count = data.groupby("author").count()
up_count = up_count["分区"].reset_index()
up_count.columns = ["author","times"]
new_count = pd.merge(up_count, data, on="author")
new_count["date"]=pd.to_datetime(new_count["date"])
result = new_count[new_count["times"]>=5]

#Calculate IFL
#Calculate I
groupbyAuthor = result.groupby("author").sum()
danmu = groupbyAuthor["danmu"]
reply = groupbyAuthor["reply"]
view = groupbyAuthor["view"]
count = result.groupby("author")["times"].count()
I = ((danmu+reply)/view/count*100)

#Calculate F
latest = result.groupby("author")["date"].max()
earliest = result.groupby("author")["date"].min()
F = ((latest-earliest).dt.days/count)

#Calculate L
likes = groupbyAuthor["likes"]
coins = groupbyAuthor["coins"]
favorite = groupbyAuthor["favorite"]
L = ((likes+coins+favorite)/view*100)

#Joint 2 by 2
IFL = pd.concat([I,F,L], axis=1)
IFL.columns = ["I","F","L"]

#分箱
IFL["I_score"] = pd.qcut(IFL["I"],q=5,labels=[1,2,3,4,5])
IFL["F_score"] = pd.qcut(IFL["F"],q=5,labels=[5,4,3,2,1])
IFL["L_score"] = pd.qcut(IFL["L"],q=5,labels=[1,2,3,4,5])


def iflTrans(x):
    if x > 3:
        return 1
    else:
        return 0


IFL["I_score"] = IFL["I_score"].apply(iflTrans)
IFL["F_score"] = IFL["F_score"].apply(iflTrans)
IFL["L_score"] = IFL["L_score"].apply(iflTrans)

IFL["mark"] = IFL["I_score"].astype(str) + IFL["F_score"].astype(str) + IFL["L_score"].astype(str)


def iflType(x):
    if x == "111":
        return "高质量UP主"
    elif x == "101":
        return "高质量拖更UP主"
    elif x == "011":
        return "高质量内容高深UP主"
    elif x == "001":
        return "高质量内容高深拖更UP主"
    elif x == "110":
        return "接地气活跃UP主"
    elif x == "100":
        return "接地气UP主"
    elif x == "010":
        return "活跃UP主"
    else:
        return "还在成长的UP主"


IFL["up_type"] = IFL["mark"].apply(iflType)

up_type = IFL["up_type"].groupby(IFL["up_type"]).count()
up_type = up_type / up_type.sum()

#可视化
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "Arial Unicode MS"
plt.bar(up_type.index, up_type.values)
plt.xticks(rotation=45)
plt.show()


