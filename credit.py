import streamlit as st
import pandas as pd
import joblib

# Fungsi untuk menentukan kategori skor kredit
def get_credit_score_category(score):
    if 300 <= score <= 579:
        return "Poor"
    elif 580 <= score <= 669:
        return "Fair"
    elif 670 <= score <= 739:
        return "Good"
    elif 740 <= score <= 799:
        return "Very Good"
    elif 800 <= score <= 850:
        return "Excellent"
    else:
        return "Invalid Score"

# Memuat model yang telah disimpan
model = joblib.load('/mount/src/random_forest_model.pkl')

# Judul Aplikasi
st.title("Prediksi Skor Kredit UMKM")
st.write("Gunakan aplikasi ini untuk memprediksi skor kredit UMKM Anda berdasarkan berbagai parameter bisnis.")

# Sidebar untuk input pengguna
st.sidebar.header("Input Parameter UMKM")

# Input fitur dari pengguna
provinsi_options = [
    'Aceh', 'Sumatra Utara', 'Sumatra Barat', 'Riau', 'Kepulauan Riau', 'Jambi', 'Sumatra Selatan', 
    'Kepulauan Bangka Belitung', 'Bengkulu', 'Lampung', 'DKI Jakarta', 'Jawa Barat', 'Banten', 
    'Jawa Tengah', 'DI Yogyakarta', 'Jawa Timur', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 
    'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 
    'Sulawesi Utara', 'Gorontalo', 'Sulawesi Tengah', 'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tenggara', 
    'Maluku', 'Maluku Utara', 'Papua Barat', 'Papua', 'Papua Tengah', 'Papua Pegunungan', 'Papua Selatan', 'Papua Barat Daya'
]
provinsi_mapping = {prov: idx+1 for idx, prov in enumerate(provinsi_options)}
kriteria_options = {'Mikro (Micro)': 1, 'Kecil (Small)': 2, 'Menengah (Medium)': 3}
jenis_options = {
    'Usaha Fashion (Fashion Business)': 1,
    'Usaha Otomotif (Automotive Business)': 2,
    'Usaha Kecantikan (Beauty Business)': 3,
    'Usaha Kuliner (Culinary Business)': 4,
    'Usaha Agribisnis (Agribusiness)': 5
}
lokasi_options = {
    'Perkotaan (Urban)': 1,
    'Pinggiran Kota (Suburban)': 2,
    'Pedesaan (Rural)': 3
}
status_kepemilikan_options = {
    'Milik Sendiri (Owned)': 1,
    'Sewa (Rented)': 2,
    'Keluarga (Family-owned)': 3,
    'Lainnya (Other)': 4
}
rekening_options = {
    'Ada (Yes)': 1,
    'Tidak Ada (No)': 0
}

provinsi = st.sidebar.selectbox("Provinsi", list(provinsi_options))
kriteria_umkm = st.sidebar.selectbox("Kriteria UMKM", list(kriteria_options.keys()))
jenis_umkm = st.sidebar.selectbox("Jenis UMKM", list(jenis_options.keys()))
lokasi_usaha = st.sidebar.selectbox("Lokasi Usaha", list(lokasi_options.keys()))
lama_usaha = st.sidebar.number_input("Lama Usaha (Bulan)", min_value=0)
status_kepemilikan = st.sidebar.selectbox("Status Kepemilikan Tempat Usaha", list(status_kepemilikan_options.keys()))

# Kondisional untuk jumlah karyawan berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    jumlah_karyawan = st.sidebar.number_input("Jumlah Karyawan (Mikro: <5 orang)", max_value=5)
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    jumlah_karyawan = st.sidebar.number_input("Jumlah Karyawan (Kecil: >5 - 25 orang)", min_value=6, max_value=25)
else:  # Menengah
    jumlah_karyawan = st.sidebar.number_input("Jumlah Karyawan (Menengah: >25 - 100 orang)", min_value=26, max_value=100)

# Kondisional untuk aset usaha berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    aset_usaha_options = {
        '< Rp10.000.000': 1,
        'Rp10.000.000 - Rp30.000.000': 2,
        'Rp30.000.001 - Rp50.000.000': 3
    }
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    aset_usaha_options = {
        'Rp50.000.001 - Rp100.000.000': 4,
        'Rp100.000.001 - Rp200.000.000': 5,
        'Rp200.000.001 - Rp300.000.000': 6,
        'Rp300.000.001 - Rp400.000.000': 7,
        'Rp400.000.001 - Rp500.000.000': 8,
        'Rp500.000.001 - Rp1.000.000.000': 9
    }
else:  # Menengah
    aset_usaha_options = {
        'Rp1.000.000.001 - Rp3.000.000.000': 10,
        'Rp3.000.000.001 - Rp5.000.000.000': 11,
        'Rp5.000.000.001 - Rp7.000.000.000': 12,
        'Rp7.000.000.001 - Rp10.000.000.000': 13
    }

aset_usaha = st.sidebar.selectbox("Aset Usaha (IDR)", list(aset_usaha_options.keys()))
jumlah_pasti_aset_usaha = st.sidebar.number_input("Jumlah Pasti Aset Usaha (IDR)", min_value=0)

# Kondisional untuk liabilitas usaha berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    liabilitas_usaha_options = {
        '< Rp20.000.000': 1,
        'Rp20.000.000 - Rp100.000.000': 2,
        'Rp100.000.001 - Rp250.000.000': 3
    }
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    liabilitas_usaha_options = {
        '< Rp50.000.000': 4,
        'Rp50.000.000 - Rp200.000.000': 5,
        'Rp200.000.001 - Rp300.000.000': 6,
        'Rp300.000.001 - Rp400.000.000': 7,
        '> Rp400.000.000': 8,
        '< Rp500.000.000': 9
    }
else:  # Menengah
    liabilitas_usaha_options = {
        'Rp500.000.000 - Rp2.000.000.000': 10,
        'Rp2.000.000.001 - Rp3.000.000.000': 11,
        'Rp3.000.000.001 - Rp4.000.000.000': 12,
        '> Rp4.000.000.000': 13
    }

liabilitas_usaha = st.sidebar.selectbox("Liabilitas Usaha (IDR)", list(liabilitas_usaha_options.keys()))
jumlah_pasti_liabilitas_usaha = st.sidebar.number_input("Jumlah Pasti Liabilitas Usaha (IDR)", min_value=0)

# Kondisional untuk omset bulanan berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    omset_bulanan_options = {
        '< Rp100.000.000': 1,
        'Rp100.000.000 - Rp300.000.000': 2
    }
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    omset_bulanan_options = {
        'Rp300.000.001 - Rp800.000.000': 3,
        'Rp800.000.001 - Rp1.500.000.000': 4,
        'Rp1.500.000.001 - Rp2.500.000.000': 5
    }
else:  # Menengah
    omset_bulanan_options = {
        'Rp2.500.000.001 - Rp10.000.000.000': 6,
        'Rp10.000.000.001 - Rp20.000.000.000': 7,
        'Rp20.000.000.001 - Rp35.000.000.000': 8,
                'Rp35.000.000.001 - Rp50.000.000.000': 9
    }

omset_bulanan = st.sidebar.selectbox("Omset Bulanan (IDR)", list(omset_bulanan_options.keys()))
jumlah_pasti_omset_bulanan = st.sidebar.number_input("Jumlah Pasti Omset Bulanan (IDR)", min_value=0)

# Kondisional untuk laba bersih berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    laba_bersih_options = {
        '< Rp20.000.000': 1,
        'Rp20.000.000 - Rp100.000.000': 2,
        'Rp100.000.001 - Rp250.000.000': 3
    }
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    laba_bersih_options = {
        '< Rp50.000.000': 4,
        'Rp50.000.000 - Rp200.000.000': 5,
        'Rp200.000.001 - Rp300.000.000': 6,
        'Rp300.000.001 - Rp400.000.000': 7,
        '> Rp400.000.000': 8
    }
else:  # Menengah
    laba_bersih_options = {
        '< Rp1.000.000.000': 9,
        'Rp1.000.000.000 - Rp3.000.000.000': 10,
        'Rp3.000.000.001 - Rp5.000.000.000': 11,
        'Rp5.000.000.001 - Rp7.000.000.000': 12,
        '> Rp7.000.000.000': 13
    }

laba_bersih = st.sidebar.selectbox("Laba Bersih (IDR)", list(laba_bersih_options.keys()))
jumlah_pasti_laba_bersih = st.sidebar.number_input("Jumlah Pasti Laba Bersih (IDR)", min_value=0)

# Kondisional untuk jumlah pinjaman berdasarkan kriteria UMKM
if kriteria_options[kriteria_umkm] == 1:  # Mikro
    jumlah_pinjaman_options = {
        '< Rp10.000.000': 1,
        'Rp10.000.000 - Rp50.000.000': 2,
        'Rp50.000.001 - Rp100.000.000': 3,
        'Rp50.000.000 - Rp100.000.000': 4
    }
elif kriteria_options[kriteria_umkm] == 2:  # Kecil
    jumlah_pinjaman_options = {
        'Rp100.000.001 - Rp200.000.000': 5,
        '< Rp50.000.000': 6,
        '> Rp200.000.000': 7
    }
else:  # Menengah
    jumlah_pinjaman_options = {
        'Rp2.000.000.001 - Rp3.000.000.000': 8,
        'Rp1.000.000.000 - Rp2.000.000.000': 9,
        '< Rp1.000.000.000': 10,
        '> Rp3.000.000.000': 11
    }

jumlah_pinjaman = st.sidebar.selectbox("Jumlah Pinjaman (IDR)", list(jumlah_pinjaman_options.keys()))
jumlah_pasti_jumlah_pinjaman = st.sidebar.number_input("Jumlah Pasti Jumlah Pinjaman (IDR)", min_value=0)
rekening_bank = st.sidebar.selectbox("Rekening Bank", list(rekening_options.keys()))

# Prediksi ketika tombol ditekan
if st.sidebar.button("Prediksi Skor Kredit"):
    # Mengubah input pengguna ke dalam bentuk numerik
    input_features = [[
        provinsi_mapping[provinsi],
        kriteria_options[kriteria_umkm],
        jenis_options[jenis_umkm],
        lokasi_options[lokasi_usaha],
        lama_usaha,
        status_kepemilikan_options[status_kepemilikan],
        jumlah_karyawan,
        aset_usaha_options[aset_usaha],
        jumlah_pasti_aset_usaha,
        liabilitas_usaha_options[liabilitas_usaha],
        jumlah_pasti_liabilitas_usaha,
        omset_bulanan_options[omset_bulanan],
        jumlah_pasti_omset_bulanan,
        laba_bersih_options[laba_bersih],
        jumlah_pasti_laba_bersih,
        jumlah_pinjaman_options[jumlah_pinjaman],
        jumlah_pasti_jumlah_pinjaman,
        rekening_options[rekening_bank]
    ]]
    input_df = pd.DataFrame(input_features, columns=[
        "Provinsi", "Kriteria UMKM", "Jenis UMKM", "Lokasi Usaha", "Lama Usaha (Bulan)",
        "Status Kepemilikan Tempat Usaha", "Jumlah Karyawan", "Aset Usaha (IDR)",
        "Jumlah Pasti Aset Usaha (IDR)", "Liabilitas Usaha (IDR)", "Jumlah Pasti Liabilitas Usaha (IDR)",
        "Omset Bulanan (IDR)", "Jumlah Pasti Omset Bulanan (IDR)", "Laba Bersih (IDR)",
        "Jumlah Pasti Laba Bersih (IDR)", "Jumlah Pinjaman (IDR)", "Jumlah Pasti Jumlah Pinjaman (IDR)",
        "Rekening Bank"
    ])
    
    # Melakukan prediksi
    prediction = model.predict(input_df)
    predicted_score = prediction[0]
    
    # Menentukan kategori skor kredit
    credit_score_category = get_credit_score_category(predicted_score)
    
    # Menampilkan hasil prediksi
    st.subheader("Hasil Prediksi")
    st.write(f"Prediksi Skor Kredit: {predicted_score}")
    st.write(f"Kategori Skor Kredit: {credit_score_category}")

    # Ekspander untuk menampilkan input detail
    with st.expander("Lihat Detail Input"):
        st.write("Provinsi:", provinsi)
        st.write("Kriteria UMKM:", kriteria_umkm)
        st.write("Jenis UMKM:", jenis_umkm)
        st.write("Lokasi Usaha:", lokasi_usaha)
        st.write("Lama Usaha (Bulan):", lama_usaha)
        st.write("Status Kepemilikan Tempat Usaha:", status_kepemilikan)
        st.write("Jumlah Karyawan:", jumlah_karyawan)
        st.write("Aset Usaha (IDR):", aset_usaha)
        st.write("Jumlah Pasti Aset Usaha (IDR):", jumlah_pasti_aset_usaha)
        st.write("Liabilitas Usaha (IDR):", liabilitas_usaha)
        st.write("Jumlah Pasti Liabilitas Usaha (IDR):", jumlah_pasti_liabilitas_usaha)
        st.write("Omset Bulanan (IDR):", omset_bulanan)
        st.write("Jumlah Pasti Omset Bulanan (IDR):", jumlah_pasti_omset_bulanan)
        st.write("Laba Bersih (IDR):", laba_bersih)
        st.write("Jumlah Pasti Laba Bersih (IDR):", jumlah_pasti_laba_bersih)
        st.write("Jumlah Pinjaman (IDR):", jumlah_pinjaman)
        st.write("Jumlah Pasti Jumlah Pinjaman (IDR):", jumlah_pasti_jumlah_pinjaman)
        st.write("Rekening Bank:", rekening_bank)
