import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="EcoClean Colomiers", layout="wide", initial_sidebar_state="expanded")

COLOMIERS_COORDS = [43.6135, 1.3330]
PAGES = ["Accueil", "Carte", "Signaler un déchet", "Impact citoyen"]
PAGE_KEYS = {"home": PAGES[0], "carte": PAGES[1], "signaler": PAGES[2], "impact": PAGES[3]}

st.markdown("""
<style>
.block-container{padding-top:2rem;padding-bottom:2rem;max-width:1200px}
.hero{padding:2.2rem 2.4rem;border:1px solid #e4e7ec;border-radius:18px;background:linear-gradient(135deg,#f4faf6,#ffffff);margin-bottom:1.5rem}
.hero h1{font-size:2.7rem;margin:0 0 .5rem;font-weight:750;color:#183b2a}
.hero p{font-size:1.08rem;color:#667085;margin:0;max-width:760px}
.section-title{font-size:1.35rem;font-weight:700;color:#1d2939;margin:1.4rem 0 .7rem}
.small-muted{color:#667085;font-size:.92rem}
.status-pending{display:inline-block;padding:4px 10px;border-radius:999px;background:#fff1f0;color:#b42318;font-size:.85rem;font-weight:600}
.status-done{display:inline-block;padding:4px 10px;border-radius:999px;background:#ecfdf3;color:#027a48;font-size:.85rem;font-weight:600}
.footer{color:#98a2b3;font-size:.85rem;text-align:center;padding:1.5rem 0}
</style>
""", unsafe_allow_html=True)

DEMO_DATA = [
    {"id":1,"type":"Emballage alimentaire","statut":"À ramasser","lat":43.6145,"lng":1.3325,"adresse":"Près du Parc Duroch","date":"2026-09-01","description":"Déchet visible dans l'espace public."},
    {"id":2,"type":"Canette / bouteille plastique","statut":"À ramasser","lat":43.6110,"lng":1.3340,"adresse":"Axe Gare de Colomiers","date":"2026-09-02","description":"Déchet signalé par un citoyen."},
    {"id":3,"type":"Mégots","statut":"À ramasser","lat":43.6162,"lng":1.3352,"adresse":"Centre-ville / Vieux Colomiers","date":"2026-09-05","description":"Plusieurs mégots regroupés."},
    {"id":4,"type":"Emballages / papiers","statut":"À ramasser","lat":43.6122,"lng":1.3295,"adresse":"Secteur du Pigeonnier","date":"2026-09-06","description":"Petits emballages abandonnés."},
]

if "dechets_db" not in st.session_state:
    st.session_state.dechets_db = pd.DataFrame(DEMO_DATA)
if "actions_ramassage" not in st.session_state:
    st.session_state.actions_ramassage = 0


def counts(df):
    total = len(df)
    done = int((df["statut"] == "Ramassé").sum())
    pending = int((df["statut"] == "À ramasser").sum())
    rate = round(done / total * 100) if total else 0
    return total, pending, done, rate


def build_map(df):
    m = folium.Map(location=COLOMIERS_COORDS, zoom_start=15, control_scale=True, tiles="OpenStreetMap")
    folium.Marker(COLOMIERS_COORDS, tooltip="EcoClean Colomiers", popup="Plateforme citoyenne de signalement et de ramassage", icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    for _, row in df.iterrows():
        pending = row["statut"] == "À ramasser"
        color = "red" if pending else "green"
        popup = f"<div style='width:250px;font-family:Arial'><h4>{row['type']}</h4><b>Statut :</b> {row['statut']}<br><b>Lieu :</b> {row['adresse']}<br><b>Date :</b> {row['date']}<br><b>Description :</b> {row['description']}</div>"
        folium.Marker([row["lat"],row["lng"]], popup=folium.Popup(popup,max_width=330), tooltip=f"#{int(row['id'])} — {row['type']}", icon=folium.Icon(color=color,icon="trash",prefix="fa")).add_to(m)
    return m

page_key = st.query_params.get("page", "home")
menu_default = PAGE_KEYS.get(page_key, PAGES[0])

with st.sidebar:
    st.markdown("## EcoClean")
    st.caption("Plateforme citoyenne de Colomiers")
    st.divider()
    menu = st.radio("Navigation", PAGES, index=PAGES.index(menu_default))
    st.divider()
    st.caption("Signalez un déchet ou agissez sur un signalement existant.")

selected_key = next(k for k,v in PAGE_KEYS.items() if v == menu)
if selected_key != page_key:
    st.query_params["page"] = selected_key

if menu == PAGES[0]:
    total,pending,done,rate = counts(st.session_state.dechets_db)
    st.markdown("<div class='hero'><h1>EcoClean Colomiers</h1><p>Une plateforme citoyenne pour signaler les déchets présents dans l'espace public et permettre à chacun d'agir pour une ville plus propre.</p></div>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Signalements",total)
    c2.metric("À ramasser",pending)
    c3.metric("Ramassés",done)
    c4.metric("Taux de nettoyage",f"{rate}%")
    st.markdown("<div class='section-title'>Comment ça fonctionne ?</div>", unsafe_allow_html=True)
    a,b,c = st.columns(3)
    with a:
        st.markdown("**1. Signaler**")
        st.write("Repérez un déchet et indiquez son emplacement.")
    with b:
        st.markdown("**2. Localiser**")
        st.write("Le signalement apparaît sur la carte citoyenne.")
    with c:
        st.markdown("**3. Agir**")
        st.write("Un autre citoyen peut le ramasser et mettre à jour son statut.")
    st.markdown("<div class='section-title'>Agir maintenant</div>", unsafe_allow_html=True)
    st.write("Consultez les déchets actuellement signalés et choisissez ceux que vous pouvez ramasser.")
    x,y = st.columns(2)
    with x:
        if st.button("Voir les déchets à ramasser →",use_container_width=True,type="primary"):
            st.query_params["page"]="carte"
            st.query_params["filtre"]="a_ramasser"
            st.rerun()
    with y:
        if st.button("Signaler un déchet",use_container_width=True):
            st.query_params["page"]="signaler"
            st.query_params.pop("filtre",None)
            st.rerun()

elif menu == PAGES[1]:
    st.title("Carte des déchets")
    st.caption("Les marqueurs rouges correspondent aux déchets à ramasser. Les marqueurs verts indiquent les déchets déjà ramassés.")
    df = st.session_state.dechets_db.copy()
    pending_only = st.query_params.get("filtre") == "a_ramasser"
    default_status = ["À ramasser"] if pending_only else ["À ramasser","Ramassé"]
    f1,f2,f3 = st.columns([1,1,1])
    with f1: statut_filter = st.multiselect("Statut",["À ramasser","Ramassé"],default=default_status)
    with f2: type_filter = st.multiselect("Type de déchet",sorted(df["type"].unique()))
    with f3: secteur_filter = st.multiselect("Secteur",sorted(df["adresse"].unique()))
    if statut_filter: df=df[df["statut"].isin(statut_filter)]
    if type_filter: df=df[df["type"].isin(type_filter)]
    if secteur_filter: df=df[df["adresse"].isin(secteur_filter)]
    st.info(f"{len(df)} signalement(s) affiché(s).")
    st_folium(build_map(df),width=None,height=540,returned_objects=[])
    st.markdown("<div class='section-title'>Signalements</div>",unsafe_allow_html=True)
    for index,row in df.iterrows():
        with st.container(border=True):
            col1,col2,col3 = st.columns([3.4,1.5,1.4])
            with col1:
                st.markdown(f"**#{int(row['id'])} — {row['type']}**")
                st.caption(f"{row['adresse']} · Signalé le {row['date']}")
            with col2:
                cls="status-pending" if row["statut"]=="À ramasser" else "status-done"
                st.markdown(f"<span class='{cls}'>{row['statut']}</span>",unsafe_allow_html=True)
            with col3:
                if row["statut"]=="À ramasser":
                    if st.button("Marquer comme ramassé",key=f"ramassage_{int(row['id'])}",use_container_width=True):
                        st.session_state.dechets_db.at[index,"statut"]="Ramassé"
                        st.session_state.actions_ramassage += 1
                        st.rerun()
                else:
                    st.caption("Action terminée")

elif menu == PAGES[2]:
    st.title("Signaler un déchet")
    st.write("Décrivez simplement le déchet et indiquez où il se trouve. Il sera ajouté à la carte.")
    with st.form("form_signalement",clear_on_submit=True):
        col1,col2=st.columns(2)
        with col1:
            type_dechet=st.selectbox("Type de déchet",["Emballage alimentaire","Canette / bouteille plastique","Mégots","Emballages / papiers","Déchet recyclable","Autre déchet"])
        with col2:
            secteur=st.selectbox("Secteur de Colomiers",["Vieux Colomiers (Centre historique)","Parc Duroch","Axe Gare de Colomiers / Bus","Secteur du Pigeonnier","Autre secteur de proximité"])
        a,b=st.columns(2)
        with a: lat=st.number_input("Latitude",43.50,43.70,float(COLOMIERS_COORDS[0]),format="%.5f")
        with b: lng=st.number_input("Longitude",1.20,1.50,float(COLOMIERS_COORDS[1]),format="%.5f")
        description=st.text_area("Description (facultatif)",placeholder="Ex. : plusieurs emballages près d'un banc.")
        submitted=st.form_submit_button("Signaler ce déchet",use_container_width=True,type="primary")
    if submitted:
        db=st.session_state.dechets_db
        new_id=int(db["id"].max())+1 if not db.empty else 1
        row={"id":new_id,"type":type_dechet,"statut":"À ramasser","lat":lat,"lng":lng,"adresse":secteur,"date":datetime.now().strftime("%Y-%m-%d"),"description":description or "Aucune description."}
        st.session_state.dechets_db=pd.concat([db,pd.DataFrame([row])],ignore_index=True)
        st.success("Votre signalement a été ajouté à la carte.")

elif menu == PAGES[3]:
    st.title("Impact citoyen")
    df=st.session_state.dechets_db.copy()
    total,pending,done,rate=counts(df)
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Signalements",total)
    c2.metric("À ramasser",pending)
    c3.metric("Ramassés",done)
    c4.metric("Taux de nettoyage",f"{rate}%")
    st.markdown("<div class='section-title'>État des signalements</div>",unsafe_allow_html=True)
    chart=df["statut"].value_counts().rename_axis("Statut").to_frame("Nombre")
    st.bar_chart(chart)
    st.caption(f"Actions de ramassage enregistrées dans cette session : {st.session_state.actions_ramassage}.")

st.markdown("<div class='footer'>EcoClean Colomiers · Version Beta v1 · Plateforme citoyenne de signalement et de ramassage</div>",unsafe_allow_html=True)
