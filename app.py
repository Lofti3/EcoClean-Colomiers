import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="EcoClean Colomiers",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# BASE DE DONNÉES
# ---------------------------------------------------------

if "dechets_db" not in st.session_state:
    st.session_state.dechets_db = pd.DataFrame([
        {
            "id": 1,
            "type": "🧃 Gourde de compote / Emballage gâteau",
            "statut": "🔴 À ramasser",
            "lat": 43.6145,
            "lng": 1.3325,
            "adresse": "Près du Parc Duroch",
            "date": "2026-09-01"
        },
        {
            "id": 2,
            "type": "🥤 Canette / Bouteille plastique",
            "statut": "🟢 Ramassé !",
            "lat": 43.6110,
            "lng": 1.3340,
            "adresse": "Axe Gare de Colomiers",
            "date": "2026-09-02"
        }
    ])

COLOMIERS_COORDS = [43.6135, 1.3330]

# ---------------------------------------------------------
# TITRE
# ---------------------------------------------------------

st.title("🌱 EcoClean Colomiers")

st.subheader(
    "L'application citoyenne de lutte contre les micro-déchets"
)

st.markdown("---")

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------

menu = st.sidebar.radio(
    "🧭 Navigation",
    [
        "🗺️ Carte des micro-déchets",
        "📸 Signaler un déchet",
        "📊 Statistiques d'impact"
    ]
)

# =========================================================
# PAGE 1 : CARTE
# =========================================================

if menu == "🗺️ Carte des micro-déchets":

    st.subheader("📍 Micro-déchets signalés à Colomiers")

    st.info(
        "Consultez la carte avant votre promenade. "
        "Si vous ramassez un déchet, vous pouvez mettre son statut à jour."
    )

    # Création de la carte
    m = folium.Map(
        location=COLOMIERS_COORDS,
        zoom_start=15,
        control_scale=True
    )

    # Ajout des déchets sur la carte
    for _, row in st.session_state.dechets_db.iterrows():

        if row["statut"] == "🔴 À ramasser":
            couleur = "red"
        else:
            couleur = "green"

        popup_html = f"""
        <div style="width:220px">
            <b>{row['type']}</b><br><br>
            <b>Statut :</b> {row['statut']}<br>
            <b>Lieu :</b> {row['adresse']}<br>
            <b>Date :</b> {row['date']}
        </div>
        """

        folium.Marker(
            location=[row["lat"], row["lng"]],
            popup=folium.Popup(
                popup_html,
                max_width=300
            ),
            tooltip=row["type"],
            icon=folium.Icon(
                color=couleur,
                icon="trash",
                prefix="fa"
            )
        ).add_to(m)

    # Affichage de la carte
    st_folium(
        m,
        width=None,
        height=500,
        returned_objects=[]
    )

    # -----------------------------------------------------
    # ACTIONS DE RAMASSAGE
    # -----------------------------------------------------

    st.markdown("### 🛠️ Actions de ramassage")

    df_affiche = st.session_state.dechets_db.copy()

    if df_affiche.empty:

        st.info(
            "Aucun déchet signalé pour le moment."
        )

    else:

        for index, row in df_affiche.iterrows():

            col1, col2, col3 = st.columns(
                [3, 2, 1]
            )

            with col1:

                st.markdown(
                    f"**{row['type']}**  \n"
                    f"📍 {row['adresse']} — 📅 {row['date']}"
                )

            with col2:

                st.markdown(
                    f"Statut : **{row['statut']}**"
                )

            with col3:

                if row["statut"] == "🔴 À ramasser":

                    if st.button(
                        "✅ Ramassé",
                        key=f"ramassage_{row['id']}"
                    ):

                        st.session_state.dechets_db.at[
                            index,
                            "statut"
                        ] = "🟢 Ramassé !"

                        st.success(
                            "Déchet marqué comme ramassé !"
                        )

                        st.rerun()


# =========================================================
# PAGE 2 : SIGNALER UN DÉCHET
# =========================================================

elif menu == "📸 Signaler un déchet":

    st.subheader("📸 Signaler un micro-déchet")

    st.markdown(
        "Vous observez un petit déchet dans l'espace public ? "
        "Ajoutez-le à la carte EcoClean Colomiers."
    )

    with st.form(
        "form_signalement",
        clear_on_submit=True
    ):

        # Type de déchet
        type_dechet = st.selectbox(
            "🗑️ Quel type de micro-déchet ?",
            [
                "🧃 Gourde de compote / Emballage gâteau",
                "🥤 Canette / Bouteille plastique",
                "🚬 Mégots groupés",
                "🍬 Emballage de bonbon / Papiers",
                "♻️ Autre déchet recyclable",
                "🗑️ Autre déchet"
            ]
        )

        # Secteur
        secteur = st.selectbox(
            "📍 Secteur de Colomiers",
            [
                "Vieux Colomiers (Centre historique)",
                "Parc Duroch",
                "Axe Gare de Colomiers / Bus",
                "Autre secteur de proximité"
            ]
        )

        st.markdown(
            "### 📌 Position du signalement"
        )

        col_lat, col_lng = st.columns(2)

        # Latitude
        with col_lat:

            lat = st.number_input(
                "Latitude",
                min_value=43.50,
                max_value=43.70,
                value=43.6135,
                format="%.4f"
            )

        # Longitude
        with col_lng:

            lng = st.number_input(
                "Longitude",
                min_value=1.20,
                max_value=1.50,
                value=1.3330,
                format="%.4f"
            )

        # Bouton
        submit = st.form_submit_button(
            "🚨 Valider le signalement"
        )

        # Enregistrement
        if submit:

            if st.session_state.dechets_db.empty:

                nouvel_id = 1

            else:

                nouvel_id = (
                    int(
                        st.session_state.dechets_db["id"].max()
                    ) + 1
                )

            nouvel_enregistrement = {

                "id": nouvel_id,

                "type": type_dechet,

                "statut": "🔴 À ramasser",

                "lat": lat,

                "lng": lng,

                "adresse": secteur,

                "date": datetime.now().strftime(
                    "%Y-%m-%d"
                )
            }

            nouveau_dechet = pd.DataFrame(
                [nouvel_enregistrement]
            )

            st.session_state.dechets_db = pd.concat(
                [
                    st.session_state.dechets_db,
                    nouveau_dechet
                ],
                ignore_index=True
            )

            st.success(
                "🎉 Merci ! Votre signalement a été ajouté "
                "à la carte EcoClean Colomiers."
            )


# =========================================================
# PAGE 3 : STATISTIQUES
# =========================================================

elif menu == "📊 Statistiques d'impact":

    st.subheader(
        "📊 Tableau de bord — Impact environnemental"
    )

    st.markdown(
        "Ces données peuvent permettre d'identifier les zones "
        "où les micro-déchets sont les plus fréquents."
    )

    # Total
    total = len(
        st.session_state.dechets_db
    )

    # Déchets ramassés
    ramasses = len(
        st.session_state.dechets_db[
            st.session_state.dechets_db["statut"]
            == "🟢 Ramassé !"
        ]
    )

    # Déchets restants
    restants = len(
        st.session_state.dechets_db[
            st.session_state.dechets_db["statut"]
            == "🔴 À ramasser"
        ]
    )

    # Indicateurs
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🗑️ Total signalés",
        total
    )

    col2.metric(
        "🟢 Total nettoyés",
        ramasses
    )

    col3.metric(
        "🔴 En attente",
        restants
    )

    st.markdown("---")

    st.write(
        "### 📈 Répartition par type de déchet"
    )

    if not st.session_state.dechets_db.empty:

        repartition = (
            st.session_state.dechets_db["type"]
            .value_counts()
        )

        st.bar_chart(
            repartition
        )

    else:

        st.info(
            "Aucune donnée disponible."
        )


# =========================================================
# PIED DE PAGE
# =========================================================

st.markdown("---")

st.caption(
    "🌱 EcoClean Colomiers — Prototype citoyen "
    "de sensibilisation et de lutte contre les micro-déchets."
)
