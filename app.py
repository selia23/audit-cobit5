import io
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Konfigurasi halaman web
st.set_page_config(page_title="Form Audit COBIT 5 - Polytron", page_icon="📊", layout="centered")

NAMA_PERUSAHAAN = "PT Hartono Istana Teknologi (Polytron), Kudus"
OBJEK_AUDIT = "Sistem informasi penjualan dan persediaan barang (ruang lingkup yang diusulkan)"
KERANGKA_KERJA = "COBIT 5 dengan lima domain proses: EDM, APO, BAI, DSS, dan MEA"
TUJUAN_AUDIT = ("Menilai kecukupan pengendalian atas pengelolaan informasi penjualan dan "
                "persediaan barang berdasarkan lima domain proses COBIT 5, serta "
                "mengidentifikasi area yang perlu diperbaiki.")
RUANG_LINGKUP = ("Pencatatan transaksi penjualan kepada dealer dan pelanggan, penerimaan barang "
                 "jadi dari pabrik ke gudang, pengeluaran dan pengiriman barang, pencatatan "
                 "mutasi dan saldo persediaan, pencocokan data dengan stok fisik, serta "
                 "pelaporan penjualan dan persediaan kepada manajemen.")

NAMA_DOMAIN = {
    'EDM': 'Evaluate, Direct and Monitor (Evaluasi, Pengarahan, dan Pengawasan)',
    'APO': 'Align, Plan and Organise (Perencanaan)',
    'BAI': 'Build, Acquire and Implement (Pembangunan)',
    'DSS': 'Deliver, Service and Support (Pelaksanaan)',
    'MEA': 'Monitor, Evaluate and Assess (Pengawasan)',
}

# (domain, kode proses, pertanyaan audit)
pertanyaan_audit = [
    # ---- EDM ----
    ('EDM', 'EDM01', 'Apakah manajemen melakukan evaluasi berkala terhadap proses pencatatan penjualan dan pengelolaan persediaan barang?'),
    ('EDM', 'EDM01', 'Apakah peran, tanggung jawab, dan kewenangan pengambilan keputusan terkait data penjualan dan persediaan barang di kantor pusat, pabrik, gudang, dan kantor perwakilan telah ditetapkan secara tertulis?'),
    ('EDM', 'EDM02', 'Apakah manajemen mengevaluasi manfaat pengelolaan informasi penjualan dan persediaan terhadap tujuan usaha, misalnya ketepatan pemenuhan pesanan dealer dan efisiensi proses?'),
    ('EDM', 'EDM03', 'Apakah manajemen telah menetapkan batas risiko yang dapat diterima terkait kesalahan, kehilangan, atau perubahan tanpa otorisasi pada data penjualan dan persediaan barang?'),
    ('EDM', 'EDM04', 'Apakah manajemen menyediakan sumber daya yang memadai (pegawai, anggaran, dan sarana pendukung) untuk pengelolaan data penjualan dan persediaan barang?'),
    ('EDM', 'EDM05', 'Apakah laporan penjualan dan persediaan barang disampaikan secara berkala kepada pimpinan dan pihak berkepentingan sesuai ketentuan perusahaan?'),
    # ---- APO ----
    ('APO', 'APO01', 'Apakah perusahaan memiliki prosedur tertulis mengenai pengelolaan data penjualan dan persediaan barang?'),
    ('APO', 'APO01', 'Apakah kebijakan dan prosedur pengelolaan data penjualan dan persediaan telah disosialisasikan kepada pegawai yang berkepentingan?'),
    ('APO', 'APO02', 'Apakah kebutuhan pengelolaan informasi penjualan dan persediaan barang dimuat dalam rencana kerja dan anggaran perusahaan?'),
    ('APO', 'APO07', 'Apakah pegawai yang mengelola data penjualan dan persediaan barang memperoleh pelatihan atau pembekalan yang sesuai dengan tugasnya?'),
    ('APO', 'APO12', 'Apakah perusahaan telah mengidentifikasi dan mendokumentasikan risiko pada proses penjualan dan persediaan barang, seperti selisih stok, kesalahan pencatatan pesanan, atau barang rusak dan tertahan?'),
    ('APO', 'APO13', 'Apakah terdapat kebijakan tertulis mengenai keamanan informasi yang mencakup data penjualan dan persediaan barang?'),
    # ---- BAI ----
    ('BAI', 'BAI02', 'Apakah kebutuhan pengguna (bagian penjualan, gudang, dan keuangan) terhadap pencatatan dan pelaporan penjualan dan persediaan diidentifikasi dan didokumentasikan?'),
    ('BAI', 'BAI04', 'Apakah perusahaan memeriksa kecukupan kapasitas dan ketersediaan sarana pencatatan dibandingkan dengan jumlah transaksi penjualan dan pergerakan persediaan?'),
    ('BAI', 'BAI06', 'Apakah setiap perubahan prosedur atau sarana pencatatan penjualan dan persediaan diajukan dan disetujui secara tertulis oleh pihak berwenang sebelum dilaksanakan?'),
    ('BAI', 'BAI07', 'Apakah perubahan sistem pencatatan penjualan dan persediaan diuji sebelum diterapkan dan hasil pengujiannya didokumentasikan?'),
    ('BAI', 'BAI08', 'Apakah tersedia panduan atau dokumentasi kerja yang dapat diakses pegawai dalam menjalankan pencatatan penjualan dan persediaan barang?'),
    ('BAI', 'BAI09', 'Apakah perusahaan memiliki daftar aset pendukung pengelolaan data penjualan dan persediaan beserta penanggung jawabnya, dan memperbaruinya secara berkala?'),
    # ---- DSS ----
    ('DSS', 'DSS01', 'Apakah kegiatan operasional harian pencatatan penjualan, penerimaan barang jadi, dan pengeluaran barang dilaksanakan sesuai prosedur yang berlaku?'),
    ('DSS', 'DSS02', 'Apakah terdapat prosedur penanganan apabila sistem pencatatan transaksi mengalami gangguan?'),
    ('DSS', 'DSS03', 'Apakah penyebab gangguan atau kesalahan pencatatan yang terjadi berulang dianalisis dan ditindaklanjuti agar tidak terulang?'),
    ('DSS', 'DSS04', 'Apakah terdapat pencadangan data penjualan dan persediaan barang, baik digital maupun dokumen fisik, beserta prosedur pemulihannya?'),
    ('DSS', 'DSS05', 'Apakah akses terhadap data dan catatan penjualan dan persediaan barang dibatasi sesuai kewenangan masing-masing pegawai?'),
    ('DSS', 'DSS06', 'Apakah terdapat pemisahan tugas antara pegawai yang melakukan penjualan, menyimpan dan mengeluarkan barang di gudang, serta mencatat transaksi?'),
    # ---- MEA ----
    ('MEA', 'MEA01', 'Apakah perusahaan menetapkan indikator kinerja proses penjualan dan persediaan barang, misalnya ketepatan pencatatan dan tingkat selisih stok, serta memantaunya secara berkala?'),
    ('MEA', 'MEA01', 'Apakah capaian penjualan dan pengelolaan persediaan dibandingkan dengan target perusahaan, dan penyimpangannya dianalisis serta dilaporkan kepada manajemen?'),
    ('MEA', 'MEA02', 'Apakah perusahaan melakukan pemeriksaan berkala (stok opname) terhadap kesesuaian data persediaan dengan stok fisik di gudang?'),
    ('MEA', 'MEA02', 'Apakah terdapat fungsi pengawasan intern atau fungsi sejenis yang menilai pengendalian pada proses penjualan dan persediaan barang?'),
    ('MEA', 'MEA02', 'Apakah kelemahan pengendalian yang ditemukan dari pemeriksaan internal maupun eksternal ditindaklanjuti dan statusnya dipantau?'),
    ('MEA', 'MEA03', 'Apakah perusahaan memantau kepatuhan proses penjualan dan persediaan barang terhadap ketentuan eksternal, misalnya ketentuan perpajakan atau perjanjian dengan dealer dan pihak ketiga?'),
]

DAFTAR_PERTANYAAN = [
    {"no": i, "domain": d, "kode": k, "teks": t}
    for i, (d, k, t) in enumerate(pertanyaan_audit, start=1)
]
TOTAL = len(DAFTAR_PERTANYAAN)          # 30
URUTAN_DOMAIN = ['EDM', 'APO', 'BAI', 'DSS', 'MEA']
PILIHAN = ['Ya', 'Tidak', 'N/A']

# ---------------------------------------------------------------------------
# FUNGSI BANTU
# ---------------------------------------------------------------------------

def indikator(ya, jumlah, na):
    """Indikator kepatuhan sederhana = Ya / (Jumlah Pertanyaan - N/A) x 100%."""
    penyebut = jumlah - na
    if penyebut <= 0:
        return None
    return round(ya / penyebut * 100, 2)


def fmt_persen(v):
    return "-" if v is None or pd.isna(v) else f"{v:.2f}%"


def hitung_rekap(isian):
    """Rekapitulasi per domain (Tabel 6) dari dict isian {no: {...}}."""
    baris = []
    tot = {"Jumlah Pertanyaan": 0, "Ya": 0, "Tidak": 0, "N/A": 0}
    for dom in URUTAN_DOMAIN:
        nomor = [q["no"] for q in DAFTAR_PERTANYAAN if q["domain"] == dom]
        ya = sum(1 for n in nomor if isian[n]["jawaban"] == "Ya")
        tidak = sum(1 for n in nomor if isian[n]["jawaban"] == "Tidak")
        na = sum(1 for n in nomor if isian[n]["jawaban"] == "N/A")
        baris.append({"Domain": dom, "Jumlah Pertanyaan": len(nomor), "Ya": ya,
                      "Tidak": tidak, "N/A": na,
                      "Indikator Kepatuhan (%)": indikator(ya, len(nomor), na)})
        tot["Jumlah Pertanyaan"] += len(nomor)
        tot["Ya"] += ya
        tot["Tidak"] += tidak
        tot["N/A"] += na
    baris.append({"Domain": "Total", **tot,
                  "Indikator Kepatuhan (%)": indikator(tot["Ya"], tot["Jumlah Pertanyaan"], tot["N/A"])})
    return pd.DataFrame(baris)


def hitung_temuan(isian):
    """Pertanyaan berjawaban 'Tidak' sebagai bahan awal Tabel 7."""
    hasil = []
    for q in DAFTAR_PERTANYAAN:
        j = isian[q["no"]]
        if j["jawaban"] == "Tidak":
            hasil.append({
                "No.": len(hasil) + 1,
                "Ref. No.": q["no"],
                "Temuan Audit": j["catatan"] or "Pengendalian tidak diterapkan atau tidak dapat dibuktikan.",
                "Risiko yang Mungkin Timbul": "",
                "Rekomendasi Perbaikan": "",
                "Penanggung Jawab": "",
                "Tindak Lanjut": "",
            })
    return pd.DataFrame(hasil, columns=["No.", "Ref. No.", "Temuan Audit", "Risiko yang Mungkin Timbul",
                                        "Rekomendasi Perbaikan", "Penanggung Jawab", "Tindak Lanjut"])


def buat_grafik(df_rekap):
    d = df_rekap[df_rekap["Domain"] != "Total"]
    fig, ax = plt.subplots(figsize=(8, 4))
    bawah = [0] * len(d)
    for kolom, warna in [("Ya", "#4CAF50"), ("Tidak", "#E57373"), ("N/A", "#BDBDBD")]:
        nilai = d[kolom].tolist()
        ax.bar(d["Domain"], nilai, bottom=bawah, color=warna, edgecolor="black", label=kolom)
        for x, (v, b0) in enumerate(zip(nilai, bawah)):
            if v > 0:
                ax.text(x, b0 + v / 2, str(v), ha="center", va="center", fontweight="bold")
        bawah = [b0 + v for b0, v in zip(bawah, nilai)]
    ax.set_ylim(0, 7)
    ax.set_ylabel("Jumlah Pertanyaan")
    ax.set_title("Rekapitulasi Jawaban per Domain COBIT 5", fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    ax.legend(loc="upper right", ncol=3)
    return fig


def _format_sheet(ws, lebar):
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    tipis = Side(style="thin", color="999999")
    garis = Border(left=tipis, right=tipis, top=tipis, bottom=tipis)
    for kol, w in lebar.items():
        ws.column_dimensions[kol].width = w
    for row in ws.iter_rows():
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = garis
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="F2F2F2")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.freeze_panes = "A2"


def buat_excel(identitas, isian, df_rekap, df_temuan):
    df_identitas = pd.DataFrame(list(identitas.items()), columns=["Komponen", "Keterangan"])

    baris = []
    for q in DAFTAR_PERTANYAAN:
        j = isian[q["no"]]
        baris.append({
            "No.": q["no"], "Domain": q["domain"], "Kode Proses": q["kode"],
            "Pertanyaan Audit": q["teks"],
            "Ya": "✓" if j["jawaban"] == "Ya" else "",
            "Tidak": "✓" if j["jawaban"] == "Tidak" else "",
            "N/A": "✓" if j["jawaban"] == "N/A" else "",
            "Bukti Pendukung": j["bukti"], "Catatan Auditor": j["catatan"],
        })
    df_form = pd.DataFrame(baris)

    df_r = df_rekap.copy()
    df_r["Indikator Kepatuhan (%)"] = df_r["Indikator Kepatuhan (%)"].apply(
        lambda v: "-" if v is None or pd.isna(v) else v)
    df_r["Catatan"] = ""

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_identitas.to_excel(writer, sheet_name="Identitas Audit", index=False)
        df_form.to_excel(writer, sheet_name="Form Audit", index=False)
        df_r.to_excel(writer, sheet_name="Rekapitulasi", index=False)
        df_temuan.to_excel(writer, sheet_name="Temuan", index=False)
        _format_sheet(writer.sheets["Identitas Audit"], {"A": 26, "B": 90})
        _format_sheet(writer.sheets["Form Audit"],
                      {"A": 6, "B": 9, "C": 12, "D": 70, "E": 6, "F": 8, "G": 6, "H": 40, "I": 40})
        _format_sheet(writer.sheets["Rekapitulasi"],
                      {"A": 12, "B": 20, "C": 8, "D": 8, "E": 8, "F": 26, "G": 30})
        _format_sheet(writer.sheets["Temuan"],
                      {"A": 6, "B": 9, "C": 45, "D": 30, "E": 30, "F": 20, "G": 20})
    return output.getvalue()


# ---------------------------------------------------------------------------
# TAMPILAN: HEADER
# ---------------------------------------------------------------------------

st.title("FORM AUDIT SISTEM INFORMASI PENJUALAN DAN PERSEDIAAN BARANG")
st.subheader(f"{NAMA_PERUSAHAAN} – COBIT 5")

with st.expander("📖 Petunjuk pengisian jawaban (klik untuk buka/tutup)"):
    st.markdown("""
    * **Ya** - Pengendalian diterapkan dan terdapat bukti yang mendukung.
    * **Tidak** - Pengendalian tidak diterapkan atau tidak dapat dibuktikan.
    * **N/A** - Pertanyaan tidak relevan dengan kondisi objek audit.

    *Jawaban "Ya" hanya diberikan apabila bukti pendukung telah diperiksa, sehingga kolom
    bukti pendukung wajib diisi untuk jawaban "Ya".*
    """)

st.markdown(f"**Objek audit:** {OBJEK_AUDIT}  \n**Kerangka kerja:** {KERANGKA_KERJA}")
st.markdown("---")

# ---------------------------------------------------------------------------
# TAMPILAN: FORM
# ---------------------------------------------------------------------------

isian = {}

with st.form("form_audit"):
    st.markdown("#### Identitas Audit")
    c1, c2 = st.columns(2)
    tanggal = c1.date_input("Tanggal audit", value=date.today(), format="DD/MM/YYYY", key="tgl")
    auditor = c2.text_input("Nama auditor", key="auditor")
    responden = c1.text_input("Responden", key="responden")
    bagian = c2.text_input("Bagian / unit kerja", key="bagian")

    st.markdown("#### Pertanyaan Audit")
    tab_list = st.tabs([f"Domain {d}" for d in URUTAN_DOMAIN])

    for dom, tab in zip(URUTAN_DOMAIN, tab_list):
        with tab:
            st.header(f"Domain: {dom}")
            st.caption(NAMA_DOMAIN[dom])
            kode_sebelumnya = None
            for q in [x for x in DAFTAR_PERTANYAAN if x["domain"] == dom]:
                if q["kode"] != kode_sebelumnya:
                    st.markdown(f"#### 🔹 {q['kode']}")
                    kode_sebelumnya = q["kode"]
                st.markdown(f"**{q['no']}.** {q['teks']}")
                jwb = st.radio(f"Jawaban pertanyaan {q['no']}", PILIHAN, index=None, horizontal=True,
                               key=f"j_{q['no']}", label_visibility="collapsed")
                bukti = st.text_area("Bukti pendukung", key=f"b_{q['no']}", height=68,
                                     placeholder="Dokumen, catatan transaksi, SOP, tangkapan layar, atau hasil pemeriksaan")
                catatan = st.text_area("Catatan auditor", key=f"c_{q['no']}", height=68,
                                       placeholder="Penjelasan mengenai kondisi yang ditemukan")
                isian[q["no"]] = {"jawaban": jwb, "bukti": bukti.strip(), "catatan": catatan.strip()}
                st.markdown("---")

    submitted = st.form_submit_button("🔍 Selesaikan Audit & Lihat Hasil")

# ---------------------------------------------------------------------------
# PROSES SETELAH SUBMIT
# ---------------------------------------------------------------------------

if submitted:
    st.session_state.pop("hasil", None)
    kosong = [n for n, v in isian.items() if v["jawaban"] is None]
    ya_tanpa_bukti = [n for n, v in isian.items() if v["jawaban"] == "Ya" and not v["bukti"]]

    if not (auditor.strip() and responden.strip() and bagian.strip()):
        st.error("⚠️ Nama auditor, responden, dan bagian/unit kerja wajib diisi.")
    elif kosong:
        st.error(f"⚠️ Masih ada {len(kosong)} pertanyaan yang belum dijawab "
                 f"(nomor: {', '.join(map(str, kosong))}). Harap isi semua pertanyaan di setiap tab domain.")
    elif ya_tanpa_bukti:
        st.error("⚠️ Jawaban \"Ya\" wajib disertai bukti pendukung. Periksa pertanyaan nomor: "
                 f"{', '.join(map(str, ya_tanpa_bukti))}.")
    else:
        identitas = {
            "Nama perusahaan": NAMA_PERUSAHAAN,
            "Objek audit": OBJEK_AUDIT,
            "Kerangka kerja audit": KERANGKA_KERJA,
            "Tanggal audit": tanggal.strftime("%d-%m-%Y"),
            "Nama auditor": auditor.strip(),
            "Responden": responden.strip(),
            "Bagian atau unit kerja": bagian.strip(),
            "Tujuan audit": TUJUAN_AUDIT,
            "Ruang lingkup audit": RUANG_LINGKUP,
        }
        df_rekap = hitung_rekap(isian)
        df_temuan = hitung_temuan(isian)
        # Disimpan di session_state agar hasil tidak hilang saat tombol unduh ditekan
        st.session_state["hasil"] = {
            "df_rekap": df_rekap,
            "df_temuan": df_temuan,
            "excel": buat_excel(identitas, isian, df_rekap, df_temuan),
            "isian": isian,
        }

# ---------------------------------------------------------------------------
# TAMPILAN HASIL
# ---------------------------------------------------------------------------

if "hasil" in st.session_state:
    h = st.session_state["hasil"]
    df_rekap = h["df_rekap"]
    df_temuan = h["df_temuan"]

    st.success("Pengisian form audit selesai!")

    st.subheader("1. Grafik Rekapitulasi per Domain")
    fig = buat_grafik(df_rekap)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("2. Rekapitulasi Jawaban Form Audit (Tabel 6)")
    tampil = df_rekap.copy()
    tampil["Indikator Kepatuhan"] = tampil["Indikator Kepatuhan (%)"].apply(fmt_persen)
    tampil = tampil.drop(columns=["Indikator Kepatuhan (%)"])
    st.dataframe(tampil, hide_index=True)
    st.caption("Indikator kepatuhan sederhana = Jumlah Ya ÷ (Jumlah Pertanyaan − Jumlah N/A) × 100%. "
               "Nilai ini hanya indikator berdasarkan jawaban kuesioner dan bukan nilai capability level "
               "resmi COBIT 5.")

    st.subheader("3. Pertanyaan Berjawaban \"Tidak\" (bahan awal Tabel 7)")
    if df_temuan.empty:
        st.info("Tidak ada pertanyaan yang dijawab \"Tidak\".")
    else:
        rinci = []
        for _, r in df_temuan.iterrows():
            q = DAFTAR_PERTANYAAN[int(r["Ref. No."]) - 1]
            rinci.append({"Ref. No.": q["no"], "Kode": q["kode"], "Pertanyaan Audit": q["teks"],
                          "Catatan Auditor": h["isian"][q["no"]]["catatan"] or "-"})
        st.dataframe(pd.DataFrame(rinci), hide_index=True)

    st.download_button(
        label="📥 Unduh Hasil Excel",
        data=h["excel"],
        file_name="Hasil_Audit_COBIT5_Polytron.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
