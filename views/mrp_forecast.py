import streamlit as st
import pandas as pd  # pip install pandas
import views.analysis_backend as analysis_backend
import views.mrp_backend as mrp_backend
import matplotlib.pyplot as plt
import numpy as np


file_path = "assets/mrp project data.xlsx"
sample_df = pd.read_excel(file_path)
df = analysis_backend.get_df(sample_df)
# st.dataframe(df)

_,low_transaction_item_list = analysis_backend.sum_overall_transaction(df)
monthly_txn_df = analysis_backend.monthly_transaction_df(df,low_transaction_item_list)
# st.dataframe(monthly_txn_df)



# Selection fields
left_col, right_col = st.columns(2)

with left_col:
    material_list = monthly_txn_df["Description"].unique().tolist()

    selected_material = st.selectbox('Get analysis for : ',material_list)
    material_table, pivot_table = mrp_backend.get_mrp(monthly_txn_df,selected_material)
    
with right_col:
    year = monthly_txn_df["Year"].unique().tolist()
    year.insert(0,'Overall')
    selected_year = st.selectbox("Select a Year for Transaction:", year)
    if selected_year != "Overall":
        material_table = material_table[material_table['Year'] ==  selected_year]
        monthly_txn_df = monthly_txn_df[monthly_txn_df["Year"] == selected_year]
        _,pivot_table = mrp_backend.get_mrp(monthly_txn_df,selected_material)





# -------------- taking input --------------------------------

col1, col2 = st.columns(2)

with col1:
    n = st.number_input("avg to top n transaction", min_value=1, step=1,max_value=24, value=3)
    demand_multiple_input = st.number_input("demand multiple input", min_value=1, step=1,max_value=10,  value=3)
    beg_invent_input = st.number_input("beg invent input", min_value=1, step=1,max_value=10,  value=6)

with col2:
    lotSize_input = st.number_input("lotSize input", min_value=1, step=1,max_value=10, value=6)
    safety_stock_input = st.number_input("safety stock input", min_value=1, step=1,max_value=10, value=3)
    lead_time = st.number_input("lead time", min_value=1, step=1,max_value=10, value=2)





# ------------- getting rough record and monthly usage -------------

mrp_record, monthly_usage = mrp_backend.create_mrp_record(material_table,n)
 # mrp_table = pd.DataFrame(data)
monthly_usage = round(monthly_usage,2)
st.subheader(f'Monthly Usage : {monthly_usage}')
st.markdown('---')



# ------ calculating input--------------------------------
st.write('## MRP Record and Forecasting')
demand = demand_multiple_input * monthly_usage
beg_inventory_q1 = beg_invent_input * monthly_usage
por_value = lotSize_input * monthly_usage
safety_stock = safety_stock_input * monthly_usage
lot_size = lotSize_input* monthly_usage



# --------- calling function for mrp -------------

mrp_table = mrp_backend.create_new_col(mrp_record,demand,beg_inventory_q1,lead_time)
# st.write(mrp_table)

mrp_table = mrp_backend.update_table(mrp_table,lead_time,safety_stock,por_value)
mrp_table = mrp_table.set_index('Period')
st.dataframe(mrp_table)

transpose_mrp = mrp_table.transpose()
st.dataframe(transpose_mrp)
st.markdown('---')




# --------- inventory plot ---------------------------

st.write('## Inventory Plot')
# Plotting the grouped bar chart
fig, ax = plt.subplots(figsize=(13, 5))

# Define bar width and positions
bar_width = 0.25
index = np.arange(len(transpose_mrp))

# Plot each category of data
bar1 = plt.bar(index - bar_width, transpose_mrp['Beg. Inventory'], bar_width, label='Beg. Inventory')
bar2 = plt.bar(index, transpose_mrp['End. Inventory'], bar_width, label='End. Inventory')
bar3 = plt.bar(index + bar_width, transpose_mrp['P.O.R'], bar_width, label='P. Order Release')

def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height != 0:
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 5),  # 5 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)  # Reduced font size for better fit

add_labels(bar1)
add_labels(bar2)
add_labels(bar3)

# Add labels, title, and legend
plt.xlabel('Quarters')
plt.ylabel('Quantity')
plt.title('Inventory (Quantity vs Time)')
plt.xticks(index, transpose_mrp.index)
plt.legend()

# Save the plot to a BytesIO object
import io
buf = io.BytesIO()
plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
buf.seek(0)

# Display the plot in Streamlit
st.image(buf, caption='Inventory Plot', use_column_width=True)

# Close the plot to avoid display in Streamlit
plt.close(fig)
st.markdown('---')






# -------- showing transaction dataframe-----------------------------------
col3, col4 = st.columns([2.2,1])

with col3:
    st.write('## Transaction Dataframe')
    table = material_table.reset_index(drop = True)
    table.index += 1
    if table.shape[0] >= 12:
        st.dataframe(table,height=455)

    else :
        
        st.dataframe(table)
    


with col4:
    st.write('## Table')
    if material_table.shape[0] >= 12:
        st.dataframe(pivot_table,height=455)

    else :
        st.dataframe(pivot_table)
