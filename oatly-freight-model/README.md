# Oatly Freight Electrification Model (Phase 1 Portfolio)

## Executive Summary
This project presents an analytical framework assessing the financial feasibility and environmental impact of transitioning a heavy-duty freight fleet from diesel to battery electric vehicles (BEVs). Designed for strategic planning, the model quantifies carbon emissions reductions and projects 5-year Total Cost of Ownership (TCO) across different financial scenarios. This analysis empowers logistics decision-makers to identify routes most viable for Phase 1 electrification and understand the role of energy markets on return on investment.

## The Business Problem
Decarbonizing logistics operations is a major challenge due to the high upfront capital expenditures of EV trucks, charging infrastructure limitations, and range anxiety. To justify investment, businesses must evaluate precisely where EVs break even relative to internal combustion engines over their operational lifespans and which geographic routes accommodate current BEV battery capabilities. This model formalizes that assessment through quantitative analytics.

## Methodology & Route Analysis
To demonstrate the model's analytical capabilities, I evaluated a synthetic logistics dataset consisting of representative urban, suburban, and regional routes. The script determines operational feasibility based on round-trip distances compared to a conservative practical EV range limit. Viable routes are then ranked using a custom weighted scoring schematic that incorporates both estimated emission savings and direct financial operational savings (fuel displacement and lower maintenance costs).

**Note:** *The route dataset is entirely hypothetical and utilized purely for scenario modeling.*

## Scenario and TCO Analysis
Because future energy prices and government interventions are uncertain, the model evaluates financial viability through three scenarios: a Base Case, a High Fuel Price scenario, and an EV Incentive scenario (e.g., IRA or HVIP grants). The findings clearly demonstrate that while EV operating costs are significantly lower per mile, breaking even over a tight 5-year horizon often relies heavily on upfront incentives due to high vehicle and charging infrastructure capex.

## Core Modeling Assumptions
- **Diesel Performance:** Baseline trucks operate at 6.5 MPG with maintenance costs estimated at $0.20/mile. The capital cost per diesel vehicle is assumed to be $150,000.
- **EV Performance:** EVs operate at an efficiency of 2.0 kWh/mile with a practical safe operational range of 250 miles. Their maintenance costs are estimated lower at $0.12/mile. Upfront capex for EVs is modeled at $350,000 with an additional $50,000 allocated for charging assets.
- **Financial Parameters:** The framework applies an 8% discount rate over a 5-year NPV horizon.

## Emissions and Grid Sensitivity
A critical aspect of an EV transition's localized climate impact is the electricity grid's energy mix. The model quantifies emissions based on the EPA's US Average grid intensity (0.385 kg CO2/kWh). To provide deeper climate reasoning, a grid sensitivity analysis compares this baseline against a Low-Carbon Grid Case (reflective of renewable-heavy regions like California at 0.100 kg CO2/kWh) and a High-Carbon Grid Case (reflective of coal-heavy regions like Wyoming at 0.800 kg CO2/kWh), clarifying how energy provenance directly governs transition efficacy.

## Limitations
This portfolio piece is a demonstrational framework. Its limitations include the reliance on synthesized route data rather than actual telemetry, the exclusion of dynamic variables such as route topography and varying payloads, and the omission of complex tax mechanisms, insurance premiums, and battery degradation curves. It serves as a high-level strategic roadmap rather than a definitive operational deployment plan.
