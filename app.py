from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Fungsi untuk memuat dataset
@ st.cache_data
def load_data():
    """
    Memuat dataset dari file Excel.
    Pastikan file 'tracer_final.xlsx' berada di direktori yang benar.
    """
    return pd.read_excel('tracer_final.xlsx')

# Fungsi untuk menerapkan filter pada dataset
def apply_filters(data, tahun_lulus, prodi):
    """
    Menerapkan filter berdasarkan tahun lulus dan program studi.
    
    Args:
        data (DataFrame): Dataset utama.
        tahun_lulus (str): Tahun lulus yang dipilih.
        prodi (str): Program studi yang dipilih.
    
    Returns:
        DataFrame: Dataset yang telah difilter.
    """
    if tahun_lulus != "Semua":
        data = data[data["TahunLulus"] == tahun_lulus]
    if prodi != "Semua":
        data = data[data["Prodi"] == prodi]
    return data

# Memuat dataset
data = load_data()

# Sidebar untuk filter
st.sidebar.title("Filter Dashboard")
tahun_lulus_filter = st.sidebar.selectbox(
    "Pilih Tahun Lulus", 
    options=["Semua"] + sorted(data["TahunLulus"].unique().tolist())
)
prodi_filter = st.sidebar.selectbox(
    "Pilih Prodi", 
    options=["Semua"] + sorted(data["Prodi"].unique().tolist())
)

# Terapkan filter
filtered_data = apply_filters(data, tahun_lulus_filter, prodi_filter)

# Judul Dashboard
st.title("Dashboard Tracer Study")

# Penanganan jika data setelah difilter kosong
if filtered_data.empty:
    st.info("Data tidak ditemukan dengan filter yang diterapkan. Silakan ubah filter Anda.")
else:
    # Baris 1: Jumlah Responden
    jumlah_pengisi = filtered_data.shape[0]
    with st.container(border=True):
        st.metric(label="Total Responden", value=f"{jumlah_pengisi}")

    # Baris 2: Distribusi Alumni Berdasarkan Status Pekerjaan dan Jenis Perusahaan
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('###### Distribusi Alumni Berdasarkan Status Pekerjaan')
        if "StatusPekerjaan" in filtered_data.columns:
            status_counts = filtered_data['StatusPekerjaan'].value_counts()
            if not status_counts.empty:
                fig = px.pie(
                    names=status_counts.index,
                    values=status_counts.values,
                    hole=0.4
                )
                fig.update_layout(
                    legend=dict(
                        orientation="v",  # Vertikal legend
                        yanchor="bottom",  # Menempatkan legend di bawah chart
                        y=-0.6,  # Mengatur jarak legenda ke bawah
                        xanchor="center",  # Centering the legend horizontally
                        x=0.5
                    ),
                    width=290,
                    height=550  # Mengubah tinggi chart
                )
                st.plotly_chart(fig)
            else:
                st.info("Data tidak tersedia untuk visualisasi ini.")
        else:
            st.info("Kolom 'StatusPekerjaan' tidak ditemukan di dataset.")

    with col2:
        st.markdown('###### Distribusi Alumni Berdasarkan Jenis Perusahaan')
        if "JenisPerusahaan" in filtered_data.columns:
            jenis_counts = filtered_data['JenisPerusahaan'].value_counts()
            if not jenis_counts.empty:
                fig = px.pie(
                    names=jenis_counts.index,
                    values=jenis_counts.values,
                    hole=0.4
                )
                fig.update_layout(
                    legend=dict(
                        orientation="v",  # Vertikal legend
                        yanchor="bottom",  # Menempatkan legend di bawah chart
                        y=-0.6,  # Mengatur jarak legenda ke bawah
                        xanchor="center",  # Centering the legend horizontally
                        x=0.5  # Menempatkan legenda di tengah secara horizontal
                    ),
                    width=290,
                    height=550  # Mengubah tinggi chart
                )
                st.plotly_chart(fig) 
            else:
                st.info("Data tidak tersedia untuk visualisasi ini.")
        else:
            st.info("Kolom 'JenisPerusahaan' tidak ditemukan di dataset.")

    # Baris 3: Distribusi Alumni Berdasarkan Daerah Tempat Kerja
    provinsi_indonesia = [
        "JAWA BARAT", "DKI JAKARTA", "BANTEN", "JAWA TENGAH", "JAWA TIMUR",
        "DI YOGYAKARTA", "SUMATERA SELATAN", "SULAWESI UTARA", "MALUKU", "RIAU",
        "LAMPUNG", "SUMATERA BARAT", "KALIMANTAN TENGAH", 
        "SULAWESI TENGAH", "SULAWESI TENGGARA", "KEPULAUAN BANGKA BELITUNG", 
        "KALIMANTAN TIMUR", "NUSA TENGGARA TIMUR", "KALIMANTAN UTARA", 
        "SUMATERA UTARA", "BALI", "SULAWESI SELATAN"
    ]
    daerah_counts = filtered_data['DaerahTempatKerja'].value_counts()
    if not daerah_counts.empty:
        daerah_df = daerah_counts.reset_index()
        daerah_df.columns = ['Daerah', 'Jumlah']

        daerah_indonesia = daerah_df[daerah_df['Daerah'].isin(provinsi_indonesia)]
        daerah_asing = daerah_df[~daerah_df['Daerah'].isin(provinsi_indonesia)]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("###### Distribusi Alumni Bekerja di Dalam Negeri")
            if not daerah_indonesia.empty:
                st.dataframe(
                    daerah_indonesia,
                    hide_index=True,  # Menyembunyikan indeks
                    column_config={
                        "Daerah": st.column_config.TextColumn(
                            "Provinsi"  # Header kolom teks
                        ),
                        "Jumlah": st.column_config.ProgressColumn(
                            "Jumlah Alumni",  # Header kolom progress
                            format="%d",  # Format sebagai bilangan bulat
                            min_value=0,  # Nilai minimum
                            max_value=max(daerah_indonesia['Jumlah']),  # Nilai maksimum
                        ),
                    }
                )
            else:
                st.info("Data tidak tersedia untuk visualisasi.")


        with col2:
            st.markdown("###### Distribusi Alumni Bekerja di Luar Negeri")
            if not daerah_asing.empty:
                st.dataframe(
                    daerah_asing,
                    hide_index=True,  # Menyembunyikan indeks
                    column_config={
                        "Daerah": st.column_config.TextColumn(
                            "Negara"  # Header kolom teks
                        ),
                        "Jumlah": st.column_config.ProgressColumn(
                            "Jumlah Alumni",  # Header kolom progress
                            format="%d",  # Format sebagai bilangan bulat
                            min_value=0,  # Nilai minimum
                            max_value=max(daerah_asing['Jumlah']),  # Nilai maksimum
                        ),
                    }
                )
            else:
                st.info("Data tidak tersedia untuk visualisasi.")
    else:
        st.info("Data tidak tersedia untuk visualisasi daerah.")

    # Baris 4: Statistik Pendapatan
    col1, col2 = st.columns(2)

    with col1:
        pendapatan_tertinggi = filtered_data["PendapatanPerbulan"].max()
        with st.container(border=True):
            st.metric(
                label="Pendapatan Tertinggi",
                value=f"Rp {pendapatan_tertinggi:,.0f}" if not np.isnan(pendapatan_tertinggi) else "Data Tidak Tersedia"
            )

    with col2:
        rata_rata_pendapatan = filtered_data["PendapatanPerbulan"].mean()
        with st.container(border=True):
            st.metric(
                label="Rata-rata Pendapatan",
                value=f"Rp {rata_rata_pendapatan:,.0f}" if not np.isnan(rata_rata_pendapatan) else "Data Tidak Tersedia"
            )

    # Baris 5: Distribusi Alumni Berdasarkan Rentang Pendapatan
    st.markdown("###### Distribusi Alumni Berdasarkan Rentang Pendapatan")
    if "PendapatanPerbulan" in filtered_data.columns:
        bins = [0, 6000000, 30000000, np.inf]
        labels = ["< 6 Juta", "6-30 Juta", "> 30 Juta"]
        filtered_data["RentangPendapatan"] = pd.cut(
            filtered_data["PendapatanPerbulan"], bins=bins, labels=labels, include_lowest=True
        )
        pendapatan_counts = filtered_data['RentangPendapatan'].value_counts(sort=False)
        if not pendapatan_counts.empty:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(pendapatan_counts.index.astype(str), pendapatan_counts.values, color='skyblue')
            ax.set_xlabel("Jumlah Alumni")
            ax.set_ylabel("Rentang Pendapatan")
            st.pyplot(fig)
        else:
            st.info("Data tidak tersedia untuk visualisasi rentang pendapatan.")
    else:
        st.info("Kolom 'PendapatanPerbulan' tidak ditemukan di dataset.")
