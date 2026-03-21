---
title: "Lab 1: Passing Pollinators"
toc: true
---

This page is where you can iterate. Follow the lab instructions in the [readme.md](./README).

```js
const pollinators = await FileAttachment("data/pollinator_activity_data.csv").csv({typed: true})
```

### Q1 (Body Mass Exploration)

This first chart explores the distribution of body mass (in grams). I chose a [Stacked Histogram](https://observablehq.com/@observablehq/plot-vertical-histogram) to show body weights for each species. These measurements are well grouped within one species, but there is also good separation between species *(except for 1 tiny Carpenter Bee measurement)*.  

```js
Plot.plot({
    title: "Body Mass Distribution",
    subtitle: "Fill by Species",
    marginLeft: 120,
    width: 750,
    height: 400,
    y: { grid: true, domain: [0,30] },
    x: { label: "Body Mass (g)", domain: [0,.556] },
    color: { legend: true },
    marks: [
        Plot.rectY(
            pollinators,
            Plot.stackY(
                Plot.binX(
                    { y: "count" },
                    {
                        x: "avg_body_mass_g",
                        fill: "pollinator_species",
                        thresholds: 100,
                        tip: true
                    }
                )
            )
        )
    ]
})
```

### Q1: Wingspan Exploration

I once again chose to use a histogram here. This one is more noisy, as there is a lot of overlab between Bumblebee's and Carpenter Bee's wingspans. To show this overlap, I used the [Overlapping Histogram](https://observablehq.com/@observablehq/plot-overlapping-histogram) style plot.

```js
Plot.plot({
    title: "Wingspan Distribution",
    subtitle: "Fill by Species",
    marginLeft: 120,
    width: 750,
    height: 400,
    y: { grid: true, domain: [0,24] },
    x: { label: "Wingspan (mm)", domain: [10, 55] },
    color: { legend: true },
    marks: [
        Plot.rectY(
            pollinators,
            Plot.binX(
                { y2: "count" },
                {
                    x: "avg_wing_span_mm",
                    fill: "pollinator_species",
                    mixBlendMode: "multiply",
                    thresholds: 100,
                    tip: true
                }
            )
        )
    ]
})
```


### Q2

For this question I experimented with some of the more unique chart types that are shown on the [Plot Gallery](https://observablehq.com/@observablehq/plot-gallery)

```js
Plot.plot({
    title: "Average Pollinator Activity by Weather Condition",
    width: 750,
    height: 400,
    y: { grid: true, label: "Avg Visit Count", domain: [0, 7] },
    x: { label: "Weather Condition" },
    color: { legend: true },
    marks: [
        Plot.frame(),
        Plot.barY(
            pollinators,
            Plot.groupX(
                { y: "mean" },
                {
                    x: "weather_condition",
                    y: "visit_count",
                    fill: "weather_condition",
                    tip: true
                }
            )
        )
    ]
})
```

### Q3 Flower Nectar Production

Once again, I chose an overlapping histogram, as I felt like it offered the best visual representation of the nectar production ranges of each species.

```js
Plot.plot({
    title: "Nectar Production (μL)",
    subtitle: "Fill by Flower Species",
    marginLeft: 120,
    width: 750,
    height: 400,
    y: { grid: true },
    x: { label: "Nectar Production " },
    color: { legend: true },
    marks: [
        Plot.rectY(
            pollinators,
            Plot.binX(
                { y2: "count" },
                {
                    x: "nectar_production",
                    fill: "flower_species",
                    mixBlendMode: "multiply",
                    thresholds: 40,
                    tip: true
                }
            )
        )
    ]
})
```
