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

<!-- CSS Styling stuff -->
<style>
  .notes-box {
    background: #f8f8f6;
    border-left: 4px solid #0e7741;
    padding: 5px 5px;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    line-height: 1.75;
    color: #222;
    max-width: 860px;
  }

  .notes-box strong {
    color: #0e7741;
  }

  .answer-box {
    background: #f8f8f6;
    padding: 5px 5px;
    margin: 5px 0;
    font-size: 12;
    line-height: 1.5;
    color: #222;
    max-width: 900px;
  }

  .input-wrap {
    margin: 5px 0px;
  }

  .input-wrap label {
    font-size: 14px;
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

<div class="notes-box">
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
  .map(d => ({
    ...d,
    eventName: local_events.find(e => e.nearby_station === stationPick && e.date.getTime() === d.date.getTime())?.event_name
  }));
```

```js
Plot.plot({
  width: 900,
  height: 460,
  x: { type: "time", tickFormat: "%b %-d", ticks: 10, axis: "top" },
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
      title: d => `Date: ${d.date.toLocaleDateString("en-US", { month: "short", day: "numeric" })}\nEntrances: ${d.entrances.toLocaleString()}`,
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
I must admit, I spent far too long playing with the style of this. I wanted a self-contained plot element that tied the select box in with the plot itself. I also spent an absurd amount of time playing with the bottom margin and angle of the event text to hopefully prevent event text from being cut off. Some of these event names are just very long which leads to a lot of dead space that I'm not sure what to do with. I generally like the appearance, and it made me experiment with CSS and HTML with Observable elements inside.

Also, thanks to Claude for generally useful CSS. I love the modern ability to describe generally what I want, get the CSS, then iterate from there.
</div>

</div>

<div class="answer-box">
  Local events have a <strong>highly variable</strong> impact on station entrances.
  High-attendance events such as sports games, fairs, parades and concerts produce dramatic ridership spikes
  at nearby stations, while low-attendance events like farmers markets result in only minor
  increases. The fare hike effect is most visible at high-volume stations where the post-July
  15th average is noticeably lower.
</div>

<hr />

## Section 2: Incident Response Times

<div class="notes-box">
  The second part of this lab explores how the stations compare in the time it takes to respond
  to an <strong style="color:red;">incident</strong>, and specifically, which stations are the <strong>best</strong>
  and <strong style="color:red;">worst</strong> in terms of response time to reported incidents.
</div>

<div class="chart-wrap">
  <h2>Station Incident Responses</h2>

  Exploring how stations respond to different types of incidents.

  <p class="chart-instruction">Select a station below to highlight its incident response information. The width of the bar represents the range from fastest to slowest response for the station, while the dots represent the average response time to <strong style="color: green">low</strong>, <strong style="color: orange">medium</strong>, and <strong style="color: red">high</strong> severity incidents.</p>

  <div class="input-wrap">

```js
const stationPick_Incident = view(Inputs.select(
  [...new Set(incidents.map(d => d.station))].sort(),
  { label: "Station" }
))
```

```js
const filtered = incidents.filter(d => d.station === stationPick_Incident);
const avgResponseMins = d3.mean(filtered, d => d.response_time_minutes);
const totalIncidents = filtered.length;
const totalRidership = d3.mean(
  ridership.filter(d => d.station === stationPick_Incident),
  d => d.entrances + d.exits
);
const stationAvg = incidents.map(d => ({
  ...d,
  selected: d.station === stationPick_Incident
}));
```

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
    range: ["green", "orange", "crimson"],
  },
  marks: [
    Plot.ruleX([0]),
    Plot.ruleX([d3.mean(incidents, d => d.response_time_minutes)], { stroke: "red", strokeOpacity: 0.5 }),
    Plot.text([{ x: d3.mean(incidents, d => d.response_time_minutes) }], {
      x: "x",
      text: ["All Incident Average"],
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

  <div class="answer-box">
  
  </div>
</div>

<hr />

## Section 3: Staffing Need Prediction

<div class="notes-box">
  The starting point for predicting event-related staffing needs is to identify how much events in 2025 contributed to
  increased ridership activity at nearby stations. For this, a ratio is calculated representing how much extra traffic
  each station experienced as a result of 2025 events based on the <strong style="color: red">estimated_attendance</strong> value.
  The same calculation is applied to the <strong style="color: red">expected_attendance</strong> numbers for 2026. This lets us compare
  the expected surge in 2026 against the known surge in 2025.
</div>

```js
// Average daily entrances + exits per station across all of summer 2025
const avgDailyRidership = d3.rollup(
  ridership,
  v => d3.mean(v, d => d.entrances + d.exits),
  d => d.station
)

// Surge ratio: how much does each event's attendance represent relative to a normal day?
const eventSurges = local_events.map(d => ({
  ...d,
  surgeRatio: d.estimated_attendance / (avgDailyRidership.get(d.nearby_station) ?? 1)
}))

const upcomingSurges = upcoming_events.map(d => ({
  ...d,
  surgeRatio: d.expected_attendance / (avgDailyRidership.get(d.nearby_station) ?? 1)
}))
```

```js
// Build a summary of mean and max surge ratio per station per year
function surgeSummaryFrom(data, nearbyStation, year) {
  return Array.from(
    d3.rollup(
      data,
      v => ({ mean: d3.mean(v, d => d.surgeRatio), max: d3.max(v, d => d.surgeRatio) }),
      d => d[nearbyStation]
    ),
    ([station, d]) => ({ station, mean: d.mean, max: d.max, year, staff: currentStaffing[station] })
  )
}

const surgeSummaryAll = [
  ...surgeSummaryFrom(eventSurges, "nearby_station", "2025"),
  ...surgeSummaryFrom(upcomingSurges, "nearby_station", "2026")
]

// Pivot to one row per station with both years' max surge, drop stations missing either year
const surgeLinks = Array.from(
  d3.rollup(surgeSummaryAll, v => Object.fromEntries(v.map(d => [d.year, d.max])), d => d.station),
  ([station, d]) => ({ station, max2025: d["2025"] ?? 0, max2026: d["2026"] ?? 0 })
).filter(d => d.max2025 > 0 && d.max2026 > 0)

// Sort stations by largest increase from 2025 to 2026, only where 2026 > 2025
const stationOrder = surgeLinks
  .filter(d => d.max2026 > d.max2025)
  .sort((a, b) => (b.max2026 - b.max2025) - (a.max2026 - a.max2025))
  .map(d => d.station)

const top3Gap = stationOrder.slice(0, 3)
```

<div class="chart-wrap">
  <h2>Event Ridership Surge</h2>

  <p class="chart-instruction">This chart shows anticipated 2026 event surge in relation to 2025 for stations where event traffic is expected to increase. Stations are sorted by largest increase.</p>

  <p class="chart-instruction">Event surge compares station activity on event days to the average activity on non-event days. Dot size represents current staff count. The top 3 stations with the largest surge increase are annotated.</p>

```js
Plot.plot({
  width: 900,
  height: 400,
  marginLeft: 160,
  style: { fontSize: 12 },
  x: { label: "Surge ratio", grid: true, domain: [0, 1] },
  y: { label: null, domain: stationOrder },
  color: { domain: ["2025", "2026"], range: ["#0e7741", "#e07741"], legend: true },
  r: { range: [2, 8] },
  marks: [
    Plot.line(surgeSummaryAll, {
      x: "max",
      y: "station",
      z: "station",
      stroke: "#ccc",
      strokeWidth: 1
    }),
    Plot.dot(surgeSummaryAll, {
      x: "max",
      y: "station",
      r: "staff",
      fill: "year",
      opacity: 0.5
    }),
    Plot.dot(surgeSummaryAll.filter(d => top3Gap.includes(d.station) && d.year === "2026"), {
      x: "max",
      y: "station",
      r: 10,
      fill: "none",
      stroke: "#e07741",
      strokeWidth: 2
    }),
    Plot.text(surgeSummaryAll.filter(d => top3Gap.includes(d.station) && d.year === "2026"), {
      x: "max",
      y: "station",
      text: d => {
        const link = surgeLinks.find(s => s.station === d.station)
        return "+" + (link.max2026 - link.max2025).toFixed(2) + " surge"
      },
      textAnchor: "start",
      fontSize: 12,
      dx: 14
    })
  ]
})
```

</div>