import pandas as pd
import streamlit as st
import joblib
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import warnings
from streamlit_navigation_bar import st_navbar
from pathlib import Path

st.set_page_config(page_title="Prédiction de note restaurant", layout="wide",initial_sidebar_state="collapsed")
st.sidebar.caption("Sélectionnez une page")
st.markdown(
    """
    <h2 style="text-align: center;">Prédiction de note restaurant</h2>
    <p style="text-align: center; font-size: 16px;">
        👉 Ce site est un outil d’aide à la décision et de visualisation de Machine Learning, qui permet de simuler l’influence de différents critères sur la note d’un restaurant.
    </p>
    """,
    unsafe_allow_html=True
)

def format_func(option):
    if option == 1:
        return "Oui"
    else:
        return "Non"
    
def format_func2(option):
    if option == 1:
        return "Économique"
    elif option == 2:
        return "Prix modérés"
    elif option == 3:
        return "Haut de gamme"
    else:
        return "Luxe"
    

######################################## MACHINE LEARNING ########################################

BASE_DIR = Path(__file__).resolve().parent  # dossier où se trouve 1_Prediction.py

model = joblib.load(BASE_DIR / "mon_modele.pkl")

df = pd.read_csv(BASE_DIR / "P3_ML3v6.csv")

df_num = df.select_dtypes(include='number')

X = df_num.drop(['stars'], axis=1)
y = df_num["stars"]
weights = df["review_count"]

X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(X, y, weights, test_size=0.2, random_state=42)

pipeline_reg = Pipeline(steps=[('scaler', StandardScaler()),
                               ('regressor', LinearRegression())])


pipeline_reg.fit(X_train, y_train, regressor__sample_weight=w_train)

y_pred_test = pipeline_reg.predict(X_test)
y_pred_train = pipeline_reg.predict(X_train)


def predict_stars(state, category, price_range,
                  outdoor_seating,
                  restaurant_delivery,
                  restaurants_takeout,
                  pipeline, X_columns):
    """
    state : str (ex: 'CA')
    category : str (ex: 'Mexican')
    price_range : int (1 à 4)
    outdoor_seating : int (1 ou 0)
    restaurant_delivery : int (1 ou 0)
    restaurants_takeout : int (1 ou 0)
    pipeline : pipeline entraîné
    X_columns : X_train.columns
    """

    # Initialiser une ligne vide
    x_input = pd.Series(0, index=X_columns)

    # State (one-hot)
    if state in x_input.index:
        x_input[state] = 1
    else:
        print(f"⚠️ State '{state}' inconnu")

    # Category (one-hot)
    if category in x_input.index:
        x_input[category] = 1
    else:
        print(f"⚠️ Catégorie '{category}' inconnue")

    # Price range
    if "RestaurantsPriceRange2" in x_input.index:
        x_input["RestaurantsPriceRange2"] = price_range

    # Outdoor seating
    if "OutdoorSeating" in x_input.index:
        x_input["OutdoorSeating"] = outdoor_seating

    # Restaurant delivery
    if "RestaurantsDelivery" in x_input.index:
        x_input["RestaurantsDelivery"] = restaurant_delivery

    # Restaurants takeout
    if "RestaurantsTakeOut" in x_input.index:
        x_input["RestaurantsTakeOut"] = restaurants_takeout

    # DataFrame (1 ligne)
    x_input_df = pd.DataFrame([x_input])

    # Prédiction
    stars_pred = pipeline.predict(x_input_df)[0]

    return stars_pred

######################################## AFFICHAGE ########################################

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Critères")

    with st.container(border=True):
        choix_category = st.selectbox("Type de restaurant", df.columns[6:72])
        choix_state = st.selectbox("Localisation", df["state"].unique())

        choix_price = st.selectbox(
            "Prix du restaurant",
            sorted(df["RestaurantsPriceRange2"].dropna().unique()),
            format_func=format_func2
        )
        temp_moy = df.loc[df["state"] == choix_state,"tavg_moyenne"].iloc[0] 
        terrasse = int(st.toggle("Terrasse", value=False))
        if terrasse:
            st.info(f"Température moyenne à l'année : **{temp_moy:.1f}** °C")

        orga_livraison = df.loc[df["state"] == choix_state,"Services de livraison"].iloc[0] 
        livraison = int(st.toggle("Livraison", value=False))
        if livraison:
            st.info(f"Service de livraison disponibles : **{orga_livraison}**")

        emporter = int(st.toggle("Plat à emporter", value=False))

        st.divider()

        prediction = st.button("Prédire ⭐", use_container_width=True)

with right:
    st.subheader("Résultat")

    with st.container(border=True):
        if prediction:
            stars = predict_stars(
                state=choix_state,
                category=choix_category,
                price_range=int(choix_price),
                outdoor_seating=terrasse,
                restaurant_delivery=livraison,
                restaurants_takeout=emporter,
                pipeline=pipeline_reg,
                X_columns=X_train.columns
            )
            
            stars_terrasse = predict_stars(
                state=choix_state,
                category=choix_category,
                price_range=int(choix_price),
                outdoor_seating=0,
                restaurant_delivery=livraison,
                restaurants_takeout=emporter,
                pipeline=pipeline_reg,
                X_columns=X_train.columns
            )
            stars_livraison = predict_stars(
                state=choix_state,
                category=choix_category,
                price_range=int(choix_price),
                outdoor_seating=terrasse,
                restaurant_delivery=0,
                restaurants_takeout=emporter,
                pipeline=pipeline_reg,
                X_columns=X_train.columns
            )
            stars_emporter = predict_stars(
                state=choix_state,
                category=choix_category,
                price_range=int(choix_price),
                outdoor_seating=terrasse,
                restaurant_delivery=livraison,
                restaurants_takeout=0,
                pipeline=pipeline_reg,
                X_columns=X_train.columns
            )
            impact_terrasse = stars - stars_terrasse
            impact_livraison = stars - stars_livraison
            impact_emporter = stars - stars_emporter


            st.metric("⭐ Note prédite", f"{stars:.2f} / 5")
            if terrasse:
             st.write(f"Impact de la **Terrasse** sur la note : {impact_terrasse:+.2f} ⭐")
            if livraison:
             st.write(f"Impact de la **Livraison** sur la note : {impact_livraison:+.2f} ⭐")
            if emporter:
             st.write(f"Impact des **Plats à emporter** sur la note : {impact_emporter:+.2f} ⭐")


            # petit feedback visuel
            if stars >= 4.0:
                st.success("Très bon potentiel !")
            elif stars >= 3.5:
                st.success("Potentiel correct !")
            else:
                st.warning("Potentiel plus faible !")
        else:
            st.success("Sélectionne tes critères puis clique sur **Prédire ⭐**")   

