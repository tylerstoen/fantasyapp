import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("RB Rankings")
st.markdown("Here you can view and reorder the RB rankings. Drag and drop players to adjust their rankings as needed. " \
            "The table below tracks your live updated rankings. Hover the **top right** corner of the table to download.")


data = pd.read_csv("updated_rankings.csv")
rb_data = data[data["Pos"] == "RB"]
rb_data = rb_data[["Pos Rank", "Player", "Pos", "Team", "ADP", "Bye", "Notes"]]  # Remove the original Rank column
if "reordered_rb" not in st.session_state:
    st.session_state.reordered_rb = rb_data
else:
    rb_data = st.session_state.reordered_rb


rb_data["id"] = rb_data.index  # Add an id column for tracking

# Set up grid options with row drag enabled
gb = GridOptionsBuilder.from_dataframe(rb_data)
gb.configure_grid_options(domLayout='normal')
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Player", rowDrag=True)  # Enable drag on Player column
gb.configure_column("id", hide=True)  # Hide the tracking column
gb.configure_column("Player", width=400)
gb.configure_grid_options(rowDragManaged=True, animateRows=True)
gb.configure_grid_options(getRowNodeId="data.id")  # Track row by id

grid_response = AgGrid(
    rb_data,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode="AS_INPUT",
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    height=500,
    width="100%",
)

reordered_rb = pd.DataFrame(grid_response["data"]).reset_index(drop=True)
reordered_rb["Pos Rank"] = range(1, len(reordered_rb) + 1)  # ✅ Live-updating position rank
reordered_rb.drop(columns=["id"], inplace=True)  # Hide internal ID

st.session_state.reordered_rb = reordered_rb
st.write("📊 Your RB Rankings Table (Live Updated):")
st.dataframe(reordered_rb.reset_index(drop=True))

# if st.button("Save Rankings"):
#     st.session_state.reordered_rb = reordered_rb
#     st.success("Rankings saved successfully!")


