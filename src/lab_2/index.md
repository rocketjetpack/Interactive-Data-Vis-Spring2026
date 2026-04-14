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
    font-size: 12pt;
    line-height: 1.5;
    color: #222;
    max-width: 860px;
  }

  .notes-box strong {
    color: #0e7741;
  }

  .answer-box {
    padding: 5px 5px;
    margin: 5px 0;
    font-size: 12pt;
    line-height: 1.5;
    max-width: 900px;
  }

  .answer-box p {
    max-width: 860px;
  }

  .input-wrap {
    margin: 5px 0px;
  }

  .input-wrap label {
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    color: #0e7741;
    display: block;
    margin-bottom: 3px;
  }

  .input-wrap select {
    appearance: none;
    background: #f9f9f9;
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
// Generate a list of unique stations from the stations object
const stationPick = view(Inputs.select(stations, { label: "Station", value: "Times Sq-42 St" }));
```

  </div>

```js
// Filter ridership data to the selected station
const stationData = ridership.filter(d => d.station === stationPick);

// Fetch events from 2025 that occurred near the selected station
const eventDates = new Set(local_events.filter(e => e.nearby_station === stationPick).map(e => e.date.getTime()));

// Create a object combining event date with the event type filtered by the selected station
const stationEventDots = stationData.filter(d => eventDates.has(d.date.getTime()))
  .map(d => ({
    date: d.date,
    eventName: local_events.find(e => e.nearby_station === stationPick && e.date.getTime() === d.date.getTime())?.event_name
  }));
```

```js
Plot.plot({
  width: 900,
  height: 460,
  x: { type: "time", tickFormat: "%b %-d", ticks: 10, axis: "top" },
  y: { domain: [0, 35000] },
  marginBottom: 120, // Leave plenty of room for event labels
  marks: [
    // Start with transparent lines for all stations
    Plot.lineY(ridership, {
      x: "date",
      y: "entrances",
      z: "station",
      stroke: "#333",
      opacity: 0.15,
      strokeWidth: 1,
    }),

    // Add a solid green line for the selected station
    Plot.lineY(stationData, {
      x: "date",
      y: "entrances",
      stroke: "#0e7741",
      strokeWidth: 2.5,
      opacity: 1,
      tip: true,
      title: d => `Date: ${d.date.toLocaleDateString("en-US", { month: "short", day: "numeric" })}\nEntrances: ${d.entrances.toLocaleString()}`,
    }),

    // Draw vertical dashed lines representing events at the selected station from 2025
    Plot.ruleX(stationEventDots, {
      x: "date",
      stroke: "#000",
      strokeWidth: 1,
      strokeDasharray: "4,3",
    }),

    // Label the bottom of the event dashed line with the type of event
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

    // July 15 represents a fare increase and should be drawn for every station
    Plot.ruleX([fareDate], {
      stroke: "red",
      strokeWidth: 1.5,
      strokeDasharray: "6,4",
      opacity: 0.5
    }),

    // Add an annotation to make it clear that July 15 represents the fare increase
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
I must admit, I spent far too long playing with the style of this. I wanted a self-contained plot element that tied the select box in with the plot itself as a visually distinct element on the page. I generally like the appearance, and it made me experiment with CSS and HTML with Observable elements inside.

Also, thanks to Claude for generally useful CSS. CSS is such an annoying time sink.
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
/// I dont think its safe to re-display the pervious charts station dropdown, so this is a new one
const stationPick_Incident = view(Inputs.select(stations, { label: "Station", value: "Times Sq-42 St" }));
```

```js
// Filter incident data by the selected station to enable tooltips for only the selected one
const filtered = incidents.filter(d => d.station === stationPick_Incident);

// Add the selection status to the raw data
const stationAvg = incidents.map(d => ({
  ...d,
  selected: d.station === stationPick_Incident
}));
```

```js
// Construct a spreadable object that represents response time by station
// I am new to this spreadable concept, but the Observable docs recommended it in some examples, so I guess its time to learn.
// This means all the data for the plot needs to be in a single structure
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
    // Add a line to separate station names from incident response data
    Plot.ruleX([0]),
    
    // Mark the average response time for all incidents
    Plot.ruleX([d3.mean(incidents, d => d.response_time_minutes)], { stroke: "red", strokeOpacity: 0.5 }),

    // Label the incident average line
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

    // Horizontal line showing the range from fastest to slowest response per-station
    Plot.ruleY(stationAvg, Plot.groupY({ x1: "min", x2: "max" }, { ...xy, stroke: "#ddd" })), 

    // Dot mark the average response times for each incident severity per-station
    Plot.dot(stationAvg, Plot.groupY({ x: "mean" }, { ...xy, fill: "severity", fillOpacity: 0.2, r: 4 })),

    // Dot mark the average response times for each incident severity for the selected station and add a tip
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
<br />
<div class="explainer-area">
    I also wanted to draw a box to group the eight stations with the best response times as they are very similar. I couldn't find a way. I suspect that slicing the top 8 and using that in a Plot.boxX  would do it, but repeatedly failed in trying to do this.
  </div>
  </div>

  <div class="answer-box">
    <p>
    From the incident data, Times square has the fastest overall response to events, but several other stations respond more quickly to <strong style="color: red">high</strong> severity events. Overall, there are eight stations that have functionally comparable response times.
    </p>
  </div>
</div>

<hr />

## Section 3: Staffing Need Prediction

<div class="notes-box">
  The third question for this lab asks us to identify three stations needing the most help for the 2026 summer season based on upcoming events.
</div>

```js
// Average daily entrances + exits per station across all of summer 2025
const avgDailyRidership = d3.rollup(
  ridership,
  v => d3.mean(v, d => d.entrances + d.exits),
  d => d.station
)

// Calcualte how much each events attendance represent relative to a normal day?
const eventSurges = local_events.map(d => ({
  ...d,
  surgeRatio: d.estimated_attendance / (avgDailyRidership.get(d.nearby_station) ?? 1)
}))

// Calculate the same for the expected events in 2026
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

// Bring the data for 2025 and 2026 into one array and add a year column
const surgeSummaryAll = [
  ...surgeSummaryFrom(eventSurges, "nearby_station", "2025"),
  ...surgeSummaryFrom(upcomingSurges, "nearby_station", "2026")
]

// Restructure the array to be grouped by station with stats from 2025 and 2025 as fields
const surgeLinks = Array.from(
  d3.rollup(surgeSummaryAll, v => Object.fromEntries(v.map(d => [d.year, d.max])), d => d.station),
  ([station, d]) => ({ station, max2025: d["2025"] ?? 0, max2026: d["2026"] ?? 0 })
).filter(d => d.max2025 > 0 && d.max2026 > 0)

// Sort stations by largest increase from 2025 to 2026, only where 2026 > 2025
const stationOrder = surgeLinks
  .filter(d => d.max2026 > d.max2025)
  .sort((a, b) => (b.max2026 - b.max2025) - (a.max2026 - a.max2025))
  .map(d => d.station)

// Use array slice to get the top 3 stations with the highest surge increase
const top3Gap = stationOrder.slice(0, 3)
```

<div class="chart-wrap">
  <h2>Event Ridership Surge</h2>

  <p class="chart-instruction">This chart shows anticipated 2026 event surge in relation to 2025 for stations where event traffic is expected to increase. Stations are sorted by largest increase.</p>

  <p class="chart-instruction">Event surge compares station activity on event days to the average activity on non-event days. Dot size represents current staff count. The top 3 stations with the largest surge increase are annotated.
  </p>


```js
Plot.plot({
  width: 900,
  height: 400,
  marginLeft: 160,
  style: { fontSize: 12 },
  x: { label: "Surge ratio", grid: true, domain: [0, 1] },
  y: { label: null, domain: stationOrder },
  color: { domain: ["2025", "2026"], range: ["#0e7741", "#e07741"], legend: true }, //define the coloring
  r: { range: [2, 8] }, // Range of radius size to make staff level part of the chart
  marks: [
    // Add a clear line between station names and surge data
    Plot.ruleX([0]),

    // Horizontal line connecting 2025 surge ratio with 2026
    Plot.line(surgeSummaryAll, {
      x: "max",
      y: "station",
      z: "station",
      stroke: "#ccc",
      strokeWidth: 1
    }),

    // Draw dots for 2025 and 2026 surge ratio per-station colored by year and sized by staff count
    Plot.dot(surgeSummaryAll, {
      x: "max",
      y: "station",
      r: "staff",
      fill: "year",
      opacity: 0.5
    }),

    // Draw larger circles around the 2026 dots for the 3 stations anticipating the largest increase in 2026
    Plot.dot(surgeSummaryAll.filter(d => top3Gap.includes(d.station) && d.year === "2026"), {
      x: "max",
      y: "station",
      r: 10,
      fill: "none",
      stroke: "#e07741",
      strokeWidth: 2
    }),

    // Label the surge ratio increase from 2025 to 2026 for those 3 stations
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

<div class="answer-box">
  <p>
    To answer this question I first rollup each stations daily entrances and exits by station for 2025, then look at traffic on days with events at a nearby station to calculate a ratio of how much the event-day traffic exceeds the average day. This effect is scaled with the estimated_attendance value for the event to scale the event surge with the size of the event.
  </p>
  <p>
    This same approach is then applied to the expected_attendance for upcoming 2026 events. Only nine stations are expected to increase event traffic in 2026. The largest expected event based increase is <strong style="color: red">West 4th St - Washington Square</strong>.  This station has an average daily entrances and exits of 11,323, and only one small event in 2025 with 1,120 estimated attendance. In June 2026, a gallery opening near W 4th is expected to draw 8,328 attendance.
  </p>
  <p>
    This 2026 event surge prediction based on 2025 values also highlights Fulton St and 23rd St as stations at risk of being heavily impacted by increased activity for events. Staffing levels at West 4th St and 23rd St are low, with 4 and 8 staff respectively. Fulton St is a bit unique with a healthy 17 staff, though it also has 4 events planned for the summer of 2026.
</div>

<hr />

## Bonus: One Station to Increase Staff

<div class="chart-wrap">
  <h2>Staffing Level, Average Riders, and 2026 Surge</h2>

  <p class="chart-instruction">
    This chart explores average daily ridership on the X axis, staffing level on the Y axis, and anticipated 2026 surge as the color.
  </p>

```js
// Recover the 2026 surge expectation from surgeSummaryAll
const surge2026ByStation = new Map(
  surgeSummaryAll
  .filter( d => d.year === "2026" )
  .map(d => [d.station, d.max])
)

//Construct a single object that contains staffing, average daily ridership, and 2026 surge grouped by station
const bonusPlotData = Object.entries(currentStaffing).map(
  ([station, staff]) => ({
    station,
    staff,
    avgDaily: avgDailyRidership.get(station) ?? 0,
    surge2026: surge2026ByStation.get(station) ?? 0
  })
)
```

```js
// Construct the scatter plot
Plot.plot({
  width: 900,
  height: 500,
  x: { label: "Avg. Daily Ridership", grid: true, domain: [9000, 38000] },
  y: { label: "Staff Count", grid: true, domain: [2, 22] },
  color: { label: "2026 Surge", legend: true, scheme: "YlOrRd" },
  r: { range: [1, 30] },
  marks: [
    Plot.dot(
      bonusPlotData,
      {
        x: "avgDaily",
        y: "staff",
        fill: "surge2026",
        r: "avgDaily",
        opacity: 0.8,
        tip: true,
        title: d => `${d.station}\nAvg ridership: ${Math.round(d.avgDaily)}\nStaff: ${d.staff}\n2026 Surge: ${d.surge2026.toFixed(2)}`
      }
    )
  ]
})
```

</div>

<div class="answer-box">
  <p>
    This chart highlights a major challenge point that was not revealed in Section 2: Canal St. This station had no nearby events in 2025 and was ignored in the filtering in Section 2, which was purely focused on stations expecting more event traffic in 2026 than they had in 2025. <strong style="color: red">Canal St</strong> had no nearby events in 2025, but is scheduled for a whopping 8 nearby events in 2026! Operating with only 4 staff, and expecting traffic surge of 113% of normal ridership, this station will be in dire need of additional staffing.
  </p>
</div>
</div>