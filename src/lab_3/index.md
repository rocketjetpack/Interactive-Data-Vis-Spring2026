---
title: "Lab 3: Mayoral Mystery"
toc: true
---

<!-- Data imports -->
```js
const nyc = await FileAttachment("data/nyc.json").json();
const results = await FileAttachment("data/election_results.csv").csv({ typed: true });
const survey = await FileAttachment("data/survey_responses.csv").csv({ typed: true });
const events = await FileAttachment("data/campaign_events.csv").csv({ typed: true });

// Note: you don't have to keep this, but some helpful data exposure to see what we've loaded. 
// NYC geoJSON data
//display(nyc);
// Campaign data (first 10 objects)
//display(results.slice(0,10))
//display(survey.slice(0,10))
//display(events.slice(0,10))
```

```js
// The nyc file is saved in data as a topoJSON instead of a geoJSON. Thats primarily for size reasons -- it saves us 3MB of data. For Plot to render it, we have to convert it back to its geoJSON feature collection. 
const districts = topojson.feature(nyc, nyc.objects.districts);
const nineCriticalDistricts = new Set([104, 105, 106, 102, 101, 302, 406, 411, 503]);
const nineCriticalFeatures = districts.features.filter(d => nineCriticalDistricts.has(d.properties.BoroCD));
//display(districts);
```

```js
// Construct a map of district ID => election margin ((+) for candidate, (-) for opponent)
const marginByCD = new Map();
for (const d of results) {
  marginByCD.set(d.boro_cd, d.votes_candidate - d.votes_opponent);
}
//display(marginByCD);
```

<!-- Reusing the general CSS style that I had in Lab 2 for visual consistency across labs. -->
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

  .answer-box ol {
    max-width: 860px;
    padding-left: 1.4rem;
  }

  .answer-box ol li {
    margin-bottom: 0.6rem;
  }

  .answer-box strong {
    color: #0e7741;
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
    max-width: 860px;
    margin: 0.6rem 0 1.2rem 0;
  }

  .lead {
    font-size: 13pt;
    line-height: 1.55;
    max-width: 860px;
    color: #222;
    margin: 0.8rem 0 1.6rem 0;
  }

  .lead strong {
    color: #0e7741;
  }
</style>

# Lab 3: Mayoral Mystery
#### Kali McLennan

<p class="lead">
The 2024 NYC mayoral candidate lost by <strong style="color: maroon;">31,123 votes</strong>; a 2.2% deficit across 1.36 million ballots cast.
Buried in that headline, the data tells a subtle yet important story: almost the entire deficit is from only <strong>nine community districts</strong>,
while the rest of the city voted in favor of the candidate by a significant margin. The three sections below work through what this means, and what
it suggests should be changed in the next campaign.
</p>

<hr />

## Section 1: Nine Critical Districts

<div class="notes-box">
  The candidate lost the citywide race by <strong style="color: maroon;">31,123 votes</strong>, but these crucial votes are not spread evenly across
  the city. All nine of these critical districts are in the high income tier (median household > $100k). In the rest of the city, the candidate was
  ahead by approximately <strong>98,500</strong> votes. Any plan to win the next race has to either neutralize the effect of these nine districts.
</div>

<div class="chart-wrap">
  <h2>Margin by District</h2>

  <p class="chart-instruction">Each NYC community district is colored by the candidate's net vote margin (blue = candidate won, red = opponent won,
  color intensity scales with margin size). A symmetric diverging color scale is used to highlight how much larger the margins were in the nine
  districts that cost the candidate this election.
  </p>

```js
// Simple rendering of the NYC districts topoJSON
Plot.plot({
  width: 900,
  height: 540,
  color: {
    type: "diverging",
    scheme: "RdBu",
    pivot: 0,
    symmetric: true,
    legend: true
  },
  // this projection is already zoomed into NYC
  projection: {
    domain: districts,
    type: "mercator",
  },
  marks: [
    Plot.geo(districts, {
      fill: d => marginByCD.get(d.properties.BoroCD),
      stroke: "darkgrey",
      strokeWidth: 0.5,
      tip: true,
      title: (d) => {
        const districtID = d.properties.BoroCD;
        const margin = marginByCD.get(districtID);
        if (margin === undefined) {
          return `District ${districtID}\nNo election data found.`;
        }
        return `District ${districtID}\nMargin: ${margin.toLocaleString("en-us")} votes`;
      }
    }),
    Plot.text(nineCriticalFeatures, Plot.centroid({
      text: d => {
        const roundedMargin = Math.round(marginByCD.get(d.properties.BoroCD) / 1000 );
        console.log(d.properties.BoroCD, marginByCD.get(d.properties.BoroCD), roundedMargin);
        return `${roundedMargin}k`
      },
      fill: "white",
      stroke: "black",
      strokeWidth: 3,
      paintOrder: "stroke",
      fontSize: 11,
      fontWeight: 700
    }))
  ]
})
```

</div>

<div class="explainer-area">
I went back and forth on whether or not to include labels for the nine districs that cost the candidate this election, but ultimately
settled on doing so for the sheer purpose of drawing more visual attention. I tried and tried to get annotation lines to move the labels
away from the districts for legibility but just couldnt win the fight. I know it needs some combination of Plot.link() and Plot.centroid(),
but no combination had {x1, y1, x2, y2} in a way that Plot.link() could use. Claude said to construct a map, but I didn't understand the
code and didn't want to use it.
</div>

<div class="answer-box">
  <p>
    These nine high income districts produced an opponent margin of <strong>−129,659 votes</strong> — more than four times the entire citywide
    deficit. These nine districts had far higher turnout and margins than was typical of other districts.. There seems to be no path to victory
    under the current platform with these nine districts aligned against a candidate.
  </p>
  <p>
    The strategic question for the next cycle is therefore not <i>how to win them</i>, but <i>how to get voters in the rest of the city to
    actually go to the polls.</i>.
  </p>
</div>

<hr />

## Section 2: The Middle Class

<div class="notes-box">
  Outside the nine districts that provided the loss, the election was decided in middle income districts. Here, the candidate won 10 of 24 and
  lost 14, most of them by very small margins compared to the critical nine. The middle is where the campaign's Get Out The Vote operation was
  almost entirely absent (611 door knocks per middle income district, vs. 6,938 in low income ones), despite measurable evidence that door
  knocking works <strong>specifically in these middle class neighborhoods</strong>.
</div>

<div class="chart-wrap">
  <h2>GOTV Effort vs. Vote Share, by Income Tier</h2>

  <p class="chart-instruction">
    Each dot is a community district. Horizontal axis: number of GOTV doors knocked. Vertical axis: candidate's share
    of the two-way vote. Dashed rule at 50% marks the win/loss threshold. The middle facet shows the only meaningful within-tier slope — direct
    evidence that doors moved share in the tier the campaign barely worked.
  </p>

```js
function doorKnockTierPlot(tier) {
  const rows = results.filter(d => d.income_category === tier);
 
  return Plot.plot({
      width: 285,
      height: 360,
      marginLeft: 50,
      marginBottom: 45,
      marginTop: 36,
      marginRight: 14,
      title: `${tier} income Districts`,
      x: { label: "Doors knocked →", grid: true, tickFormat: "~s", nice: true },
      y: { label: "Vote margin", grid: true, tickFormat: d3.format("~s"), domain: [-17000, 6500]},
      marks: [
        Plot.frame({ stroke: "#ddd" }),
        Plot.ruleY([0], { stroke: "#999", strokeDasharray: "4 3" }),
        // Best-fit line so each tier's slope (or absence of one) is obvious.
        Plot.linearRegressionY(rows, {
          x: "gotv_doors_knocked",
          y: d => d.votes_candidate - d.votes_opponent,
          stroke: "#0e7741"
        }),
        Plot.dot(rows, {
          x: "gotv_doors_knocked",
          y: d => d.votes_candidate - d.votes_opponent,
          fill: d => (d.votes_candidate - d.votes_opponent) >= 0 ? "#2c7bb6" : "#b2182b",
          stroke: "white",
          strokeWidth: 0.8,
          r: 5,
          title: d => `District ${d.boro_cd}
  Doors knocked: ${d.gotv_doors_knocked}
  Margin: ${(d.votes_candidate - d.votes_opponent)}`,
          tip: true
        })
      ]
    });
  }
```

<!-- I made the door kick effect plots be instantiable by income category because 
     the built in Plot faceting gave all 3 plots a common x domain and it looked bad -->
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem;">
  <div>${doorKnockTierPlot("Low")}</div>
  <div>${doorKnockTierPlot("Middle")}</div>
  <div>${doorKnockTierPlot("High")}</div>
</div>

</div>

<div class="explainer-area">
Faceting here was difficult. The built in Plot facet mechanism wanted to give all 3 sub-plots the same X axis domain.
This looked genuinely bad because it wildly compressed the high and middle class charts. The goal of this plot is
simply to show how districts of each income category responded to the number of doors knocked. This doesnt need a common
X axis domain, and using a common domain would have, I think, reduced the impact of these charts.
</div>

<div class="answer-box">
  <p>
    Door knocking is a frustratingly common part of local elections in New York City. In this election the candidate clearly
    focused their door knocking activity on low income districts. The lowest number of knocks in any low income district was
    5,630, while the highest number of door knocks in any middle or high income district was 984. 
  </p>
  <p>
    The effectiveness of knocking on doors is clearly not consistent. Low income district voters are clearly so well aligned
    with the candidate to begin with that there is no meaningful increase in vote margin when charted against the number of knocks.
  </p>
  <p>
    High income neighborhoods were somewhat responsive to door knocks, with a non-trivial upward trend in votes for the candidate
    correlating with higher numbers of doors knocked. That said, these neighborhoods are so oppositional to the candidate to begin
    with that there is likely no number of door knocks that could turn one of these districts.
  </p>
  <p>
    The critical oversight in this campaign appears to be the low focus of door knocking on middle income districts. These districts
    clearly respond quite well to door knocking, with the candidate <strong style="color: maroon;">losing</strong> every district with
    fewer than ~650 knocks, and <strong>winning</strong> every district with more.
  </p>
</div>

<hr />

## Section 3: The Class Structure of the Platform

<div class="notes-box">
  The clear reading of the survey is <strong style="color: maroon;">"police reform is highly toxic to all voters."</strong> Comparing policy
  alignment by the respondent's <i>district income</i> reveals a key finding: <strong>every other policy is obviously income-segmented</strong>.
  Non-police reform policies are broadly supported by low and middle income voters and rejected by high income voters.
</div>
<div class="notes-box">
    Police reform is uniformly <strong style="color: maroon;">disliked</strong> at across all three income groups, including the candidate's own base. 
</div>

<div class="chart-wrap">
  <h2>Policy Alignment by District Income</h2>

  <p class="chart-instruction">
  Mean alignment with the candidate's policy positions on a 1–5 scale (1 = strongly disagree, 5 = strongly agree), grouped by the survey
  respondent's district income tier. Darker fill = stronger alignment. The police reform row is the only one without an income gradient.
  </p>

```js
// Construct a map from the survey results grouped by the districts income tier
const incomeTierByCD = new Map();
for (const d of results) {
  incomeTierByCD.set(d.boro_cd, d.income_category);
}

const tierOrder = ["Low", "Middle", "High"];

// Map the column names for the alignment fields to prettified display names
const policies = [
  { key: "affordable_housing_alignment", label: "Affordable Housing" },
  { key: "public_transit_alignment",     label: "Public Transit" },
  { key: "childcare_support_alignment",  label: "Childcare Support" },
  { key: "small_business_tax_alignment", label: "Small Business Tax" },
  { key: "police_reform_alignment",      label: "Police Reform" }
];


// Construct an array where each policy is a row containing a unique combination of income, policy, and alignment
const policyAlignment = [];
for (const tier of tierOrder) {
  const respondentsInTier = survey.filter(d => incomeTierByCD.get(d.boro_cd) === tier);
  for (const p of policies) {
    policyAlignment.push({
      tier: tier,
      policy: p.label,
      mean: d3.mean(respondentsInTier, d => d[p.key]).toFixed(1),
    });
  }
}

//display(policyAlignment);
```

```js
Plot.plot({
  width: 640,
  height: 340,
  marginLeft: 175,
  marginRight: 30,
  marginTop: 40,
  marginBottom: 30,
  x: {
    domain: tierOrder,
    label: "District income tier",
    axis: "top",
    tickSize: 0
  },
  y: {
    domain: policies.map(p => p.label),
    reverse: true,
    label: null,
    tickSize: 0
  },
  color: {
    type: "linear",
    scheme: "Greens",
    domain: [1, 5],
    legend: true,
    label: "Mean alignment (1 = strongly disagree, 5 = strongly agree)"
  },
  marks: [
    Plot.cell(policyAlignment, {
      x: "tier",
      y: "policy",
      fill: "mean",
      inset: 1,
      stroke: "lightgrey",
      strokeWidth: 1
    }),
    Plot.text(policyAlignment, {
      x: "tier",
      y: "policy",
      text: d => d.mean,
      fill: "black"
    })
  ]
})
```

</div>

<div class="explainer-area">
A heat map is the logical choice here, as each row represents one item and each column is the value for the item grouped by the income level
of a district. Even after 3 semesters in this program, I still struggle with when it is reasonable to convert discrete values like a Liekert
scale policy alignment question into a continuous mean. 
</div>

<div class="answer-box">
  <p>
    The guidance for the campaign from this chart is very simple: <strong style="color: maroon">Nobody likes your police reform policy</strong>.
  </p>
  <p>
    The candidate is deeply opposed by high income voters in all policy categories. Pandering to the security concerns of high income voters
    does not earn this candidate any higher support in that group. A policing policy that is more aligned with the desires of low and middle
    income voters would likely generate much more support for the candidate in those districts and aid in the previously discussed low turnout
    of those voters in the election.
  </p>
</div>

<hr />

## What This Suggests for the Next Cycle

<div class="answer-box">
  <p>
    The deficit is structural but not insurmountable. Closing it does not require expanding campaigning investment into hostile districts, but
    mobilizing the voters that already exist and broadly support the candidates platform. Five concrete changes follow from the analysis above:
  </p>
  <ol>
    <li><strong>Stop campaigning in the nine high income districts.</strong> The candidate invested more door knocking effort in high income districts than
    they did on middle income, and the high income voters are simply not responsive enough to overcome the very low support level in general.</li>
    <li><strong>Engage with middle income districts.</strong> These districts overwhelmingly align with the candidates policy platform, aside from the
    universally disliked police reform policy. The candidate seems to have assumed they would carry these districts by large numbers. They did carry them,
    but the voter turnout was low and the margins were not large enough to offset the nine high income districts they lost by large margins.</li>
    <li><strong>Recalibrate police reform.</strong> The candidates policy on police reform is unappealing to everyone. In theory, high income districts
    in America tend to be more security minded, but these voters are so opposed to the candidate that this has no meaningful impact. Changing their police
    reform policy may inspire higher turnout from the critical and under-motivated middle class voters.</li>
  </ol>
  <p>
    The candidate doesn't need to become a different candidate. They need to be more informed about who their voters are, who supports their platform, and who
    simply won't.
  </p>
</div>
