import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =========================================================
# ECOCLEAN COLOMIERS — V2
# =========================================================

st.set_page_config(
    page_title="EcoClean Colomiers",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLOMIERS_COORDS = [43.6135, 1.3330]

# ---------------------------------------------------------
# STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {font-size: 2.5rem; font-weight: 800; margin-bottom: 0;}
    .subtitle {font-size: 1.05rem; color: #667085; margin-top: 0.2rem;}
    .hero {padding: 1rem 0 0.5rem 0;}
    .small-muted {color: #667085; font-size: 0.9rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# BASE DE DONNÉES DE DÉMO
# ---------------------------------------------------------

DEMO_DATA = [
    {
        "id": 1,
        "type": "🧃 Gourde de compote / Emballage gâteau",
        "statut": "🔴 À ramasser",
        "lat": 43.6145,
        "lng": 1.3325,
        "adresse": "Près du Parc Duroch",
        "date": "2026-09-01",
    },
    {
        "id": 2,
        "type": "🥤 Canette / Bouteille plastique",
        "statut": "🟢 Ramassé !",
        "lat": 43.6110,
        "lng": 1.3340,
        "adresse": "Axe Gare de Colomiers",
        "date": "2026-09-02",
    },
    {
        "id": 3,
        "type": "🚬 Mégots groupés",
        "statut": "🔴 À ramasser",
        "lat": 43.6162,
        "lng": 1.3352,
        "adresse": "Centre-ville / Vieux Colomiers",
        "date": "2026-09-05",
    },
    {
        "id": 4,
        "type": "🍬 Emballage de bonbon / Papiers",
        "statut": "🟢 Ramassé !",
        "lat": 43.6122,
        "lng": 1.3295,
        "adresse": "Secteur du Pigeonnier",
        "date": "2026-09-06",
    },
]

if "dechets_db" not in st.session_state:
    st.session_state.dechets_db = pd.DataFrame(DEMO_DATA)

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def get_counts(df):
    total = len(df)
    ramasses = int((df["statut"] == "🟢 Ramassé !").sum())
    restants = int((df["statut"] == "🔴 À ramasser").sum())
    taux = round((ramasses / total) * 100) if total else 0
    return total, ramasses, restants, taux


def build_map(df):
    m = folium.Map(
        location=COLOMIERS_COORDS,
        zoom_start=15,
        control_scale=True,
        tiles="OpenStreetMap",
    )

    folium.Marker(
        COLOMIERS_COORDS,
        tooltip="🌱 EcoClean Colomiers",
        popup="Point central de Colomiers",
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(m)

    for _, row in df.iterrows():
        couleur = "red" if row["statut"] == "🔴 À ramasser" else "green"
        popup_html = f"""
        <div style='width:240px;font-family:Arial,sans-serif'>
            <h4 style='margin-bottom:8px'>{row['type']}</h4>
            <b>Statut :</b> {row['statut']}<br>
            <b>Lieu :</b> {row['adresse']}<br>
            <b>Date :</b> {row['date']}<br>
            <b>ID :</b> #{int(row['id'])}
        </div>
        """
        folium.Marker(
            location=[row["lat"], row["lng"]],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"#{int(row['id'])} — {row['type']}",
            icon=folium.Icon(color=couleur, icon="trash", prefix="fa"),
        ).add_to(m)

    return m

# ---------------------------------------------------------
# EN-TÊTE
# ---------------------------------------------------------

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="main-title">🌱 EcoClean Colomiers</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">La plateforme citoyenne pour signaler, suivre et réduire les micro-déchets à Colomiers.</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.image(
        "https://em-content.zobj.net/source/apple/391/seedling_1f331.png",
        width=55,
    )
    st.markdown("## EcoClean V2")
    st.caption("Prototype citoyen — Colomiers")
    st.markdown("---")

    menu = st.radio(
        "🧭 Navigation",
        [
            "🏠 Accueil",
            "🗺️ Carte des déchets",
            "📸 Signaler un déchet",
            "📊 Tableau de bord",
        ],
    )

    st.markdown("---")
    st.caption("💡 V2 : filtres, indicateurs, carte interactive et gestion des ramassages.")

# =========================================================
# ACCUEIL
# =========================================================

if menu == "🏠 Accueil":
    total, ramasses, restants, taux = get_counts(st.session_state.dechets_db)

    st.subheader("Bienvenue sur EcoClean Colomiers 👋")
    st.write(
        "EcoClean permet aux habitants de signaler rapidement les micro-déchets "
        "présents dans l'espace public et de suivre leur prise en charge."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🗑️ Signalements", total)
    c2.metric("🟢 Ramassés", ramasses)
    c3.metric("🔴 À ramasser", restants)
    c4.metric("♻️ Taux de nettoyage", f"{taux}%")

    st.markdown("---")
    left, right = st.columns([1.25, 1])

    with left:
        st.markdown("### 🎯 Comment ça marche ?")
        st.markdown(
            """
            **1. 📸 Signaler** — indiquez le type et la localisation du déchet.  
            **2. 🗺️ Visualiser** — retrouvez les signalements directement sur la carte.  
            **3. 🧤 Agir** — un déchet ramassé peut être marqué comme nettoyé.  
            **4. 📊 Mesurer** — suivez l'évolution de l'impact local.
            """
        )

    with right:
        st.markdown("### 🌱 Objectif")
        st.info(
            "Transformer les petits signalements du quotidien en données utiles "
            "pour encourager l'action citoyenne et identifier les zones prioritaires."
        )

    st.markdown("### 📍 Situation actuelle")
    if restants:
        st.warning(f"{restants} signalement(s) sont encore à traiter.")
    else:
        st.success("Tous les signalements sont actuellement traités 🎉")

# =========================================================
# CARTE
# =========================================================

elif menu == "🗺️ Carte des déchets":
    st.subheader("🗺️ Carte interactive des micro-déchets")
    st.caption("🔴 À ramasser · 🟢 Ramassé")

    df = st.session_state.dechets_db.copy()

    f1, f2, f3 = st.columns([1.2, 1.2, 1])
    with f1:
        statut_filter = st.multiselect(
            "Statut",
            ["🔴 À ramasser", "🟢 Ramassé !"],
            default=["🔴 À ramasser", "🟢 Ramassé !"],
        )
    with f2:
        types = sorted(df["type"].unique().tolist())
        type_filter = st.multiselect("Type de déchet", types)
    with f3:
        secteur_filter = st.multiselect(
            "Secteur",
            sorted(df["adresse"].unique().tolist()),
        )

    if statut_filter:
        df = df[df["statut"].isin(statut_filter)]
    if type_filter:
        df = df[df["type"].isin(type_filter)]
    if secteur_filter:
        df = df[df["adresse"].isin(secteur_filter)]

    st.info(f"📍 {len(df)} signalement(s) correspondent aux filtres sélectionnés.")
    st_folium(build_map(df), width=None, height=560, returned_objects=[])

    st.markdown("### 🧤 Actions de ramassage")
    if df.empty:
        st.info("Aucun signalement ne correspond aux filtres.")
    else:
        for index, row in df.iterrows():
            col1, col2, col3 = st.columns([3.5, 2, 1])
            with col1:
                st.markdown(
                    f"**#{int(row['id'])} — {row['type']}**  \n"
                    f"📍 {row['adresse']} · 📅 {row['date']}"
                )
            with col2:
                st.write(f"Statut : **{row['statut']}**")
            with col3:
                if row["statut"] == "🔴 À ramasser":
                    if st.button("✅ Ramassé", key=f"ramassage_{int(row['id'])}"):
                        st.session_state.dechets_db.at[index, "statut"] = "🟢 Ramassé !"
                        st.success("Signalement mis à jour.")
                        st.rerun()

# =========================================================
# SIGNALER
# =========================================================

elif menu == "📸 Signaler un déchet":
    st.subheader("📸 Signaler un micro-déchet")
    st.write(
        "Un déchet abandonné dans l'espace public ? Ajoutez son emplacement "
        "pour le rendre visible sur la carte."
    )

    with st.form("form_signalement", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            type_dechet = st.selectbox(
                "🗑️ Type de déchet",
                [
                    "🧃 Gourde de compote / Emballage gâteau",
                    "🥤 Canette / Bouteille plastique",
                    "🚬 Mégots groupés",
                    "🍬 Emballage de bonbon / Papiers",
                    "♻️ Autre déchet recyclable",
                    "🗑️ Autre déchet",
                ],
            )
        with col2:
            secteur = st.selectbox(
                "📍 Secteur de Colomiers",
                [
                    "Vieux Colomiers (Centre historique)",
                    "Parc Duroch",
                    "Axe Gare de Colomiers / Bus",
                    "Secteur du Pigeonnier",
                    "Autre secteur de proximité",
                ],
            )

        st.markdown("### 📌 Localisation")
        col_lat, col_lng = st.columns(2)
        with col_lat:
            lat = st.number_input(
                "Latitude",
                min_value=43.50,
                max_value=43.70,
                value=float(COLOMIERS_COORDS[0]),
                format="%.5f",
            )
        with col_lng:
            lng = st.number_input(
                "Longitude",
                min_value=1.20,
                max_value=1.50,
                value=float(COLOMIERS_COORDS[1]),
                format="%.5f",
            )

        description = st.text_area(
            "📝 Description (facultatif)",
            placeholder="Ex. : plusieurs emballages près d'un banc...",
        )

        submitted = st.form_submit_button("🚨 Valider le signalement", use_container_width=True)

    if submitted:
        db = st.session_state.dechets_db
        nouvel_id = int(db["id"].max()) + 1 if not db.empty else 1
        nouvelle_ligne = {
            "id": nouvel_id,
            "type": type_dechet,
            "statut": "🔴 À ramasser",
            "lat": lat,
            "lng": lng,
            "adresse": secteur + (f" — {description}" if description else ""),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        st.session_state.dechets_db = pd.concat(
            [db, pd.DataFrame([nouvelle_ligne])], ignore_index=True
        )
        st.success("🎉 Merci ! Le signalement a été ajouté à la carte EcoClean Colomiers.")
        st.balloons()

# =========================================================
# TABLEAU DE BORD
# =========================================================

elif menu == "📊 Tableau de bord":
    st.subheader("📊 Tableau de bord — Impact environnemental")

    df = st.session_state.dechets_db.copy()
    total, ramasses, restants, taux = get_counts(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🗑️ Total", total)
    c2.metric("🟢 Nettoyés", ramasses)
    c3.metric("🔴 En attente", restants)
    c4.metric("♻️ Taux de nettoyage", f"{taux}%")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.markdown("### 📈 Déchets par type")
        if not df.empty:
            repartition = df["type"].value_counts()
            st.bar_chart(repartition)

    with right:
        st.markdown("### 📍 Signalements par secteur")
        if not df.empty:
            secteurs = df["adresse"].str.split(" — ").str[0].value_counts()
            st.bar_chart(secteurs)

    st.markdown("### 🕒 Derniers signalements")
    if not df.empty:
        derniers = df.sort_values("date", ascending=False).copy()
        st.dataframe(
            derniers[["id", "type", "statut", "adresse", "date"]],
            use_container_width=True,
            hide_index=True,
        )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.caption(
    f"🌱 EcoClean Colomiers V2 · Prototype citoyen · {datetime.now().strftime('%d/%m/%Y')}"
)
