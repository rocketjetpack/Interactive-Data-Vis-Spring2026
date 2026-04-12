---
title: "Lab 2: Subway Staffing"
toc: true
---

<!-- Import Data -->
```js
const incidents = await FileAttachment("./data/incidents.csv").csv({ typed: true })
const local_events = await FileAttachment("./data/local_events.csv").csv({ typed: true })
const upcoming_events = await FileAttachment("./data/upcoming_events.csv").csv({ typed: true })
const ridership = await FileAttachment("./data/ridership.csv").csv({ typed: true })
```

<!-- Include current staffing counts from the prompt -->
```js
const currentStaffing = {
  "Times Sq-42 St": 19,
  "Grand Central-42 St": 18,
  "34 St-Penn Station": 15,
  "14 St-Union Sq": 4,
  "Fulton St": 17,
  "42 St-Port Authority": 14,
  "Herald Sq-34 St": 15,
  "Canal St": 4,
  "59 St-Columbus Circle": 6,
  "125 St": 7,
  "96 St": 19,
  "86 St": 19,
  "72 St": 10,
  "66 St-Lincoln Center": 15,
  "50 St": 20,
  "28 St": 13,
  "23 St": 8,
  "Christopher St": 15,
  "Houston St": 18,
  "Spring St": 12,
  "Chambers St": 18,
  "Wall St": 9,
  "Bowling Green": 6,
  "West 4 St-Wash Sq": 4,
  "Astor Pl": 7
}
```

<!-- Styling stuff -->
<style>
  .insight-box {
    background: #f8f8f6;
    border-left: 4px solid #0e7741;
    padding: 1rem 1.4rem;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #222;
    max-width: 860px;
  }

  .insight-box strong {
    color: #0e7741;
  }

  .input-wrap {
    margin: 5px 0px;
  }

  .input-wrap label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #0e7741;
    display: block;
    margin-bottom: 0.4rem;
  }

  .input-wrap select {
    appearance: none;
    background: #f8f8f6;
    border: 1.5px solid #0e7741;
    border-radius: 0;
    padding: 5px;
    font-size: 12pt;
    color: #222;
    cursor: pointer;
    background-repeat: no-repeat;
    background-position: right 0.8rem center;
  }
  
  .input-wrap select:focus {
    outline: none;
    border-color: #0a5530;
  }

  .chart-wrap {
    border: 1.5px solid #0e7741;
    padding: 1.4rem 1.6rem;
    margin: 1.2rem 0;
    max-width: 930px;
    background: #fafaf8;
  }

  .chart-wrap .chart-instruction {
    font-size: 0.78rem;
    color: #666;
    margin-bottom: 1rem;
    font-style: italic;
  }

  .explainer-area {
    font-size: 10pt;
    color: #4d4d4d;
    font-style: italic;
  }
</style>

# Lab 2: Subway Staffing
#### Kali McLennan

This lab focuses on working with multiple data sets in Observable Plot using transforms.

## Section 1: Ridership and local events

<div class="insight-box">
  The following plot shows daily entrances recorded at each station in low-opacity grey.
  Use the dropdown to focus on a specific station — its ridership is highlighted in green,
  with vertical lines marking <strong>local event dates</strong>. The
  <strong style="color:red;">dashed red line</strong> marks the July 15th fare increase
  from $2.75 to $3.00, after which a general downward trend is visible across all stations.
</div>

```js
const fareDate = new Date("2025-07-15");
const stations = [...new Set(ridership.map(d => d.station))].sort();
```



<div class="chart-wrap">
  <h2>Station Entrances by Date</h2>

  Exploring the impacts of local events on station activity.
  <p class="chart-instruction">Select a station below to highlight its ridership trend. Event dates are marked with dashed vertical lines.</p>
  <div class="input-wrap">

```js
const stationPick = view(Inputs.select(stations, { label: "Station", value: "Times Sq-42 St" }));
```

  </div>

```js
const stationData = ridership.filter(d => d.station === stationPick);
const eventDates = new Set(local_events.filter(e => e.nearby_station === stationPick).map(e => e.date.getTime()));
const stationEventDots = stationData.filter(d => eventDates.has(d.date.getTime()))
  .map( d => ({
    ...d,
    eventName: local_events.find(e => e.nearby_station === stationPick && e.date.getTime() === d.date.getTime())?.event_name
  }));
```

```js
Plot.plot({
  width: 900,
  height: 460,
  x: { type: "time", tickFormat: "%b %-d", ticks: 10, axis: "top"},
  y: { domain: [0, 35000] },
  marginBottom: 120,
  marks: [
    Plot.lineY(ridership, {
      x: "date",
      y: "entrances",
      z: "station",
      stroke: "#333",
      opacity: 0.1,
      strokeWidth: 1,
    }),
    Plot.lineY(stationData, {
      x: "date",
      y: "entrances",
      stroke: "#0e7741",
      strokeWidth: 2.5,
      opacity: 0.75,
      tip: true,
      title: d => `Date: ${d.date.toLocaleDateString("en-US", {month:"short", day:"numeric"})}\nEntrances: ${d.entrances.toLocaleString()}`,
    }),
    Plot.ruleX(stationEventDots, {
      x: "date",
      stroke: "#000",
      strokeWidth: 1,
      strokeDasharray: "4,3",
    }),
    Plot.text(stationEventDots, {
      x: "date",
      y: 0,
      text: d => d.eventName,
      //fill: "#f5e642",
      fontSize: 10.5,
      textAnchor: "end",
      rotate: -60,
      dx: -6,
      dy: 5,
    }),
    Plot.ruleX([fareDate], {
      stroke: "red",
      strokeWidth: 1.5,
      strokeDasharray: "6,4",
    }),
    Plot.text([fareDate], {
      x: d => d,
      y: ridership[0].entrances,
      text: ["July 15\nFare: $2.75 → $3.00"],
      fill: "red",
      fontSize: 10,
      textAnchor: "start",
      dx: 6,
      dy: -130
    }),
  ]
})
```

<div class="explainer-area">
I must admit, I spent far too long playing with the style of this. I wanted a self-contained plot element that tied the select box in with the plot itself. I also spent an absurd amount of time playing with the bottom margin and anble of the event text to hopefully prevent event text from being cut off. Some of these event names are just very long which leads to a lot of dead space that Im not sure what to do with. I generally like the appearance, and it made me experiment with CSS and HTML with Observable elements inside.

Also, thanks to Claude for generally useful CSS. I love the modern ability to describe generally what I want, get the CSS, then iterate from there.
</div>

</div>

<div class="insight-box">
  Local events have a <strong>highly variable</strong> impact on station entrances.
  High-attendance events such as sports games, fairs, parades and concerts produce dramatic ridership spikes
  at nearby stations, while low-attendance events like farmers markets result in only minor
  increases. The fare hike effect is most visible at high-volume stations where the post-July
  15th average is noticeably lower.
</div>

## Section 2: Incident Response Times

<div class="insight-box">
  The second part of this lab explores how the stations compare in the time it takes to respond
  to an <strong style="color:red;">incident</strong>, and specifically, which stations are the <strong>best</strong>
  and <strong style="color:red;">worst</strong> in terms of response time to reported incidents.
</div>

<div class="chart-wrap">
  <h2>Station Incident Responses</h2>

  Exploring how stations respond to different types of incidents.

  <p class="chart-instruction">Select a station below to highlight its incident response information. The width of the bar represents the range from fastest to slowest response for the station, while the dots represent the average response time to <strong style="color: green">low</strong>, <strong style="color: gold">medium</strong>, and <strong style="color: red">high</strong> severity incidents.</p>

  <div class="input-wrap">

```js
const stationPick_Incident = view(Inputs.select(
  [... new Set(incidents.map( d => d.station ))].sort(),
  { label: "Station" }
))
```

```js
const filtered = incidents.filter( d => d.station === stationPick_Incident );
const avgResponseMins = d3.mean(filtered, d=> d.response_time_minutes);
const totalIncidents = filtered.length;
const totalRidership = d3.mean(
  ridership.filter(d => d.station === stationPick_Incident),
  d => d.entrances + d.exits
);
const stationAvg = incidents.map( d => ({
  ...d,
  selected: d.station === stationPick_Incident
}));
```

<!-- Trying something fancy here. A tip on https://observablehq.com/plot/marks/dot says:
To reduce code duplication, pull shared options out into an object and then merge them into
each marks options using the spread operator (...). -->
```js
// Construct a spreadable object that represents response time by station
const xy = {
  x: "response_time_minutes",
  y: "station",
  sort: { y: "x" }
};
```

```js
Plot.plot({
  marginLeft: 160,
  x: { label: "Avg response time (min)", grid: true },
  color: {
    domain: ["low", "medium", "high"],
    range: ["steelblue", "orange", "crimson"],
  },
  marks: [
    Plot.ruleX([0]),
    Plot.ruleX([d3.mean(incidents, d => d.response_time_minutes)], { stroke: "red", strokeOpacity: 0.5 }),
    Plot.text([{x: d3.mean(incidents, d => d.response_time_minutes)}], { 
      x: "x",
      text: ["All Incident Average"],
      dy: -6,
      textAnchor: "middle",
      rotate: 90,
      dx: 10,
      dy: -200,
      fontSize: 11,
      fill: "red",
      fillOpacity: 0.5
    }),
    Plot.ruleY(stationAvg, Plot.groupY({ x1: "min", x2: "max" }, { ...xy, stroke: "#ddd" })),
    Plot.dot(stationAvg, Plot.groupY({ x: "mean" }, { ...xy, fill: "severity", fillOpacity: 0.2, r: 4 })),
    Plot.dot(filtered, Plot.groupY({ x: "mean" }, { ...xy, fill: "severity", r: 5, tip: true }))
  ]
})
```

  </div>

  <div class="explainer-area">
    Originally, I wanted to try to combine the incident data and/or the staffing data to see if there was any likely
    connections between ridership or staffing and response time. It seems expected that staffing level would have an
    impact on responsiveness to incidents, but I could not come up with a clean way to visualize this.
  </div>
</div>

## Section 2: Staffing Need Prediction

<div class="insight-box">
  The final section of this lab asks which three stations are likely to need the most staffing help summer based on
  the 2026 event calendar.
</div>