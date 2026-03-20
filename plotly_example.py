import math
import plotly
import plotly.graph_objs as go
 
## generate some data
x = [x/10 for x in range(100)]
y = [math.sin(c) for c in x]
 
## check that the values are as expected:
print(f'x={x}')
print(f'y={y}')
 
## create a figure and plot it
fig = go.Scatter(x=x, y=y)
fig = go.Bar(x=x, y=y)
plotly.offline.plot({"data":[fig]})