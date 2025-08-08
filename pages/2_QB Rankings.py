import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("QB Rankings")
st.markdown("Here you can view and reorder the QB rankings. Drag and drop players to adjust their rankings as needed. " \
            "The table below tracks your live updated rankings. Hover the **top right** corner of the table to download.")


data = pd.read_csv("updated_rankings.csv")
qb_data = data[data["Pos"] == "QB"]
qb_data = qb_data[["Pos Rank", "Player", "Pos", "Team", "ADP", "Bye", "Notes"]] # Remove the original Rank column
if "reordered_qb" not in st.session_state:
    st.session_state.reordered_qb = qb_data
else:
    qb_data = st.session_state.reordered_qb


qb_data["id"] = qb_data.index  # Add an id column for tracking

# Set up grid options with row drag enabled
gb = GridOptionsBuilder.from_dataframe(qb_data)
gb.configure_grid_options(domLayout='normal')
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Player", rowDrag=True)  # Enable drag on Player column
gb.configure_column("id", hide=True)  # Hide the tracking column
gb.configure_column("Player", width=400)
gb.configure_grid_options(rowDragManaged=True, animateRows=True)
gb.configure_grid_options(getRowNodeId="data.id")  # Track row by id

grid_response = AgGrid(
    qb_data,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode="AS_INPUT",
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    height=500,
    width="100%",
)

reordered_qb = pd.DataFrame(grid_response["data"]).reset_index(drop=True)
reordered_qb["Pos Rank"] = range(1, len(reordered_qb) + 1)  # ✅ Live-updating position rank
reordered_qb.drop(columns=["id"], inplace=True)  # Hide internal ID

st.session_state.reordered_qb = reordered_qb[["Pos Rank", "Player", "Pos", "Team", "ADP", "Bye", "Notes"]]
st.write("📊 Your QB Rankings Table (Live Updated):")
st.dataframe(reordered_qb.reset_index(drop=True), hide_index=True)

# if st.button("Save Rankings"):
#     st.session_state.reordered_qb = reordered_qb
#     st.success("Rankings saved successfully!")


