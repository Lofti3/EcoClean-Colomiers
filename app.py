import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =========================================================
# ECOCLEAN COLOMIERS — V3 CITOYENNE
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
# DONNÉES DE DÉMONSTRATION
# Tous les exemples sont initialement "À ramasser".
# Un citoyen peut ensuite les marquer comme ramassés.
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
        "description": "Déchet visible dans l'espace public.",
    },
    {
        "id": 2,
        "type": "🥤 Canette / Bouteille plastique",
        "statut": "🔴 À ramasser",
        "lat": 43.6110,
        "lng": 1.3340,
        "adresse": "Axe Gare de Colomiers",
        "date": "2026-09-02",
        "description": "Déchet signalé par un citoyen.",
    },
    {
        "id": 3,
        "type": "🚬 Mégots groupés",
        "statut": "🔴 À ramasser",
        "lat": 43.6162,
        "lng": 1.3352,
        "adresse": "Centre-ville / Vieux Colomiers",
        "date": "2026-09-05",
        "description": "Plusieurs mégots regroupés.",
    },
    {
        "id": 4,
        "type": "🍬 Emballage de bonbon / Papiers",
        "statut": "🔴 À ramasser",
        "lat": 43.6122,
        "lng": 1.3295,
        "adresse": "Secteur du Pigeonnier",
        "date": "2026-09-06",
        "description": "Petits emballages abandonnés.",
    },
]

if "dechets_db" not in st.session_state:
    st.session_state.dechets_db = pd.DataFrame(DEMO_DATA)

if "actions_ramassage" not in st.session_state:
    st.session_state.actions_ramassage = []

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------

def get_counts(df):
    total = len(df)
    ramasses = int((df["statut"] == "🟢 Ramassé").sum())
    restants = int((df["statut"] == "🔴 À ramasser").sum())
    taux = round((ramasses / total) * 100) if total else 0
    contributeurs = len(set(st.session_state.actions_ramassage))
    return total, ramasses, restants, taux, contributeurs


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
        popup="Plateforme citoyenne de Colomiers",
        icon=folium.Icon(color="blue", icon="home", prefix="fa"),
    ).add_to(m)

    for _, row in df.iterrows():
        couleur = "red" if row["statut"] == "🔴 À ramasser" else "green"
        popup_html = f"""
        <div style='width:250px;font-family:Arial,sans-serif'>
            <h4 style='margin-bottom:8px'>{row['type']}</h4>
            <b>Statut :</b> {row['statut']}<br>
            <b>Lieu :</b> {row['adresse']}<br>
            <b>Date :</b> {row['date']}<br>
            <b>Description :</b> {row.get('description', '')}<br>
            <b>ID :</b> #{int(row['id'])}
        </div>
        """
        folium.Marker(
            location=[row["lat"], row["lng"]],
            popup=folium.Popup(popup_html, max_width=330),
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
    '<div class="subtitle">Une plateforme citoyenne pour signaler, ramasser et réduire les micro-déchets à Colomiers.</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("# 🌱 EcoClean")
    st.caption("La propreté de Colomiers, c'est l'affaire de tous.")
    st.markdown("---")

    menu = st.radio(
        "🧭 Navigation",
        [
            "🏠 Accueil",
            "🗺️ Carte des déchets",
            "📸 Signaler un déchet",
            "📊 Impact citoyen",
        ],
    )

    st.markdown("---")
    st.caption("💚 Chaque citoyen peut signaler un déchet ou contribuer à son ramassage.")

# =========================================================
# ACCUEIL
# =========================================================

if menu == "🏠 Accueil":
    total, ramasses, restants, taux, contributeurs = get_counts(st.session_state.dechets_db)

    st.subheader("Bienvenue sur EcoClean Colomiers 👋")
    st.write(
        "Vous voyez un déchet abandonné ? Signalez-le. Vous passez près d'un déchet signalé ? "
        "Vous pouvez le ramasser et contribuer à améliorer votre ville."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🗑️ Signalements", total)
    c2.metric("🧤 Ramassés", ramasses)
    c3.metric("🔴 À ramasser", restants)
    c4.metric("👥 Contributeurs", contributeurs)

    st.markdown("---")
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("### 🤝 Comment participer ?")
        st.markdown(
            """
            **1. 📸 Signaler** — vous trouvez un déchet et le signalez sur EcoClean.  
            **2. 🗺️ Localiser** — le signalement apparaît sur la carte de Colomiers.  
            **3. 🧤 Ramasser** — n'importe quel citoyen peut décider de le ramasser.  
            **4. ✅ Confirmer** — cliquez sur « Je l'ai ramassé » pour mettre à jour la carte.
            """
        )

    with right:
        st.markdown("### 🌱 Notre objectif")
        st.info(
            "Créer une dynamique citoyenne simple : une personne signale, une autre peut agir. "
            "EcoClean transforme ces petits gestes en impact collectif."
        )

    st.markdown("### 📍 État actuel")
    if restants:
        st.warning(f"🔴 {restants} déchet(s) sont actuellement signalés comme étant à ramasser.")
    else:
        st.success("🎉 Aucun déchet signalé n'est actuellement en attente !")

    st.markdown("### 🧤 Vous avez envie d'agir ?")
    st.write("Consultez la carte et choisissez un déchet que vous pouvez ramasser en toute sécurité.")
    if st.button("🗺️ Voir les déchets à ramasser", use_container_width=True):
        st.info("Utilisez le menu à gauche pour ouvrir la carte des déchets.")

# =========================================================
# CARTE
# =========================================================

elif menu == "🗺️ Carte des déchets":
    st.subheader("🗺️ Carte citoyenne des micro-déchets")
    st.caption("🔴 À ramasser · 🟢 Ramassé")

    df = st.session_state.dechets_db.copy()

    f1, f2, f3 = st.columns([1.2, 1.2, 1])
    with f1:
        statut_filter = st.multiselect(
            "Statut",
            ["🔴 À ramasser", "🟢 Ramassé"],
            default=["🔴 À ramasser", "🟢 Ramassé"],
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

    st.info(f"📍 {len(df)} signalement(s) affiché(s) sur la carte.")
    st_folium(build_map(df), width=None, height=560, returned_objects=[])

    st.markdown("### 🧤 Agir maintenant")
    st.caption("Si vous ramassez réellement un déchet, utilisez le bouton correspondant pour informer la communauté.")

    if df.empty:
        st.info("Aucun signalement ne correspond aux filtres.")
    else:
        for index, row in df.iterrows():
            col1, col2, col3 = st.columns([3.5, 2, 1.4])
            with col1:
                st.markdown(
                    f"**#{int(row['id'])} — {row['type']}**  \n"
                    f"📍 {row['adresse']} · 📅 {row['date']}"
                )
            with col2:
                st.write(f"Statut : **{row['statut']}**")
            with col3:
                if row["statut"] == "🔴 À ramasser":
                    if st.button("🧤 Je l'ai ramassé", key=f"ramassage_{int(row['id'])}"):
                        st.session_state.dechets_db.at[index, "statut"] = "🟢 Ramassé"
                        st.session_state.actions_ramassage.append(f"citoyen_{len(st.session_state.actions_ramassage)+1}")
                        st.success("Merci pour votre geste ! Le déchet est maintenant indiqué comme ramassé.")
                        st.rerun()
                else:
                    st.success("✓ Ramassé")

# =========================================================
# SIGNALER
# =========================================================

elif menu == "📸 Signaler un déchet":
    st.subheader("📸 Signaler un micro-déchet")
    st.write(
        "Vous avez repéré un déchet dans l'espace public ? Signalez-le pour que les autres citoyens puissent le voir."
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

        submitted = st.form_submit_button("🚨 Signaler ce déchet", use_container_width=True)

    if submitted:
        db = st.session_state.dechets_db
        nouvel_id = int(db["id"].max()) + 1 if not db.empty else 1
        nouvelle_ligne = {
            "id": nouvel_id,
            "type": type_dechet,
            "statut": "🔴 À ramasser",
            "lat": lat,
            "lng": lng,
            "adresse": secteur,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": description or "Aucune description.",
        }
        st.session_state.dechets_db = pd.concat(
            [db, pd.DataFrame([nouvelle_ligne])], ignore_index=True
        )
        st.success("🎉 Merci ! Votre signalement est maintenant visible sur la carte.")
        st.balloons()

# =========================================================
# IMPACT CITOYEN
# =========================================================

elif menu == "📊 Impact citoyen":
    st.subheader("📊 Impact citoyen")
    st.write("Découvrez l'impact collectif des habitants qui utilisent EcoClean.")

    df = st.session_state.dechets_db.copy()
    total, ramasses, restants, taux, contributeurs = get_counts(df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🗑️ Déchets signalés", total)
    c2.metric("🧤 Déchets ramassés", ramasses)
    c3.metric("🔴 Encore à ramasser", restants)
    c4.metric("♻️ Taux de nettoyage", f"{taux}%")

    st.markdown("---")

    left, right = st.columns(2)
    with left:
        st.markdown("### 📈 Déchets par type")
        if not df.empty:
            st.bar_chart(df["type"].value_counts())

    with right:
        st.markdown("### 📍 Signalements par secteur")
        if not df.empty:
            secteurs = df["adresse"].value_counts()
            st.bar_chart(secteurs)

    st.markdown("### 🌱 Message collectif")
    if ramasses:
        st.success(f"Bravo ! La communauté a déjà permis de retirer {ramasses} déchet(s) de l'espace public. 💚")
    else:
        st.info("Aucun ramassage n'a encore été enregistré. Le prochain geste peut être le vôtre ! 🧤")

    st.markdown("### 🏆 Contribution citoyenne")
    st.write(f"👥 Actions de ramassage enregistrées : **{len(st.session_state.actions_ramassage)}**")
    st.caption("Cette version prototype ne demande pas de compte personnel : les contributions sont comptabilisées anonymement.")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.caption(
    f"🌱 EcoClean Colomiers V3 · Plateforme citoyenne · {datetime.now().strftime('%d/%m/%Y')}"
)
