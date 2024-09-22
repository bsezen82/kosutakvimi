# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# Veri Hazırlığı: Trail ve Road yarışlarını filtrelemek
race_data = {
    "Race Name": [
        "Bodrum Yarı Maratonu", "Gebze Kurtuluş Koşusu", "Runkara Yarı Maratonu",
        "Salomon Cappadocia Ultra Trail", "Büyükada Yarı Maratonu", "Tarsus Yarı Maratonu",
        "Antalya 29 Ekim Koşusu", "İstanbul Maratonu", "Kaş Yarımadaton", 
        "Babadağ Ultra Trail", "Mersin Maratonu", "Antalya Ultra Maratonu", 
        "Büyük Atatürk Koşusu", "Sagalassos Sky Ultra", "Marmaris Ultra Trail", 
        "Ida Ultra", "Geyik Koşuları", "Varda Ultra Trail", 
        "Tantalos Trail Koşusu"
    ],
    "Race Type": [
        "Road Race", "Road Race", "Road Race", "Trail Run", "Road Race", 
        "Road Race", "Road Race", "Road Race", "Trail Run", 
        "Trail Run", "Road Race", "Trail Run", 
        "Road Race", "Trail Run", "Trail Run", 
        "Trail Run", "Trail Run", "Trail Run", 
        "Trail Run"
    ],
    "Distances": [
        "5K, 10K, 21K", "10K", "5K, 10K, 21K", "38K, 63K, 119K", "5K, 10K, 21K", 
        "5K, 10K, 21K", "5K, 10K", "42K, 15K, 8K", "6K, 12K, 21K", 
        "5K, 14K, 24K, 60K", "42K, 15K", "30K, 60K, 120K", 
        "10K", "30K, 60K, 110K", "25K, 50K, 80K", 
        "15K, 30K, 60K, 90K", "4K, 12K, 24K", "50K, 80K, 110K", 
        "30K, 60K"
    ],
    "Date": [
        "2024-10-06", "2024-10-12", "2024-10-13", "2024-10-19", "2024-10-20", 
        "2024-10-20", "2024-10-29", "2024-11-03", "2024-10-26", 
        "2024-10-18", "2024-12-15", "2024-12-28", 
        "2024-12-29", "2024-11-08", "2024-11-15", 
        "2024-11-29", "2024-11-24", "2024-11-09", 
        "2024-11-09"
    ],
    "City": [
        "Muğla", "Kocaeli", "Ankara", "Nevşehir", "İstanbul", 
        "Mersin", "Antalya", "İstanbul", "Antalya", 
        "Muğla", "Mersin", "Antalya", 
        "Ankara", "Burdur", "Muğla", 
        "Balıkesir", "İstanbul", "Adana", 
        "İzmir"
    ],
    "Website": [
        "https://www.bodrumyarimaratonu.com", "https://www.gebzekurtuluskosusu.com", 
        "https://www.runkara.com.tr", "https://www.cappadociaultratrail.com", 
        "https://www.buyukadayarimaratonu.com", "https://www.tarsusyarimaratonu.com", 
        "https://www.antalya29ekimkosusu.com", "https://www.istanbulmarathon.org", 
        "https://www.kasyarimadaton.com", "https://www.babadagultratrail.com", 
        "https://www.mersinmarathon.com", "https://www.antalyaultramaratonu.com", 
        "https://www.buyukataturkkosusu.com", "https://www.sagalassosskyultra.com", 
        "https://www.marmarisultratrail.com", "https://www.idaultra.com", 
        "https://www.geyikkosulari.com", "https://www.vardaultratrail.com", 
        "https://www.tantalostrail.com"
    ]
}

df_races = pd.DataFrame(race_data)
df_races["Date"] = pd.to_datetime(df_races["Date"])

# Helper function to extract minimum and maximum distances
def extract_min_max_distances(distance_series):
    min_distances = []
    max_distances = []
    for distances in distance_series:
        dist_list = [int(d[:-1]) for d in distances.split(', ')]
        min_distances.append(min(dist_list))
        max_distances.append(max(dist_list))
    return min_distances, max_distances

df_races["Min Distance"], df_races["Max Distance"] = extract_min_max_distances(df_races["Distances"])

# Function to create clickable links in the dataframe
def make_clickable(link):
    return f'<a href="{link}" target="_blank">{link}</a>'

df_races['Website'] = df_races['Website'].apply(make_clickable)

# Streamlit Uygulaması
st.title("2024 Türkiye Koşu Yarışları")
st.write("Aşağıdaki filtreleri kullanarak istediğiniz yarışları bulun.")

# Filtreleri merkezi olarak yerleştirmek için Streamlit formu kullanıyoruz
with st.form("filters"):
    st.subheader("Filtreleme Seçenekleri")
    
    # Yarış Türü ve Şehir Filtreleme Seçenekleri (Başlangıçta boş)
    selected_type = st.multiselect(
        "Yarış Türü Seçiniz", options=df_races["Race Type"].unique(), default=[]
    )
    selected_city = st.multiselect(
        "Şehir Seçiniz", options=df_races["City"].unique(), default=[]
    )

    # Mesafe Aralığı Filtreleme
    min_distance, max_distance = st.slider(
        "Mesafe Aralığını Seçiniz (km)", 
        min_value=int(df_races["Min Distance"].min()), 
        max_value=int(df_races["Max Distance"].max()), 
        value=(int(df_races["Min Distance"].min()), int(df_races["Max Distance"].max()))
    )

    # Tarih Aralığı Filtreleme
    start_date, end_date = st.date_input(
        "Tarih Aralığını Seçiniz",
        [df_races["Date"].min(), df_races["Date"].max()],
        min_value=df_races["Date"].min(),
        max_value=df_races["Date"].max()
    )

    # "Yarışları Listele" Butonu
    submit_button = st.form_submit_button(label="Yarışları Listele")

# Eğer butona basılmışsa, filtreleri uygula ve sonuçları göster
if submit_button:
    # Filtreleme İşlemi
    filtered_df = df_races[
        (df_races["Race Type"].isin(selected_type) if selected_type else [True] * len(df_races)) & 
        (df_races["City"].isin(selected_city) if selected_city else [True] * len(df_races)) & 
        (df_races["Min Distance"] >= min_distance) & 
        (df_races["Max Distance"] <= max_distance) &
        (df_races["Date"] >= pd.to_datetime(start_date)) & 
        (df_races["Date"] <= pd.to_datetime(end_date))
    ]

    # Sonuçları Gösterme
    st.write(f"Toplam {len(filtered_df)} yarış bulundu.")
    # Index olmadan tabloyu göster
    st.write(filtered_df.reset_index(drop=True)[['Race Name', 'Date', 'Distances', 'Website']].to_html(escape=False, index=False), unsafe_allow_html=True)
