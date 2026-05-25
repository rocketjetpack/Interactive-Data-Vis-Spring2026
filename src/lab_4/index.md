---
title: "Lab 4: Tornado Alley on the Move"
toc: true
---

<!-- Data imports -->
```js
// Load the processed CSV with 
const tornadoData = await FileAttachment("data/tornadoes/tornadoes_with_night_flag.csv").csv({typed: true});
const us = await FileAttachment("data/counties-10m.json").json();
```

```js
const states = topojson.feature(us, us.objects.states);
const nation = topojson.feature(us, us.objects.nation);
const contiguousStates = {
  type: "FeatureCollection",
  features: states.features.filter(d => d.id !== "02" && d.id !== "15")
};
const contiguousCounties = {
  type: "FeatureCollection",
  features: topojson.feature(us, us.objects.counties).features
    .filter(d => d.id && !d.id.startsWith("02") && !d.id.startsWith("15") && parseInt(d.id) < 57000)
};
```

<style>
  .lead {
    font-size: 13pt;
    line-height: 1.55;
    max-width: 860px;
    color: #222;
    margin: 0.8rem 0 1.6rem 0;
  }
  .lead strong {
    color: #8b1a1a;
  }

  .notes-box {
    background: #f8f4ee;
    border-left: 5px solid #8b1a1a;
    padding: 1rem 1.4rem;
    margin: 1.4rem 0;
    font-size: 12.5pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 860px;
  }
  .notes-box strong {
    color: #8b1a1a;
  }
  .notes-box em {
    font-style: italic;
    color: #4a4a4a;
  }

  .chart-wrap {
    border: 1.5px solid #8b1a1a;
    padding: 1.4rem 1.6rem;
    margin: 1.4rem 0;
    max-width: 930px;
    background: #fafaf8;
  }
  .chart-wrap h2 {
    margin-top: 0;
  }

  .chart-wrap .chart-instruction {
    font-size: 0.82rem;
    color: #555;
    margin-bottom: 1rem;
    font-style: italic;
    line-height: 1.5;
    max-width: none;
    width: 100%;
  }

  .chart-wrap .chart-instruction strong {
    color: #8b1a1a;
    font-style: normal;
  }

  .explainer-area {
    font-size: 0.82rem;
    color: #555;
    line-height: 1.55;
    max-width: 780px;
    margin: 0.6rem 0 1.4rem 0.5rem;
    padding: 0.5rem 0 0.5rem 1rem;
    border-left: 2px solid #cfcfcf;
  }
  .explainer-area::before {
    font-weight: 600;
    color: #444;
  }

  .answer-box {
    background: #fffbf5;
    border-top: 3px solid #8b1a1a;
    border-bottom: 1px solid #ead9bf;
    padding: 1.1rem 1.4rem;
    margin: 1rem 0 1.8rem 0;
    font-size: 12pt;
    line-height: 1.65;
    max-width: 860px;
    color: #1a1a1a;
  }
  .answer-box p {
    max-width: 860px;
    margin: 0;
  }
  .answer-box p + p {
    margin-top: 0.7rem;
  }
  .answer-box ol {
    max-width: 860px;
    padding-left: 1.4rem;
  }
  .answer-box ol li {
    margin-bottom: 0.6rem;
  }
  .answer-box strong {
    color: #8b1a1a;
  }

  .year-display {
    font-size: 2.6rem;
    font-weight: 300;
    text-align: center;
    color: #222;
    margin: 0.4rem 0 0.6rem 0;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.02em;
  }

  .chart-wrap form {
    font-family: inherit;
    font-size: 0.9rem;
    margin: 0 0 1.2rem 0;
    width: 100%;
  }
  .chart-wrap form input[type="range"] {
    accent-color: #8b1a1a;
    width: 100%;
    cursor: pointer;
  }
  .chart-wrap form input[type="number"] {
    display: none;
  }

  .map-container {
    background: white;
    border: 1px solid #ddd;
    min-height: 480px;
  }

  .map-legend {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1rem 0 0.4rem 0;
    font-size: 0.85rem;
    color: #333;
  }
  .map-legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .map-legend-swatch {
    width: 14px;
    height: 14px;
    display: inline-block;
    border-radius: 50%;
  }
  .swatch-day { background: #c89b3e; }
  .swatch-night { background: #2c5f7c; }
  
</style>

# Lab 4: Tornado Alley on the Move
#### Kali McLennan

<p class="lead">
"Tornado Alley" is the corridor of violent storms which traditionally stretched from Texas to South Dakota. Since being
named in the 1950s this area has defined the area the public associates with tornado risk. 76 years of NOAA records tell
a different story: the center of tornado activity has been <strong>drifting steadily eastward</strong> into the Dixie states, 
where population density is higher, mobile homes are more common, and the deep warning culture that the plains states built
over generations simply does not exist. The question is not whether the alley is moving. The question is <strong>what 
happens to the communities in its path.</strong>
</p>

<hr />

## Section 1: Seventy-Six Years of Data
<div class="notes-box">
  Data for this lab comes from the <a href="https://www.ncei.noaa.gov/stormevents/">NOAA Storm Events Database</a> and contains
  extensive information on all tornadoes recognized by NOAA going back to October 1950. This dataset consists of many columns, and
  the data dictionary is distributed by NOAA in <a href="https://www.spc.noaa.gov/wcm/data/SPC_severe_database_description.pdf">what might
  be the world's worst PDF</a>. I wrote a simple Python preprocessor to extract fields of relevance for this lab and to flag each record by whether the
  touchdown of a tornado occurred before or after solar twilight. These night tornadoes are often far deadlier than those in the day. 
</div>

<p class="lead">
  This first section provides a simple dot plot of the touchdown location of all 71,795 tornado records for the continental
  United States. Each is color coded by its rating on the <a href="https://www.weather.gov/oun/efscale">Enhanced Fujita Scale</a>.
  This scale went into effect early in 2007, and events prior to this were rated either on the former Fujita Scale or through
  inference from reported wind speed or hail diameter. This is a real limitation of this dataset and a professional analysis
  should make effort to reconcile the scales.
</p>

<div class="chart-wrap">
  <h2>All US Tornado Touchdowns, 1950–2025</h2>
  <p class="chart-instruction">
    Each dot is one tornado touchdown. <strong>Color</strong> shows the EF/F rating; <strong>size</strong> grows with
    the casualty toll starting from a minimum of 50 casualties. Tornadoes with unknown ratings are excluded, and Alaska
    and Hawaii are not shown. Hover any larger dot for the date and casualty counts.
  </p>

  <p class="chart-instruction">
  <strong>You can click on any of the magnitude bars under the map to filter the map to just that
  magnitude.</strong><br />For example, to see only EF3 events click on the orange EF3 bar under the map.
  </p>

```js
// Weighted impact: a fatality counts twice as much as an injury.
// Sorting ascending puts the deadliest dots last, so they render on top.
const impactOf = d => 2 * d.fat + d.inj;

const tornadoesContiguous = tornadoData
  .filter(d => d.mag >= 0 && d.slat > 23 && d.slat < 50 && d.slon > -125 && d.slon < -65)
  .sort((a, b) => impactOf(a) - impactOf(b));

const tornadoesWithLowCasualties = tornadoesContiguous
  .filter( d=> (d.inj + d.fat) <= 50 );

const tornadoesWithHighCasualties = tornadoesContiguous
  .filter( d => (d.inj + d.fat ) > 50 )
  .sort((a, b) => (b.inj + b.fat) - (a.inj + a.fat))
  .reverse();

const casualtiesByMag = Array.from(
  d3.rollup(
    tornadoesContiguous,
    rows => d3.sum(rows, d => d.inj + d.fat),
    d => d.mag
  ),
  ([mag, casualties]) => ({ mag,casualties})
)
```

```js
const selectedMag = Mutable(null);
const setSelectedMag = (v) => { selectedMag.value = v; };
```

```js
const mapLow  = selectedMag === null ? tornadoesWithLowCasualties
              : tornadoesWithLowCasualties.filter(d => d.mag === selectedMag);
const mapHigh = selectedMag === null ? tornadoesWithHighCasualties
              : tornadoesWithHighCasualties.filter(d => d.mag === selectedMag);

display(Plot.plot({
  projection: "albers-usa",
  width: 860,
  color: {
    type: "ordinal",
    domain: [1, 2, 3, 4, 5],
    scheme: "YlOrRd",
    legend: false,
    label: "EF/F Rating",
    tickFormat: d => `EF${d}`
  },
  r: {
    type: "sqrt",
    domain: [0, 1000],
    range: [1.25, 10],
    clamp: true
  },
  marks: [
    Plot.geo(contiguousStates, { fill: "#e8e4de", stroke: "white", strokeWidth: 0.8 }),
    Plot.dot(mapLow, {
      x: "slon", y: "slat",
      fill: "mag",
      r: 1.25,
      fillOpacity: 0.65,
      stroke: null,
      channels: {
        Date: d => d.date,
        Rating: d => `EF${d.mag}`,
        Deaths: d => d.fat,
        Injuries: d => d.inj
      },
      tip: false
    }),
    Plot.dot(mapHigh, {
      x: "slon", y: "slat",
      fill: "mag",
      r: d => (2 * (d.fat + d.inj)),
      fillOpacity: 0.65,
      stroke: null,
      channels: {
        Date: d => d.date,
        Rating: d => `EF${d.mag}`,
        Deaths: d => d.fat,
        Injuries: d => d.inj
      },
      sort: { channel: "r", order: "ascending" },
      tip: {
        format: {
          x: false,
          y: false,
          fill: false,
          r: false,
          Date: d => d.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" })
        }
      }
    })
  ]
}))
```

```js
const magsSorted = casualtiesByMag.sort((a, b) => a.mag - b.mag);

const barChart = Plot.plot({
  width: 860,
  height: 160,
  marginLeft: 65,
  marginBottom: 40,
  marginTop: 20,
  x: { label: "EF/F Rating" },
  y: {
    label: "Total casualties",
    grid: true,
    domain: [0, 40000]
  },
  color: {
    type: "ordinal",
    domain: [0, 1, 2, 3, 4, 5],
    scheme: "YlOrRd"
  },
  marks: [
    Plot.barY(magsSorted, {
      x: d => `EF${d.mag}`,
      y: "casualties",
      fill: "mag",
      fillOpacity: d => selectedMag === null || d.mag === selectedMag ? 1 : 0.25,
      tip: false,
      cursor: "pointer"
    }),
    Plot.ruleY([0])
  ]
});

d3.select(barChart).selectAll("rect").each(function(_, i) {
  d3.select(this).on("click", () => {
    setSelectedMag(selectedMag === magsSorted[i].mag ? null : magsSorted[i].mag);
  });
});

display(barChart);
```

</div>

<div class="explainer-area">
  This graphic is drawn by splitting the dataset into two passes. The lower layer is drawn
  without tooltips and represents tornado events with 50 or fewer casualties. The upper layer
  is drawn with tooltips for events with more than 50 casualties. The hook into clicking on
  the bars would not have been possible for me without Claude assistance, though because of
  AI assistance I have now learned about Observables <strong><a href="https://observablehq.com/@observablehq/mutable">Mutable</a></strong> mechanism to allow
  one cell to be re-run as a result of change in a different cell. In this case, the bar chart is a separate cell which manipulates a variable named <i>selectedMag</i> and triggers the
  first cell (the map) to rerun with the new value.
</div>

<div class="answer-box">
  <p>
    The deadliest tornadic events of the last 76 years are clustered loosely in a triangle covering roughly the area between north-central Texas, the Great Lakes, and down through Alabama. This encompasses three generally recognized areas of tornadic activity: the Great Plains, the Midwest, and the Deep South.
  </p>
</div>

<hr />

## Section 2: The Moving Alley

<div class="lead">
  Where tornadoes <i>happen</i> is one question; where they have been happening <strong>more than usual</strong> in more recent years is another. This map explores the second one by
  comparing comparative tornado activity in each county against the average for that county
  in the previous 5 years. Individual tornado events are semi-randomly distributed, but trends can be inferred across reasonable timespans.
</div>

<div class="chart-wrap">
  <h2>Tornado Anomaly by County, 5-Year Window</h2>
  <p class="chart-instruction">
    Each county is colored by the previous five-year average minus its average across the full
    data set. You will see two trends that are important. Up through the early 2000s the classic Tornado Alley from Oklahoma through the Dakotas represents the highest areas of activity. Between roughly 2020 and 2025 the most active area is shifting southeast into Dixie Alley.
    <br /><strong style="color: #b2182b">Red</strong> = Increased frequency of tornadoes;
    <br /><strong style="color: #2166ac">blue</strong> = Decreased frequency.
    <br /><strong>Drag the scrubber to compare windows.</strong>
  </p>

```js
// Per-county tornado counts and all-time averages. One-time computation.

const anomalyWindowSize = 5;
const anomalyStartYear  = 1955;
const anomalyEndYear    = 2025;

// Build 5-digit FIPS string (e.g. "48303") from state FIPS + first county FIPS.
// We credit each tornado to its STARTING county only (f1). ~95% of tornadoes are
// single-county; this keeps the data layer simple at the cost of a small undercount
// in the few counties downstream of long-track tornadoes.
const fipsOf = d => String(d.stf).padStart(2, "0") + String(d.f1).padStart(3, "0");

const validForAnomaly = tornadoData.filter(d =>
  d.mag >= 0 && d.stf && d.f1 &&
  d.slat > 23 && d.slat < 50 && d.slon > -125 && d.slon < -65
);

// Map<fips, Map<year, count>>
const countyByYear = d3.rollup(
  validForAnomaly,
  rows => rows.length,
  fipsOf,
  d => d.yr
);

// Map<fips, allTimeAveragePerYear>
const anomalyTotalYears = anomalyEndYear - anomalyStartYear + 1;
const countyAvgPerYear = new Map();
for (const [fips, byYear] of countyByYear) {
  countyAvgPerYear.set(fips, d3.sum(byYear.values()) / anomalyTotalYears);
}

// Helper: deviation (window-avg-per-year − all-time-avg-per-year) for one county/window-end.
// Handles short windows at the start of the dataset by clamping windowStart to anomalyStartYear.
function countyDeviation(fips, endYear) {
  const windowStart = Math.max(anomalyStartYear, endYear - anomalyWindowSize + 1);
  const actualSize  = endYear - windowStart + 1;
  const byYear      = countyByYear.get(fips);
  const allTime     = countyAvgPerYear.get(fips) ?? 0;
  if (!byYear) return -allTime;   // zero tornadoes ever → window-avg is 0
  let sum = 0;
  for (let y = windowStart; y <= endYear; y++) sum += byYear.get(y) ?? 0;
  return (sum / actualSize) - allTime;
}
```

```js
display(html`<div class="year-display">${anomalyYear}</div>`);
```

```js
const anomalyYear = view(Inputs.range(
  [anomalyStartYear, anomalyEndYear],
  { step: 1, value: 2010, label: "" }
));
```

  <div class="map-container" id="anomaly-map-container">
    <!-- D3 will inject the SVG here -->
  </div>

```js
// === Section 1.5 render setup ===
// Runs once. Builds the SVG, fills the counties, draws state outlines on top.

const anomalyMapWidth  = 860;
const anomalyMapHeight = 540;

d3.select("#anomaly-map-container").selectAll("*").remove();

const anomalyMapSvg = d3.select("#anomaly-map-container").append("svg")
  .attr("viewBox", `0 0 ${anomalyMapWidth} ${anomalyMapHeight}`)
  .attr("width", "100%")
  .style("display", "block");

const anomalyProjection = d3.geoAlbersUsa()
  .fitSize([anomalyMapWidth, anomalyMapHeight], contiguousStates);
const anomalyGeoPath = d3.geoPath(anomalyProjection);

// Counties layer — drawn first so state outlines overlay cleanly
const anomalyCountiesLayer = anomalyMapSvg.append("g").attr("class", "counties");

// State outlines on top — thin gray lines for reference
anomalyMapSvg.append("g")
  .selectAll("path")
  .data(contiguousStates.features)
  .join("path")
    .attr("d", anomalyGeoPath)
    .attr("fill", "none")
    .attr("stroke", "#666")
    .attr("stroke-width", 0.6);

// Color scale: diverging RdBu, reversed so red = above normal, blue = below.
// Symmetric domain so colors mean the same thing across all years (critical for
// honest scrubbing comparison). ±2 tornadoes/year captures the bulk of real swings.
const anomalyColorScale = d3.scaleDiverging(t => d3.interpolateRdBu(1 - t))
  .domain([-2, 0, 2])
  .clamp(true);
```

```js
// === Section 1.5 reactive update ===
// Re-runs whenever anomalyYear changes. Smoothly transitions county fill colors.

const anomalyTransitionMs = 300;

anomalyCountiesLayer.selectAll("path")
  .data(contiguousCounties.features, d => d.id)
  .join(
    enter => enter.append("path")
      .attr("d", anomalyGeoPath)
      .attr("stroke", "none")
      .attr("fill", d => anomalyColorScale(countyDeviation(d.id, anomalyYear))),
    update => update.call(sel =>
      sel.transition().duration(anomalyTransitionMs)
         .attr("fill", d => anomalyColorScale(countyDeviation(d.id, anomalyYear)))
    )
  );
```

</div>

<div class="explainer-area">
  I have to admit, this one also relied on Claude for several core parts I wanted to include but didn't know how to implement. I wanted more exposure to using D3 directly, and this chart along with the following one use D3 to directly manipulate an SVG in response to changes in the slider. The concept here is 100% mine and the implementation is roughly 50/50, especially because Claude really struggles to differentiate Observable Framework syntax from Observable notebooks.
</div>

<div class="answer-box">
  <p>
    Two trends emerge from scrubbing across the years with this county-level view. First is that there is a clear jump in color intensity starting around 1990. This is attributable to the installation of the NEXRAD radar starting in 1992. This resulted in the recording of far more tornadoes because they could be spotted from radar data without requiring human confirmation. This led to comparatively far more events being reported in rural counties than previous years.
  </p>
  <p>
    The second trend of importance occurs between roughly 2005 and 2025. In these years the historical hot-spot of Oklahoma and Kansas rapidly becomes blue while the Dixie Alley states of Alabama and Mississippi become deep red. This is the real pattern of importance: <strong>Tornado Alley is moving to the southeast, and these states are poorly prepared.</strong>
  </p>
</div>

<hr />

<div class="lead">
  The following map presents functionally the same data, but as a density map highlighting where
  tornado events have been by density in each year of the dataset. This works the same as the previous map where you can drag the year slider and see how the density of events changes over time.
</div>

<div class="chart-wrap">
  <h2>The Moving Alley, 1950–2025</h2>
  <p class="chart-instruction">
    A fifteen-year sliding window of tornado activity, smoothed into density contours and redrawn for each year you
    select. <strong>Deeper red</strong> = denser activity in that window. Use the EF filter to focus on stronger
    storms. Adjacent frames cross-fade so the drift reads as motion rather than as a series of jumps.
  </p>

```js
// === Section 2 data layer ===
const windowSize = 15;
const startYear = 1950;
const endYear = 2025;

// Year-indexed lookup: Map<year, row[]>, filtered by the current min EF rating
const tornadoesByYear = d3.group(
  tornadoData.filter(d => d.mag >= minMag),
  d => d.yr
);

// Window selector: returns all rows in the trailing windowSize years ending at `year`.
function tornadoesInWindow(year) {
  const out = [];
  for (let i = 0; i < windowSize; i++) {
    const rows = tornadoesByYear.get(year - i);
    if (rows) out.push(...rows);
  }
  return out;
}
```

```js
display(html`<div class="year-display">${year}</div>`);
```

```js
const year = view(Inputs.range([startYear, endYear], {step: 1, value: 1950, label: ""}));
```

  <div class="map-container" id="map-container">
    <!-- D3 will inject the SVG here -->
  </div>

```js
const mapWidth = 860;
const mapHeight = 540;
const minMag = 1;

d3.select("#map-container").selectAll("*").remove();

const mapSvg = d3.select("#map-container").append("svg")
  .attr("viewBox", `0 0 ${mapWidth} ${mapHeight}`)
  .attr("width", "100%")
  .style("display", "block");

const projection = d3.geoAlbersUsa().fitSize([mapWidth, mapHeight], contiguousStates);
const geoPath = d3.geoPath(projection);

// Static base map
mapSvg.append("g")
  .selectAll("path")
  .data(contiguousStates.features)
  .join("path")
    .attr("d", geoPath)
    .attr("fill", "#e8e4de")
    .attr("stroke", "white")
    .attr("stroke-width", 0.8);

// Density contour layer — reactively updated below
const densityLayer = mapSvg.append("g").attr("class", "density");
```

```js
const throttleMs   = 10;   // ignore rapid changes; only the latest commits
const transitionMs = 175;   // fade duration for new and exiting paths
// Stash the pending-render timer on the container so it persists across re-runs.
const _container = document.querySelector("#map-container");
if (_container._pendingTimer) clearTimeout(_container._pendingTimer);

_container._pendingTimer = setTimeout(() => {
  const rows = tornadoesInWindow(year);

  const contours = d3.contourDensity()
    .x(d => projection([d.slon, d.slat])?.[0] ?? -1)
    .y(d => projection([d.slon, d.slat])?.[1] ?? -1)
    .size([mapWidth, mapHeight])
    .bandwidth(40)
    .thresholds(20)
    (rows);

  const densityColor = d3.scaleSequential(d3.interpolateReds)
    .domain([0, d3.max(contours, d => d.value) ?? 1]);

  // Tag each contour with the year/minMag of THIS render, so existing paths
  // carry their original key and the data join correctly identifies them as
  // exiting rather than mistakenly matching them with the new frame's paths.
  const contoursTagged = contours.map((c, i) => ({ ...c, _key: `${year}-${minMag}-${i}` }));

  densityLayer.selectAll("path")
    .data(contoursTagged, d => d._key)
    .join(
      enter => enter.append("path")
        .attr("d", d3.geoPath())
        .attr("fill", d => densityColor(d.value))
        .attr("fill-opacity", 0)
        .attr("stroke", "none")
        .call(sel => sel.transition().duration(transitionMs).attr("fill-opacity", 0.15)),
      update => update,
      exit => exit.call(sel => sel.transition().duration(transitionMs).attr("fill-opacity", 0).remove())
    );
}, throttleMs);
```

</div>

<div class="explainer-area">
  Of all the visuals, this one is the most convincing to me. One can clearly see the area of greatest density begins to drift southeast starting in the late 1990s. There is some reuse of code here, and initially this was a very unpleasant visual. After working on a cross-fade effect between frames and playing with timing, I feel like it's smooth enough, though still somewhat jarring.
</div>

<div class="answer-box">
  <p>
    The center of US tornado activity has moved east. Across the 1960s and 70s windows, the densest red sits over a
    triangle from north Texas through central Oklahoma and into Kansas — the classic Tornado Alley footprint, exactly
    where the name suggests it should be.
  </p>
  <p>
    By the 2010s and 2020s, the densest red has migrated to a broad band across Mississippi, Alabama, Tennessee, and
    Arkansas. This region has denser population centers, more residents in mobile homes, and far less of the warning
    infrastructure and weather-aware culture that Oklahoma and Kansas built over generations. The shift is gradual
    on a year-by-year basis, but impossible to ignore when seen across decades.
  </p>
</div>

<hr />

## Section 3: The Day/Night Divide

<div class="lead">
  There is one more factor that matters when understanding how the movement of tornado activity poses risk
  to communities in Dixie Alley: <strong>tornadoes are also happening more at night in the new hot spot.</strong>
</div>
<div class="lead">
  The following chart presents the proportion of tornadoes that begin after local sundown across the data set, grouped by
  the classic Tornado Alley region and the Dixie Alley.
</div>

<div class="chart-wrap">
  <h2>Nighttime Share of EF2+ Tornadoes, by Decade</h2>
  <p class="chart-instruction">
    Each point is the share of EF2+ tornadoes in that decade that struck after civil twilight (sun more than 6° below
    the horizon). <strong style="color: #8b1a1a">Crimson</strong> is the Dixie states; <strong>dashed gray</strong> is the
    Plains. The wedge between them is the regional gap — narrow at mid-century, twice as wide today.
  </p>

```js
// Create two groups of states
const plainsStates = new Set(["TX", "OK", "KS", "NE", "SD", "ND", "CO"]);
const dixieStates = new Set(["AR", "LA", "MS", "AL", "TN", "KY", "MO", "GA"]);

// Helper function that when given a state will return either of the relevent regions or null
function regionFor(state) {
  if (plainsStates.has(state)) return "Plains";
  if (dixieStates.has(state)) return "Dixie";
  return null;  // exclude these unrelated states
}

const section3MinMag = 1;  // This is important

// Per-region-decade rollup
const regionalDecadeShares = d3.flatRollup(
  tornadoData
    .filter(d => d.mag >= section3MinMag && regionFor(d.st) !== null),
  rows => ({
    n: rows.length,
    nightShare: d3.mean(rows, d => d.is_night)   // is_night is 0/1, mean = share
  }),
  d => regionFor(d.st),
  d => Math.floor(d.yr / 10) * 10
)
.map(([region, decade, stats]) => ({ region, decade, ...stats }))
.sort((a, b) => a.region.localeCompare(b.region) || a.decade - b.decade);
```

```js
// Calculate the middle area between the two regions for shading
const wedgeData = Array.from(
  d3.rollup(
    regionalDecadeShares,
    rows => Object.fromEntries(rows.map(r => [r.region, r.nightShare])),
    d => d.decade
  ),
  ([decade, shares]) => ({
    decade,
    plains: shares["Plains"],
    midsouth: shares["Dixie"]
  })
).sort((a, b) => a.decade - b.decade);

// Per-region subsets
const plainsRows   = regionalDecadeShares.filter(d => d.region === "Plains");
const midSouthRows = regionalDecadeShares.filter(d => d.region === "Dixie");

// Inline labels live at the last decade in each region's series
const lastDecade = d3.max(regionalDecadeShares, d => d.decade);
const endLabels  = regionalDecadeShares.filter(d => d.decade === lastDecade);

const decadeTicks = Array.from(new Set(regionalDecadeShares.map(d => d.decade)))
  .sort((a, b) => a - b);
```

```js
Plot.plot({
  width: 860,
  height: 380,
  marginLeft: 55,
  marginRight: 90,
  marginTop: 20,
  marginBottom: 40,
  x:
  {
    label: "Decade",
    ticks: decadeTicks,
    },
  y:
  {
    label: "Night Share",
    domain: [0.18, 0.55],
    ticks: [0.2, 0.3, 0.4, 0.5],
    tickFormat: ".0%",
  },
  marks: [
    Plot.gridX({
      strokeDasharray: "5,5",
      strokeOpacity: 0.05
    }),
    Plot.gridY({
      strokeOpacity: 0.1
    }),
    Plot.areaY(wedgeData,
      {
        x: "decade",
        y1: "plains",
        y2: "midsouth",
        fill: "crimson",
        fillOpacity: 0.10
      }
    ),
    Plot.line(plainsRows, {
      x: "decade",
      y: "nightShare",
      stroke: "darkgrey",
      strokeDasharray: "8",
      strokeWidth: 1.5,
      tip: { 
        format: { 
          x: d => `${d}s`, y: d3.format(".0%")
        } 
      }
    }),
    Plot.line(midSouthRows, {
      x: "decade",
      y: "nightShare",
      stroke: "crimson",
      strokeWidth: 1.5,
      strokeDasharray: "8",
      tip: { format: { x: d => `${d}s`, y: d3.format(".0%") } }
    }),
    Plot.dot(
      plainsRows,
      {
        x: "decade",
        y: "nightShare",
        fill: "darkgrey",
        r: 4
      }
    ),
    Plot.dot(
      midSouthRows,
      {
        x: "decade",
        y: "nightShare",
        fill: "#8b1a1a",
        r: 5
      }
    ),
    Plot.text(endLabels,
      {
        x: "decade",
        y: "nightShare",
        text: "region",
        dx: 10,
        textAnchor: "start",
        fill: d => d.region === "Dixie" ? "crimson" : "darkgrey",
        fontWeight: 600,
        fontSize: 13
      }
    )
  ]
})
```

</div>

<div class="explainer-area">
  I struggled a lot with this chart, but for an unexpected reason: it looks visually way more dramatic when filtering the data to EF2+ events. I think this is a bit of a statistical anomaly, as all other minimum strength
  filters show an increase for both the Plains and Dixie areas. I settled on being accurate over being visually
  impactful.
</div>

<div class="lead">
    Across all states in both the Plains and Dixie regions the frequency of nighttime tornadoes follows a similar
    trend: dipping slightly in the earliest years of the dataset, then increasing significantly since the 1980s.
</div>
<div class="lead">
    Time will tell if this trend continues, but any tornado that strikes at night is far more dangerous by default —
    most people will be asleep and unable to respond to warnings.
</div>
<hr />

## What the Data Tells Us

<div class="answer-box">
  <p>
    Tornado Alley is not where it used to be. Through the first ~50 years of data tornado activity was centered in
    the traditional belt from northern Texas up through the Dakotas. However, analysis of recent years shows that
    tornado events are becoming much more common in the Dixie states near the Gulf of Mexico.
  </p>
  <p>
    Worse yet, an increasing number of these events are happening at night. The Dixie states generally have higher
    population density in their urban areas than the Plains, and do not benefit from the decades of experience with
    tornadoes that has resulted in a weather-aware culture in the Plains. When combined, all these factors are likely
    to result in more severe loss of life and injuries in the new hot-spot where people are less prepared for tornadoes.
  </p>
  <p>
    <strong>The risk profile has changed, but the public's mental map has not.</strong>
  </p>
</div>

## Final Note
<div class="answer-box">
  <p>
    There are portions of this lab, specifically the direct d3 work on the two national maps showing per-county and density zones, that I could not have reasonably accomplished without Claude assistance. d3 was lightly covered toward the very end of this class, and this lab makes the use of d3 optional, and this is a technology that I deeply want to learn. I did construct Observable versions of these mostly by hand, but the interactive component with year based scrubbing just felt bad. They were jerky, overly response with no form of debouncing or cross-fading. I have learned quite a bit about SVG manipulation via d3 as part of this, and can confidently state that I could have made lower quality versions of these plots in Observable without much AI assistance.
  </p>
  <p>
    Critically, I do not believe anything in this lab exceeds my <i>ability</i> though some portions exceeded my <i>knowledge</i> of these APIs. This is an area where I find AI assistance greatly helps in the process of learning.
  </p>
</div>