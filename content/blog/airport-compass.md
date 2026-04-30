+++
title = "The airport compass"
date = 2024-02-25
draft = false
tags = ["Python", "Aviation", "Visualization"]
+++

A few years ago, I got inspired by a very interesting figure published on a paper by [Geoff Boeing](https://github.com/gboeing) called ["Urban spatial order: street network orientation, configuration, and entropy"](https://appliednetsci.springeropen.com/articles/10.1007/s41109-019-0189-1).

This figure represents the distribution of the orientation of every street of major cities. I like how it gives a quick representation of each city's layout and how evident the various levels of entropy are.

Shortly after seeing this chart, I immediately thought of replicating this view for airports' traffic worldwide.

## Sources and code

For this project I used two major open-source datasets:

- The airlines routes data comes from [@jpatokal](https://github.com/jpatokal/openflights)'s OpenFlights repository
- The airports data is from [@davidmegginson](https://github.com/davidmegginson/ourairports-data/)'s OurAirports repository

I made the source-code available on my GitHub [here](https://github.com/lucianosrp/airport-compass).

## Outcomes

I first generated the top 15 airports by number of destinations. Each chart (or compass) displays the distribution of outbound flights and aligns those for each initial bearing. The longer the yellow bar, the more frequently that bearing occurs. For example, if an airport has most of the departures pointing West (or 270°), you would see the longest bar pointing left.

![15 Airports view](/assets/img/airport-compass/Where-is-it-going-15.png)

Some airports like New York JFK and London Heathrow (LHR) represent an important hub for transatlantic flights. In these charts, we can see how LHR has a long bar towards the West (towards North America) and JFK has one towards the East (Europe).

![LHR](/assets/img/airport-compass/LHR-dark.png)

Other airports' compasses, instead, are majorly driven by the geographical constrains of their location. Tokyo's Narita Intl. Airport is a very good example to illustrate this case. It has virtually no routes pointing eastwards! This is because Japan has the Pacific Ocean to its east side and most of the routes connecting Japan to North America take an initial bearing pointing North! (Since this would be the shortest great circle path)

![NRT](/assets/img/airport-compass/NRT-dark.png)

## How-to

As I said earlier in this post, I used two freely available datasets and published the source code to replicate these charts. Everything is made entirely using Python:

- To merge and transform the data I used [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/) is used for the visualization

### Data

First, I set a constant to represent the number of airports I want to have in the final view. In this example, we are going to start with 30. The csv data can be conveniently loaded directly from GitHub using the `read_csv` method.

```python
import pandas as pd

TOP_AIRPORTS = 30

# Getting airlines' routes data:
routes = pd.read_csv(
    "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat",
    usecols=[0, 2, 4],
    names=["airline", "origin", "destination"],
)
```

This first dataset doesn't come with headers, hence why we need to use the `names` argument to specify the column names. Also, we are just interested in knowing the origin and destination airport of each route (Column 2 and 4), I also added the airline IATA code (Column 0) because I was curious, but not needed for this project.

We are also not interested in displaying all airports on this dataset. To do so, we can get the Top airports by grouping the data, ordering it and accessing only until the `TOP_AIRPORTS` constant number:

```python
# Selecting only top airports
top_airports = (
    routes.groupby("origin")
    .destination.count()
    .sort_values(ascending=False)
    .index[:TOP_AIRPORTS]
)

routes = routes.loc[routes.origin.isin(top_airports)]
```

Now, we are just having data about each airlines' routes. But in order to plot the data into small compasses, we will need to calculate the initial bearing of each airport pair. And in order to do so, we also need the coordinates of each airport:

```python
# Getting airports data:
airports = pd.read_csv(
    "https://raw.githubusercontent.com/davidmegginson/ourairports-data/main/airports.csv",
    usecols=["ident", "iata_code", "latitude_deg", "longitude_deg"],
)
```

When looping for `origin` and `destination` we also make sure that the columns in the airport dataset are suffixed with "_origin" and "_destination" respectively. We can now calculate the bearing (angle) for each pair:

```python
import numpy as np

# Getting initial bearing for each route:
df["angle"] = np.degrees(
    np.arctan2(
        df.latitude_deg_destination - df.latitude_deg_origin,
        df.longitude_deg_destination - df.longitude_deg_origin,
    )
)
```

Numpy can do all the math for us with a resulting column "angle" which contains all angles for each pair.

Since we would want to have a sense of the "distribution" of routes for each angle, we can make a resulting dataframe by doing a final aggregation:

```python
# Aggregating final data:
res = df.groupby(["origin", "angle"]).destination.count()
```

### Visualization

We can dynamically create the layout of our "poster" by dividing the total number of airports by the number of columns we want to have:

```python
ncols = 5
nrows = len(top_airports) // ncols
```

Now we can set up the figure and axes of our plot:

```python
fig, axes = plt.subplots(
    nrows=nrows,
    ncols=ncols,
    subplot_kw=dict(projection="polar"),
    figsize=(ncols * 1.9, nrows * 2.6),
)
```

We can fill each axis with a for-loop:

```python
for ax, airport in zip(axes.flatten(), top_airports):
    airport_data = res.loc[airport]
    ax.bar(
        np.radians(airport_data.index),
        airport_data.values,
        width=0.3,
        color="C2",
        alpha=0.5,
    )

    ax.set_title(f"{airport}\n", fontdict=dict(fontweight="bold"))
    ax.set_yticks([])
    ax.set_rlabel_position(90)
    ax.set_xticklabels(["E", "", "N", "", "W", "", "S", ""], fontdict=dict(fontsize=10))
```

Here, `axes.flatten()` conveniently "flattens" out the nested array that `axes` is. We don't need the ticks for the Y axis so we turn them off using `ax.set_yticks([])`.

The `set_xtickslabels` currently raise a `UserWarning` which we can safely ignore.

```python
fig.suptitle("Where is the traffic going?", fontsize=25, fontweight="bold")
fig.text(0.05, 0.005, "Made by Luciano Scarpulla")
fig.tight_layout(pad=3)
fig.savefig(f"Where is it going {TOP_AIRPORTS}.png", dpi=300)
```

## What's next?

I first developed this years ago and re-adapted my old code for this post. There are some changes and improvements that can be made:

- The data is grouped by each unique bearing. This can be fixed by simply rounding the angles, or distributing the angles into different buckets (e.g 130-140 degrees, 140-150, etc.)
- The image is a static outlook at airlines' routes of 2014. A seasonal outlook could be made so that you could notice the differences in the "orientation" in certain airports.

## Key Insights

This visualization reveals interesting patterns about global air travel:

1. **Transatlantic hubs** — LHR and JFK stand out with strong opposing bearings. LHR points West (towards North America), JFK points East (towards Europe). This reflects the dominant transatlantic market.

2. **Geographical constraints** — Tokyo Narita shows almost no eastward routes because the Pacific Ocean makes it inefficient. Routes to North America actually head North — the shortest great circle path.

3. **Regional vs international** — Some airports (like in the Middle East) show a balanced spread, reflecting their role as connecting hubs between multiple continents.

These patterns emerge naturally from the data and tell a story about how geography and market demand shape air traffic.

![30 Airports view](/assets/img/airport-compass/Where-is-it-going-30.png)
