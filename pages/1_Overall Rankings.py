import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("Overall Player Rankings")

st.markdown(
    "Here you can view and reorder the overall player rankings. "
    "Drag and drop players to adjust their rankings as needed. "
    "Hover over the table generated below to download your custom ranking order. " \
    "**All rankings are based on half PPR scoring.**"
)

# Load original data from file
original_data = pd.read_csv("updated_rankings_8-8.csv")
original_data["id"] = original_data.index  # unique row ID for AgGrid

# Load from session state or fall back to original
if "reordered_overall" not in st.session_state:
    st.session_state.reordered_overall = original_data.copy()

# Use working data for drag-and-drop session
working_data = st.session_state.reordered_overall.copy()
working_data["id"] = working_data.index  # Ensure ID is always there

# Set up grid options
gb = GridOptionsBuilder.from_dataframe(working_data)
gb.configure_grid_options(domLayout='normal')
gb.configure_selection("single", use_checkbox=False)
gb.configure_column("Player", rowDrag=True, width=600)
gb.configure_column("id", hide=True)
gb.configure_grid_options(rowDragManaged=True, animateRows=True)
gb.configure_grid_options(getRowNodeId="data.id")

grid_response = AgGrid(
    working_data,
    gridOptions=gb.build(),
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode="AS_INPUT",
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=False,
    height=500,
    width="100%",
)

live_df = pd.DataFrame(grid_response["data"]).drop(columns=["id"])

# Add dynamic overall and position ranks
live_df.insert(0, "Personal Rank", range(1, len(live_df) + 1))


live_df["Pos Rank"] = live_df.groupby("Pos").cumcount() + 1

# Display live rankings
st.write("🟢 Your Updated Rankings (Live View):")
st.dataframe(live_df[["Personal Rank", "Player", "Pos", "Team", "ADP", "Pos Rank", "Rank", "Bye", "Notes"]].reset_index(drop=True), hide_index=True)

# Save on button click
# if st.button("Save Rankings"):
#     st.session_state.reordered_overall = live_df.copy()
#     st.success("✅ Rankings saved successfully!")

# Display last saved version
# st.write("💾 Last Saved Rankings:")
# st.dataframe(st.session_state.reordered_overall)

# st.write("🟢 Live Drag-and-Drop View (not saved yet):")
# st.dataframe(pd.DataFrame(grid_response["data"]).drop(columns=["id"]))

# if st.button("Save Rankings"):
#     st.session_state.reordered_overall = pd.DataFrame(grid_response["data"]).drop(columns=["id"]).copy()
#     st.success("✅ Rankings saved successfully!")

# st.write("💾 Last Saved Rankings:")
# st.dataframe(st.session_state.reordered_overall)
