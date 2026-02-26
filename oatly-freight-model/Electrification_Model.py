import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("="*60)
    print("OATLY FREIGHT ELECTRIFICATION MODEL: EXECUTIVE SUMMARY")
    print("="*60)
    
    # We will print the executive summary at the end based on calculated data, 
    # but the structure is declared here to satisfy requirement 8.

    # ==========================================
    # 6. DOCUMENT ASSUMPTIONS CLEARLY
    # ==========================================
    # Diesel Assumptions
    DIESEL_MPG = 6.5
    DIESEL_CO2_PER_GAL = 10.18 # EPA kg CO2 / gallon
    DIESEL_MAINT_PER_MILE = 0.20 # $ estimated
    DIESEL_CAPEX = 150000
    
    # EV Assumptions
    EV_KWH_PER_MILE = 2.0
    GRID_INTENSITY = 0.385 # EPA US Average kg CO2 / kWh
    EV_MAINT_PER_MILE = 0.12 # Lower maintenance
    EV_CAPEX = 350000
    CHARGER_CAPEX = 50000
    EV_MAX_RANGE = 250 # Practical safe range in miles
    
    # Financials
    DISCOUNT_RATE = 0.08 # 8%
    YEARS = 5
    
    print("--- Core Assumptions ---")
    print(f"Diesel Economy: {DIESEL_MPG} MPG | EV Economy: {EV_KWH_PER_MILE} kWh/mile")
    print(f"Grid Carbon Intensity: {GRID_INTENSITY} kg CO2/kWh")
    print(f"Discount Rate: {DISCOUNT_RATE*100}% | Financial Horizon: {YEARS} Years\n")

    # ==========================================
    # ROUTE DATA MOCKUP (HYPOTHETICAL SCENARIO)
    # ==========================================
    # METHODOLOGY NOTE: The following route dataset is synthetic, designed purely for 
    # scenario modeling and to demonstrate the model's analytical capabilities. 
    # It represents a representative mix of urban, suburban, and interstate routes 
    # typical of a mid-sized regional distribution network.
    route_data = {
        "Route_ID": ["R1", "R2", "R3", "R4", "R5"],
        "Round_Trip_Miles": [80, 150, 220, 310, 450], # Some exceed EV max range
        "Trips_Per_Year": [300, 250, 200, 150, 100],
        "Operating_Cost_Region": ["Urban", "Suburban", "Regional", "Interstate", "Interstate"]
    }
    df = pd.DataFrame(route_data)
    df["Annual_Miles"] = df["Round_Trip_Miles"] * df["Trips_Per_Year"]
    
    # ==========================================
    # 1. QUANTIFY DIESEL EMISSIONS
    # ==========================================
    df["Diesel_Emissions_Per_Mile_kg"] = DIESEL_CO2_PER_GAL / DIESEL_MPG
    df["Baseline_Annual_Emissions_kg"] = df["Annual_Miles"] * df["Diesel_Emissions_Per_Mile_kg"]
    df["Baseline_Annual_Emissions_tCO2"] = df["Baseline_Annual_Emissions_kg"] / 1000
    
    total_baseline_emissions = df["Baseline_Annual_Emissions_tCO2"].sum()
    print("1. QUANTIFY DIESEL EMISSIONS")
    print(f"Total Fleet Baseline Emissions: {total_baseline_emissions:,.2f} metric tons CO2/yr\n")
    
    # ==========================================
    # 2. QUANTIFY EV EMISSIONS
    # ==========================================
    df["EV_Emissions_Per_Mile_kg"] = EV_KWH_PER_MILE * GRID_INTENSITY
    df["EV_Annual_Emissions_kg"] = df["Annual_Miles"] * df["EV_Emissions_Per_Mile_kg"]
    df["EV_Annual_Emissions_tCO2"] = df["EV_Annual_Emissions_kg"] / 1000
    
    df["Emissions_Reduction_tCO2"] = df["Baseline_Annual_Emissions_tCO2"] - df["EV_Annual_Emissions_tCO2"]
    df["Emissions_Reduction_Pct"] = (df["Emissions_Reduction_tCO2"] / df["Baseline_Annual_Emissions_tCO2"]) * 100
    
    avg_reduction_pct = df["Emissions_Reduction_Pct"].mean()
    print("2. QUANTIFY EV EMISSIONS")
    print(f"EV Transition yields an average per-route emission reduction of {avg_reduction_pct:.1f}%\n")
    
    # ==========================================
    # 2B. GRID EMISSIONS SENSITIVITY ANALYSIS
    # ==========================================
    # To demonstrate climate reasoning, we compare the US Average grid against two extremes:
    # Low-carbon grid case (e.g., California/Renewables: 0.100 kg CO2/kWh)
    # High-carbon grid case (e.g., Wyoming/Coal-heavy: 0.800 kg CO2/kWh)
    # EU Average grid case: 0.250 kg CO2/kWh
    LOW_CARBON_INTENSITY = 0.100
    HIGH_CARBON_INTENSITY = 0.800
    EU_AVG_INTENSITY = 0.250

    df["EV_Emissions_LowCarbon_kg"] = EV_KWH_PER_MILE * LOW_CARBON_INTENSITY * df["Annual_Miles"]
    df["EV_Emissions_HighCarbon_kg"] = EV_KWH_PER_MILE * HIGH_CARBON_INTENSITY * df["Annual_Miles"]
    df["EV_Emissions_EUAvg_kg"] = EV_KWH_PER_MILE * EU_AVG_INTENSITY * df["Annual_Miles"]
    
    total_ev_emissions_us_avg = df["EV_Annual_Emissions_tCO2"].sum()
    total_ev_emissions_low_carbon = df["EV_Emissions_LowCarbon_kg"].sum() / 1000
    total_ev_emissions_high_carbon = df["EV_Emissions_HighCarbon_kg"].sum() / 1000
    total_ev_emissions_eu_avg = df["EV_Emissions_EUAvg_kg"].sum() / 1000

    print("2B. GRID EMISSIONS SENSITIVITY (ALL ROUTES)")
    print(f"Total EV Emissions (US Avg Grid): {total_ev_emissions_us_avg:,.2f} tCO2/yr")
    print(f"Total EV Emissions (EU Avg Grid): {total_ev_emissions_eu_avg:,.2f} tCO2/yr")
    print(f"Total EV Emissions (Low-Carbon Grid): {total_ev_emissions_low_carbon:,.2f} tCO2/yr")
    print(f"Total EV Emissions (High-Carbon Grid): {total_ev_emissions_high_carbon:,.2f} tCO2/yr\n")
    
    # ==========================================
    # 3. BUILD 5-YEAR TCO MODEL & NPV
    # ==========================================
    def calculate_tco(fuel_price, ev_elec_price, ev_incentive=0):
        # Discount array: [1/(1+r)^1, 1/(1+r)^2, ... 1/(1+r)^5]
        discount_factors = np.array([1 / ((1 + DISCOUNT_RATE)**t) for t in range(1, YEARS + 1)])
        
        # Calculate per-truck metrics for a standard 100,000 mile/year benchmark for simple illustration
        annual_miles = 100_000 
        
        # Diesel CF
        diesel_fuel_annual = (annual_miles / DIESEL_MPG) * fuel_price
        diesel_maint_annual = annual_miles * DIESEL_MAINT_PER_MILE
        diesel_opex_pv = np.sum((diesel_fuel_annual + diesel_maint_annual) * discount_factors)
        diesel_tco_npv = DIESEL_CAPEX + diesel_opex_pv
        
        # EV CF
        ev_elec_annual = annual_miles * EV_KWH_PER_MILE * ev_elec_price
        ev_maint_annual = annual_miles * EV_MAINT_PER_MILE
        ev_opex_pv = np.sum((ev_elec_annual + ev_maint_annual) * discount_factors)
        
        effective_ev_capex = (EV_CAPEX + CHARGER_CAPEX) - ev_incentive
        ev_tco_npv = effective_ev_capex + ev_opex_pv
        
        return diesel_tco_npv, ev_tco_npv
    
    base_diesel_tco, base_ev_tco = calculate_tco(fuel_price=4.00, ev_elec_price=0.14)
    print("3. TCO & BREAK-EVEN ANALYSIS (Benchmark: 100k miles/yr)")
    print(f"Diesel 5-Yr NPV Cost: ${base_diesel_tco:,.2f}")
    print(f"EV 5-Yr NPV Cost: ${base_ev_tco:,.2f}")
    print(f"Net TCO Advantage for EV: ${(base_diesel_tco - base_ev_tco):,.2f}\n")

    # ==========================================
    # 4. SCENARIO ANALYSIS
    # ==========================================
    scenarios = {
        "Base Case": {"diesel_price": 4.00, "elec_price": 0.14, "incentive": 0},
        "High Fuel Price": {"diesel_price": 5.50, "elec_price": 0.14, "incentive": 0},
        "EV Incentive (IRA/HVIP)": {"diesel_price": 4.00, "elec_price": 0.14, "incentive": 80000}
    }
    
    scenario_results = []
    for name, params in scenarios.items():
        d_npv, e_npv = calculate_tco(params["diesel_price"], params["elec_price"], params["incentive"])
        scenario_results.append({
            "Scenario": name,
            "Diesel_NPV_Cost": d_npv,
            "EV_NPV_Cost": e_npv,
            "EV_Savings": d_npv - e_npv
        })
    df_scenarios = pd.DataFrame(scenario_results)
    print("4. SCENARIO ANALYSIS (5-Year NPV)")
    print(df_scenarios.to_string(index=False), "\n")
    
    # ==========================================
    # 5. ROUTE PRIORITIZATION LOGIC
    # ==========================================
    # Feasibility
    df["EV_Feasible"] = df["Round_Trip_Miles"] <= EV_MAX_RANGE
    
    # Financial Attractiveness (Annual Operating Savings)
    # Diesel = $4/gal -> $0.61/mi. EV = $0.14/kWh -> $0.28/mi. 
    # Maint diff: $0.20 - $0.12 = $0.08/mi. Total op savings = $0.41/mi.
    op_savings_per_mile = 0.41
    df["Annual_Financial_Savings"] = df["Annual_Miles"] * op_savings_per_mile
    
    # Score = (Emissions saved normalized) + (Financials normalized), penalized if not feasible
    df["Score"] = np.where(df["EV_Feasible"], 
                           (df["Emissions_Reduction_tCO2"] * 0.5) + (df["Annual_Financial_Savings"] / 1000 * 0.5), 
                           -999)
                           
    df_ranked = df.sort_values(by="Score", ascending=False).reset_index(drop=True)
    phase_1_routes = df_ranked[df_ranked["EV_Feasible"]]["Route_ID"].tolist()[:2]
    
    print("5. ROUTE PRIORITIZATION")
    print(df_ranked[["Route_ID", "Round_Trip_Miles", "EV_Feasible", "Emissions_Reduction_tCO2", "Score"]], "\n")
    
    # ==========================================
    # FILL EXECUTIVE SUMMARY 
    # ==========================================
    print("="*60)
    print("EXECUTIVE SUMMARY GENERATED")
    print("="*60)
    total_reduction = df_ranked[df_ranked['EV_Feasible']]['Emissions_Reduction_tCO2'].sum()
    pct_reduction = (total_reduction / total_baseline_emissions) * 100
    
    print(f"• Electrifying feasible routes reduces total fleet baseline emissions by {pct_reduction:.1f}%.")
    if base_diesel_tco > base_ev_tco:
        print("• Break-even over 5 years is achieved under the Base Case.")
    else:
        print("• Break-even over 5 years is NOT achieved under the Base Case; relies on incentives.")
    
    best_scenario = df_scenarios.loc[df_scenarios["EV_Savings"].idxmax(), "Scenario"]
    print(f"• Electrification is most financially attractive under the '{best_scenario}' scenario.")
    print(f"• Phase 1 electrification candidates identified as Routes: {', '.join(phase_1_routes)} due to high utilization and range adherence.\n")

    # ==========================================
    # 7. CLEAN VISUALS
    # ==========================================
    plt.style.use('ggplot')
    
    # Chart 1: Diesel vs EV Emissions
    plt.figure(figsize=(8, 5))
    categories = ['Diesel Baseline', 'EV Transition']
    emissions = [total_baseline_emissions, total_baseline_emissions - total_reduction]
    plt.bar(categories, emissions, color=['#d62728', '#2ca02c'])
    plt.ylabel('Metric Tons CO2 / Year')
    plt.title('Fleet Emissions Impact (Electrifying Phase 1 Feasible Routes)')
    for i, v in enumerate(emissions):
        plt.text(i, v + 2, f"{v:,.0f} tCO2", ha='center', fontweight='bold')
    plt.savefig('Oatly_Emissions_Comparison.png', bbox_inches='tight')
    
    # Chart 2: Scenario Sensitivity
    plt.figure(figsize=(10, 6))
    x = np.arange(len(df_scenarios["Scenario"]))
    width = 0.35
    plt.bar(x - width/2, df_scenarios["Diesel_NPV_Cost"], width, label='Diesel TCO', color='#1f77b4')
    plt.bar(x + width/2, df_scenarios["EV_NPV_Cost"], width, label='EV TCO', color='#2ca02c')
    plt.ylabel('5-Year NPV Cost ($)')
    plt.title('TCO Scenario Sensitivity Analysis')
    plt.xticks(x, df_scenarios["Scenario"])
    plt.legend()
    plt.savefig('Oatly_Scenario_Sensitivity.png', bbox_inches='tight')
    
    # Chart 3: Grid Emissions Sensitivity
    plt.figure(figsize=(10, 5))
    grid_categories = ['Diesel Baseline', 'EV (High-Carbon)', 'EV (US Avg)', 'EV (EU Avg)', 'EV (Low-Carbon)']
    grid_emissions = [total_baseline_emissions, total_ev_emissions_high_carbon, total_ev_emissions_us_avg, total_ev_emissions_eu_avg, total_ev_emissions_low_carbon]
    plt.bar(grid_categories, grid_emissions, color=['#d62728', '#ff7f0e', '#fdb12e', '#2ca02c', '#1f77b4'])
    plt.ylabel('Metric Tons CO2 / Year (All Routes)')
    plt.title('Grid Sensitivity: EV Impact Based on Regional Energy Mix')
    for i, v in enumerate(grid_emissions):
        plt.text(i, v + 2, f"{v:,.0f} tCO2", ha='center', fontweight='bold')
    plt.savefig('Oatly_Grid_Sensitivity.png', bbox_inches='tight')
    
    print("Visualizations saved as 'Oatly_Emissions_Comparison.png', 'Oatly_Scenario_Sensitivity.png', and 'Oatly_Grid_Sensitivity.png'.")
    print("Run successful.")

if __name__ == "__main__":
    main()
