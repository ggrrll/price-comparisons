import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Confronto Tariffe Gas Naturale", page_icon="🔥", layout="wide")

st.title("🔥 Confronto Tariffe Gas Naturale - Mercato Italiano")
st.markdown("Confronta diverse tariffe di gas naturale per clienti privati")

# Sidebar for adding tariffs
st.sidebar.header("Aggiungi Tariffe")

# Initialize session state for tariffs
if 'tariffs' not in st.session_state:
    st.session_state.tariffs = [
        {"name": "EniPlenitude", "fixed": 144.0, "variable": 1.07, "color": "#FF6B6B"},
        {"name": "Acea", "fixed": 72, "variable": 0.75, "color": "#4ECDC4"},
        # {"name": "Tariffa C", "fixed": 150.0, "variable": 0.75, "color": "#45B7D1"},
    ]

# Form to add new tariff
with st.sidebar.form("add_tariff"):
    st.subheader("Nuova Tariffa")
    tariff_name = st.text_input("Nome Tariffa", value=f"Tariffa {len(st.session_state.tariffs) + 1}")
    fixed_rate = st.number_input("Quota Fissa (€/anno)", min_value=0.0, value=100.0, step=10.0)
    variable_rate = st.number_input("Prezzo Variabile (€/m³)", min_value=0.0, value=0.85, step=0.01, format="%.3f")
    color = st.color_picker("Colore", value="#95E1D3")
    
    submitted = st.form_submit_button("Aggiungi Tariffa")
    if submitted:
        st.session_state.tariffs.append({
            "name": tariff_name,
            "fixed": fixed_rate,
            "variable": variable_rate,
            "color": color
        })
        st.rerun()

# Display and edit existing tariffs
st.sidebar.header("Tariffe Esistenti")
for i, tariff in enumerate(st.session_state.tariffs):
    with st.sidebar.expander(f"{tariff['name']}"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Quota Fissa:** €{tariff['fixed']:.2f}/anno")
            st.write(f"**Prezzo Variabile:** €{tariff['variable']:.3f}/m³")
        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.tariffs.pop(i)
                st.rerun()

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Confronto Grafico")
    
    # Consumption range slider
    max_consumption = st.slider(
        "Consumo Massimo (m³/anno)",
        min_value=500,
        max_value=5000,
        value=2000,
        step=100
    )
    
    # Calculate costs for different consumption levels
    consumption_range = np.linspace(0, max_consumption, 100)
    
    # Create plotly figure
    fig = go.Figure()
    
    for tariff in st.session_state.tariffs:
        costs = tariff['fixed'] + tariff['variable'] * consumption_range
        fig.add_trace(go.Scatter(
            x=consumption_range,
            y=costs,
            mode='lines',
            name=tariff['name'],
            line=dict(color=tariff['color'], width=3),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Consumo: %{x:.0f} m³<br>' +
                         'Costo Totale: €%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    fig.update_layout(
        xaxis_title="Consumo Annuo (m³/y)",
        yaxis_title="Costo Totale Annuo (€/y)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💡 Calcolo Personalizzato")
    
    your_consumption = st.number_input(
        "Il tuo consumo annuo (m³)",
        min_value=0,
        max_value=10000,
        value=1200,
        step=50
    )
    
    st.markdown("---")
    st.markdown("### Costi Stimati")
    
    # Calculate and display costs for user's consumption
    results = []
    for tariff in st.session_state.tariffs:
        total_cost = tariff['fixed'] + tariff['variable'] * your_consumption
        results.append({
            "Tariffa": tariff['name'],
            "Costo Totale": f"€{total_cost:.2f}",
            "Quota Fissa": f"€{tariff['fixed']:.2f}",
            "Consumo": f"€{tariff['variable'] * your_consumption:.2f}",
            "_sort": total_cost
        })
    
    # Sort by total cost
    results_sorted = sorted(results, key=lambda x: x['_sort'])
    
    for i, result in enumerate(results_sorted):
        if i == 0:
            st.success(f"🏆 **{result['Tariffa']}** - {result['Costo Totale']}")
        else:
            st.info(f"**{result['Tariffa']}** - {result['Costo Totale']}")

# Additional info section
st.markdown("---")
st.subheader("📋 Tabella Riepilogativa")

# Create comparison table
table_data = []
consumption_levels = [500, 1000, 1500, 2000, 2500]

for tariff in st.session_state.tariffs:
    row = {
        "Tariffa": tariff['name'],
        "Quota Fissa (€/anno)": f"€{tariff['fixed']:.2f}",
        "Prezzo (€/m³)": f"€{tariff['variable']:.3f}",
    }
    for consumption in consumption_levels:
        total = tariff['fixed'] + tariff['variable'] * consumption
        row[f"{consumption} m³"] = f"€{total:.2f}"
    table_data.append(row)

df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("💡 **Nota:** I prezzi indicati sono puramente indicativi. Verifica sempre le condizioni contrattuali complete prima di sottoscrivere un contratto.")


if __name__ == "__main__":
    pass
