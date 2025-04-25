import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solidaritätsmodell", layout="centered")

st.title("💸 Solidaritätsmodell in der Krankenversicherung")
st.markdown("""
Passe den Solidaritätsfaktor \\( α in [0, 1] \\) an. 
- Bei \\( α = 0 \\): Prämien sind rein risikobasiert (fair).
- Bei \\( α = 1 \\): Alle zahlen denselben Beitrag (maximale Solidarität).
""")

# Einstellungen
fair_premiums = {x: (x / 6) * 50000 for x in range(1, 7)}
equal_premium = sum(fair_premiums.values()) / 6

alpha = st.slider("Solidaritätsfaktor α", 0.0, 1.0, 0.5, 0.01)

data = []
for x in range(1, 7):
    fair = fair_premiums[x]
    solidar = (1 - alpha) * fair + alpha * equal_premium
    delta = solidar - fair
    expected_cost = fair  # da fair = erwarteter Schaden
    gain_or_loss = solidar - expected_cost
    data.append({
        "Typ": x,
        "Faire Prämie (€)": fair,
        "Solidarische Prämie (€)": solidar,
        "Delta zur fairen Prämie (€)": delta,
        "Gewinn/Verlust für Versicherung (€)": gain_or_loss
    })

df = pd.DataFrame(data)

st.subheader("📊 Prämienvergleich")
st.dataframe(df.style.format("{:,.2f}"))

st.subheader("📈 Visualisierung")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Balkendiagramm Prämien
ax[0].bar(df["Typ"] - 0.2, df["Faire Prämie (€)"], width=0.4, label="Fair")
ax[0].bar(df["Typ"] + 0.2, df["Solidarische Prämie (€)"], width=0.4, label="Solidarisch")
ax[0].set_title("Prämien nach Typ")
ax[0].set_xlabel("Typ")
ax[0].set_ylabel("Prämie (€)")
ax[0].legend()

# Balkendiagramm Gewinn/Verlust
ax[1].bar(df["Typ"], df["Gewinn/Verlust für Versicherung (€)"], color='orange')
ax[1].set_title("Versicherungsgewinn/-verlust nach Typ")
ax[1].set_xlabel("Typ")
ax[1].set_ylabel("Gewinn/Verlust (€)")

st.pyplot(fig)

st.subheader("📘 Gesamtauswertung")
total_gain = df["Gewinn/Verlust für Versicherung (€)"].sum()
st.write(f"**Gesamter Gewinn/Verlust der Versicherung über alle Typen:** €{total_gain:,.2f}")

if abs(total_gain) < 1e-3:
    st.success("✅ Die Versicherung bleibt insgesamt kostendeckend!")
else:
    st.warning("⚠️ Die Versicherung macht insgesamt Gewinn oder Verlust.")
