import numpy as np
from sympy import *
from sympy.abc import x, y
"------------------------------------------Initialization--------------------------------------------------------------"
G = 4750 * np.e ** 7 / (350 * 24 * 3600)  # 油品的质量流量
e = 5 * 10 ** (-5)
g = 9.8

'待确定参数'
T = 40  # 当前温度
ρ20 = 0
Q = 0
d = 1
ν = 0.001045287 * T ** 4 - 0.213254821 * T ** 3 + 16.320975514 * T ** 2 - 16.320975514 * T + 7901.112727272  # 数据拟合
L = 1
A = 1
l = 1
m = 1
Hsz = 1
Hc = 1
i = 1
hm = 1

ε_t = 1.825 - 0.001315 * ρ20
ρ = ρ20 - ε_t * (T-2)
Q = G / ρ

Re = 4 * Q / (np.pi * d * ν)
ε = 2 * e / d
Re1 = 59.5 / (ε ** (8/7))

Re2 = (655 - 765 * np.log(ε))/ε

if Re <= 2000:
    λ = 64 / Re
if 2000 < Re <= Re1:
    λ = 0.3164 * Re ** (-0.25)
if Re1 < Re <= Re2:
    λ = 0.11 * (e/d + 68/Re) ** 0.25
if Re > Re2:
    λ = 1 / (1.74 - 2 * np.log(ε)) ** 2

'沿程摩阻损失'
υ = 4 * Q / (np.pi * d ** 2)
h_l = λ * L / d * υ ** 2 / (2 * g)

'综合摩阻损失'
beta = 8 * A / (4 ** m * np.pi ** (2-m) * g)
h_l = beta * l * Q ** (2-m) * υ ** m / d ** (5 - m)

H = h_l + Hsz

N = (i * L + Hsz) / Hc - hm

"------------------------------------------compute_temperature---------------------------------------------------------"
'待确定参数'
# D = 1  # 管道外径，m

"------------------------------原油及成品油的物性参数------------------------------"
'待确定参数'
d4_20 = 1  # 原油在20°C时的相对密度
d4_15 = 1  # 原油在15°C时的相对密度

'计算相对密度'
ξ = 1.825 * 10 ** (-3) - 1.315 * 10 ** (-3) * d4_20  # 温度系数
d4 = d4_20 - ξ * (T - 20)

'计算比热容'
# T_sl = 1  # 稀蜡点温度
# T_cmax = 2  # 最大比热容温度
# A_1 = 1  # 常数，随原油而不同，KJ/(kg*°C)
# n_1 = 1  # 常数，随原油而不同，１/°C
# A_2 = 1  # 常数，随原油而不同，KJ/(kg*°C)
# n_2 = 1  # 常数，随原油而不同，１/°C

'书上经验公式'
# if T > T_sl:
#     c_y = (1.687 + 3.39 * 10 ** (-3) * T) / np.sqrt(d4_15)
# if T_sl > T > T_cmax:
#     c_y = 4.186 - A_1 * np.exp(n_1 * T)  # 含蜡原油在稀蜡温度以下，高于Tcmax的比热容，KJ/(kg*°C)
# if T_cmax > T > 0:
#     c_y = 4.186 - A_2 * np.exp(-n_2 * T)  # 含蜡原油在低于Tcmax的比热容，KJ/(kg*°C)

'数据拟合'
c_y = 1934 + 5.866 * T

'导热系数'
# λ_y = 0.137 * (1 - 0.54 * 10 ** (-3) * T) / d4_15  # 油品在T°C的导热系数,W/(m*°C)
# λ_y = 0.14

'粘度'
# ν = 10 ** (10 ** (a + b * np.log10(T + 273))) - 0.8 * 10 ** (-6)  # 书上经验公式
# ν = 0.001045287 * T ** 4 - 0.213254821 * T ** 3 + 16.320975514 * T ** 2 - 16.320975514 * T + 7901.112727272  # 数据拟合

"------------------------------油流至管内壁的的放热系数α_1-----------------------------------------"
'待确定参数'
Pr_bi = 1
β_y = 1

D = 597.20 * 10 ** (-3)
α_1 = 1
# α_2 = 1
T0 = 40

h1 = 2  # 油对管道壁面的传热，待查
h2 = 3  # 管道对土地的传热，待查
λ_tiaohe = 0.269  # 调和平均之后的传热率
x1 = 0  # 油和管道内壁接触位置
x2 = 14.4  # 管道外壁于土壤接触位置
t_1 = 40  # 第三类问题，油的温度
t_2 = 20  # 第三类问题，土壤的温度

aa = solve([h1 * (x * x1 + y - t_1) + λ_tiaohe * x, h2 * (x * x2 + y - t_2) + λ_tiaohe * x], [x, y])
c1 = aa[x]
c2 = aa[y]
T_bi = c1 * 14.4 + c2

K0 = 0
Re_K0 = [[2.2, 1.9], [2.3, 3.2], [2.5, 4.0], [3.0, 6.8], [3.5, 9.5], [4.0, 11], [5.0, 16],
         [6.0, 19], [7.0, 24], [8.0, 27], [9.0, 30], [10, 33]]
k = Re // 100
k = k / 10

for i in range(12):
    if Re_K0[i][0] == k:
        K0 = (Re_K0[i+1][1] - Re_K0[i][1]) / (Re_K0[i+1][0] - Re_K0[i][0]) * (Re / 1000 - Re_K0[i][0])

Pr_y = ρ * c_y * ν / λ
Gr = d ** 3 * g * β_y * (T - T_bi) / ν ** 2
num = Pr_y * Gr

if Re < 2000 and num > 5 * 10 ** 2:
    α_1 = λ / D * 0.17 * Re ** 0.33 * Pr_y ** 0.43 * Gr ** 0.1 * (Pr_y / Pr_bi) ** 0.25
if Re > 10 ** 4 and Pr_y < 2500:
    α_1 = 0.021 * λ / D * Re ** 0.8 * Pr_y ** 0.44 * (Pr_y / Pr_bi) ** 0.25
if 2000 < Re < 10 ** 4:
    α_1 = λ / D * K0 * Pr_y ** 0.43 * (Pr_y / Pr_bi) ** 0.25

"------------------------------管外壁至土壤的放热系数α_2-----------------------------------------"
λ_t = 1.4  # 土壤导热系数,W/(m*°C)
h_t = 1.6  # 管中心埋深,m
D_ω = 610 * 10 ** (-3)  # 与土壤接触的管外直径,m

α_2 = 2 * λ_t / (D_ω * np.log(2 * h_t / D_ω + np.sqrt((2 * h_t / D_ω) ** 2 - 1)))  # 管外壁至土壤的放热系数,W/(m*°C)

"------------------------------热油管道的总传热系数----------------------------------------"
# α_1 = 1  # 油流至管内壁的放热系数,W/(m*°C)
# α_2 = 1  # 管外壁至土壤的放热系数,W/(m*°C)
λ_1 = 48  # 钢管的导热系数,W/(m*°C)
δ_1 = 6.4 * 10 ** (-3)  # 钢管壁的厚度,m
λ_2 = 0.15  # 绝热层的导热系数,W/(m*°C)
δ_2 = 8 * 10 ** (-3)  # 绝热层的厚度,m

K = 1 / (1 / α_1 + 1 / α_2 + δ_1 / λ_1 + δ_2 / λ_2)  # 管道总传热系数，W/(m2*°C)

"------------------------------轴向温降-----------------------------------------"
'待确定参数'
# D = 1  # 管道外径，m
# c = 1  # 输油平均温度下油品的比热容，J/(kg*°C)
TR = 40  # 管道起点油温，°C
T0 = 20  # 周围介质温度，°C
# d4_20 = 1  # 原油在20°C时的相对密度
# d4_15 = 1  # 原油在15°C时的相对密度
# T = 40  # 当前温度

'距离起始点l产生的温降'
'a,b参数'
a = K * np.pi * D / (G * c_y)
b = g * i / c_y / a

TL = (TR - T0 - b) / np.exp(a * L) + T0 + b

"------------------------------确定加热站数及热负荷------------------------------"
Tz = 1  # 终点温度,°C

l_R = G * c_y / K * np.pi * D * np.log((TR - T0 - b) / (Tz - T0 - b))

nR = L / l_R  # 初步计算的加热站距离,m
