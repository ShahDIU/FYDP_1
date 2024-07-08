import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors  # Import KNN

# Load the DataFrame globally
df = pd.read_csv("fifaratings.csv")

# Page for Find Position using KNN
def find_position():
    st.subheader("FIND POSITION")

    st.text("Rate yourself between 1 and 100 for the following statistics:")

    stats = [
        "Overall", "Potential", "Pace Total", "Shooting Total", "Passing Total",
        "Dribbling Total", "Defending Total", "Physicality Total", "Crossing",
        "Finishing", "Freekick Accuracy", "BallControl", "Acceleration", "Reactions",
        "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking",
        "Goalkeeper Diving", "Goalkeeper Handling", " GoalkeeperKicking", "Goalkeeper Reflexes"
    ]

    user_inputs = {}
    for stat in stats:
        user_inputs[stat] = st.slider(f"{stat}:", min_value=1, max_value=100, value=50)

    if st.button("Submit"):
        user_data = pd.DataFrame([user_inputs])

        # Select the relevant stats columns from the dataset
        knn_data = df[stats]

        # Fit KNN model
        knn = NearestNeighbors(n_neighbors=1)
        knn.fit(knn_data)

        # Find the closest match
        distances, indices = knn.kneighbors(user_data)
        best_match = df.iloc[indices[0][0]]

        st.subheader("Output:")
        st.text(f"Position: {best_match['Best Position']}")
        st.text(f"Name: {best_match['Full Name']}")
        st.text(f"Age: {best_match['Age']}")
        st.text(f"Nationality: {best_match['Nationality']}")
        st.text(f"Overall: {best_match['Overall']}")
        st.image(best_match['Image Link'], caption="Player Image")

# Page for Find Similar Player
def find_similar_player():
    st.subheader("FIND SIMILAR PLAYER")

    positions = ["Forward", "Middle", "Backward"]
    preferred_position = st.selectbox("Preferred Position:", positions)

    if preferred_position in ["Forward", "Middle", "Backward"]:
        stats = ["Pace Total", "Shooting Total", "Passing Total", "Dribbling Total",
                 "Physicality Total", "Crossing", "Finishing", "Freekick Accuracy", "BallControl",
                 "Acceleration", "Reactions", "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking"]

    user_inputs = {}
    for stat in stats:
        user_inputs[stat] = st.slider(f"{stat}:", min_value=1, max_value=100, value=50)

    if st.button("Submit"):
        user_data = pd.DataFrame([user_inputs])

        # Select the relevant stats columns from the dataset
        knn_data = df[stats]

        # Fit KNN model
        knn = NearestNeighbors(n_neighbors=1)
        knn.fit(knn_data)

        # Find the closest match
        distances, indices = knn.kneighbors(user_data)
        best_match = df.iloc[indices[0][0]]

        st.subheader("Output:")

        comparison_stats = ["Pace Total", "Shooting Total", "Passing Total", "Dribbling Total",
                            "Physicality Total", "Crossing", "Finishing", "Freekick Accuracy", "BallControl",
                            "Acceleration", "Reactions", "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking"]
        comparison_data = {
            "Stat": comparison_stats,
            "User Data": [user_inputs[stat] for stat in comparison_stats],
            "Similar Player": [best_match[stat] for stat in comparison_stats]
        }
        comparison_df = pd.DataFrame(comparison_data)

        col1, col2 = st.columns(2)

        with col1:
            st.image(best_match['Image Link'], caption="Similar Player")
            st.text(f"Position: {best_match['Best Position']}")
            st.text(f"Name: {best_match['Full Name']}")
            st.text(f"Age: {best_match['Age']}")
            st.text(f"Nationality: {best_match['Nationality']}")
            st.text(f"Overall: {best_match['Overall']}")
            st.text(f"Potential: {best_match['Potential']}")

        with col2:
            st.subheader("User Data")
            st.write(user_data.T)

        st.subheader("Comparison")
        st.table(comparison_df)

# Page for Know Player
def know_player():
    st.subheader("KNOW PLAYER")
    player_names = df['Known As']
    selected_player = st.selectbox("Select a player:", player_names)
    selected_row = df[df['Known As'] == selected_player]

    if st.button("Show Player Data"):
        st.subheader(f"Player Details: {selected_player}")
        st.text(f"Name: {selected_row['Full Name'].values[0]}")
        st.text(f"Age: {selected_row['Age'].values[0]}")
        st.text(f"Overall: {selected_row['Overall'].values[0]}")
        st.text(f"Potential: {selected_row['Potential'].values[0]}")
        st.text(f"Pace Total: {selected_row['Pace Total'].values[0]}")
        st.text(f"Passing Total: {selected_row['Passing Total'].values[0]}")
        st.text(f"Shooting Total: {selected_row['Shooting Total'].values[0]}")
        st.text(f"Nationality: {selected_row['Nationality'].values[0]}")

        st.image(selected_row['Image Link'].values[0], caption="Player Image")

    if st.button("Show Full Details"):
        st.write(selected_row)

def comparison_page():
    st.subheader("Comparison With Your Dream Player:")

    st.text("Rate yourself between 1 and 100 for the following statistics:")

    user_inputs = {}
    for stat in ["Pace Total", "Shooting Total", "Passing Total", "Dribbling Total", "Physicality Total",
                 "Crossing", "Finishing", "Freekick Accuracy", "BallControl", "Acceleration", "Reactions",
                 "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking"]:
        user_inputs[stat] = st.slider(stat, min_value=1, max_value=100, value=50)

    st.subheader("Select Dream Player")
    dream_player_options = df['Known As'].tolist()
    selected_dream_player = st.selectbox("Select a Dream Player:", dream_player_options)

    if st.button("Compare"):
        dream_player_data = df[df['Known As'] == selected_dream_player].squeeze()

        comparison_stats = ["Pace Total", "Shooting Total", "Passing Total", "Dribbling Total", "Physicality Total",
                            "Crossing", "Finishing", "Freekick Accuracy", "BallControl", "Acceleration", "Reactions",
                            "Balance", "Shot Power", "Stamina", "Vision", "Penalties", "Marking"]
        comparison_data = {
            "Stat": comparison_stats,
            "User Data": [user_inputs[stat] for stat in comparison_stats],
            "Dream Player": [dream_player_data[stat] for stat in comparison_stats]
        }
        comparison_df = pd.DataFrame(comparison_data)

        st.subheader("Comparison Result:")
        st.table(comparison_df)

# Main option page
def option_page():
    st.title("OPTIONS")
    option = st.radio("Choose an option:", ["FIND POSITION", "FIND SIMILAR PLAYER", "KNOW PLAYER", "COMPARISON"])

    if option == "FIND POSITION":
        find_position()
    elif option == "FIND SIMILAR PLAYER":
        find_similar_player()
    elif option == "KNOW PLAYER":
        know_player()
    elif option == "COMPARISON":
        comparison_page()

# Main function to run the app
def main():
    option_page()

if __name__ == "__main__":
    main()


