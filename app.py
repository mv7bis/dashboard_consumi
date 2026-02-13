import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import os

st.title("Registro Consumi e Produzione Elettrica")

# Nome del file CSV
FILE = "dati.csv"

# Se il file non esiste, crealo con intestazioni
if not os.path.exists(FILE):
    df_init = pd.DataFrame(columns=["data", "consumo_kwh", "produzione_kwh", "delta_kwh"])
    df_init.to_csv(FILE, index=False)

# Carica i dati esistenti
df = pd.read_csv(FILE)

st.header("Inserisci nuovi dati")

# Input utente
data_input = st.date_input("Data", value=date.today())
consumo = st.number_input("Consumo elettrico (kWh)", min_value=0.0, step=0.1)
produzione = st.number_input("Produzione elettrica (kWh)", min_value=0.0, step=0.1)

if st.button("Salva dati"):
    delta = consumo - produzione

    nuovo_record = pd.DataFrame({
        "data": [str(data_input)],
        "consumo_kwh": [consumo],
        "produzione_kwh": [produzione],
        "delta_kwh": [delta]
    })

    df = pd.concat([df, nuovo_record], ignore_index=True)
    df.to_csv(FILE, index=False)

    st.success("Dati salvati correttamente!")

st.header("Visualizzazione dati")

if len(df) == 0:
    st.info("Nessun dato presente. Inserisci almeno un record.")
else:
    # Ordina per data
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    st.dataframe(df)
    
# Grafico con barre affiancate + linee di riferimento + asse X a 0
fig, ax = plt.subplots(figsize=(10, 5))

x = range(len(df))
width = 0.18  # barre più strette per creare spazio

offset = 0.22  # distanza laterale tra le barre

# Barre affiancate con distanza
ax.bar([i - offset for i in x], df["consumo_kwh"], width=width, color="red", label="Consumo")
ax.bar(x, df["produzione_kwh"], width=width, color="green", label="Produzione")
ax.bar([i + offset for i in x], df["delta_kwh"], width=width, color="yellow", label="Delta")

# Linee di riferimento
ax.axhline(0, color="black", linewidth=0.8)  # asse X continuo
ax.axhline(5, color="gray", linestyle="-", linewidth=0.7, alpha=0.7)
ax.axhline(10, color="gray", linestyle="-", linewidth=0.7, alpha=0.7)

# Etichette asse X
ax.set_xticks(x)
ax.set_xticklabels(df["data"].dt.strftime("%Y-%m-%d"), rotation=45, ha="right")

ax.set_ylabel("kWh")
ax.set_title("Consumo, Produzione e Delta per Giorno")
ax.legend()

st.pyplot(fig)
