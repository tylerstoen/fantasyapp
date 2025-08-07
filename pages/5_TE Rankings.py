import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("TE Rankings")
st.markdown("Here you can view and reorder the TE rankings. Drag and drop players to adjust their rankings as needed. " \
            "The table below tracks your live updated rankings. Hover the **top right** corner of the table to download.")


data = pd.read_csv("updated_rankings.csv")
te_data = data[data["Pos"] == "TE"]
te_data = te_data[["Pos Rank", "Player", "Pos", "Team", "ADP", "Bye", "Notes"]]  # Remove the original Rank column
if "reordered_te" not in st.session_state:
    st.session_state.reordered_te = te_data
else:
    te_data = st.session_state.reordered_te


te_data["id"] = te_data.index  # Add an id column for tracking

# Set up grid options with row drag enabled
gb = GridOptionsBuilder.from_dataframe(te_data)
gb.configure_grid_options(domLayout='normal')
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Player", rowDrag=True)  # Enable drag on Player column
gb.configure_column("id", hide=True)  # Hide the tracking column
gb.configure_column("Player", width=400)
gb.configure_grid_options(rowDragManaged=True, animateRows=True)
gb.configure_grid_options(getRowNodeId="data.id")  # Track row by id

grid_response = AgGrid(
    te_data,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode="AS_INPUT",
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    height=500,
    width="100%",
)

reordered_te = pd.DataFrame(grid_response["data"]).reset_index(drop=True)
reordered_te["Pos Rank"] = range(1, len(reordered_te) + 1)  # ✅ Live-updating position rank
reordered_te.drop(columns=["id"], inplace=True)  # Hide internal ID

st.session_state.reordered_te = reordered_te
st.write("📊 Reordered Table (Live Updated):")
st.dataframe(reordered_te.reset_index(drop=True))

# if st.button("Save Rankings"):
#     st.session_state.reordered_te = reordered_te
#     st.success("Rankings saved successfully!")


