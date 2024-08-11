import views.analysis_backend as analysis_backend
# ,hpage2
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


file_path = "assets/mrp project data.xlsx"
sample_df = pd.read_excel(file_path)
    
            
        

# ********* Load the data *********************************
        
sample_df.index += 1  # Adjust index to start from 1
df = analysis_backend.get_df(sample_df)

# first section to display basic information ***************

col1,col2 = st.columns([2,1])

with col1:
       st.write("# **Basic Information**")

with col2:
       chemical_list = df['Description'].sort_values().unique().tolist()
       
       chemical_list.insert(0,'Overall')
       select_material = st.selectbox('Select Chemical',chemical_list)
       if select_material != 'Overall':
              df = df[df['Description'] == select_material]
       

       
# getting the overall transaction list and low transaction item list

total_transaction_df,low_transaction_item_list = analysis_backend.sum_overall_transaction(df)     

st.markdown("---")
# Use columns for side-by-side content
col1, col2 = st.columns(2,vertical_alignment="top")

with col1:
        # Display total number of unique items
        st.write("## Total Number of Chemicals")
        st.write(f"### **{sample_df['Description'].nunique()}**")
        st.markdown("---")

        # Display total number of transactions
        st.write("## Total Number of Transactions")
        st.write(f"### **{df.shape[0]}**")
        st.markdown("---")

        # Display total amount of material transferred
        st.write("## Total Amount of Material Transferred")
        st.write(f"### **{df['TransactionQty'].sum()} Ltr**")
        st.markdown("---")
        
        # Add a placeholder to ensure equal height
        st.write("")  # You can add any extra information or leave it empty if not needed

with col2:
        # Display list of all transacted chemicals
        st.write("## List of All Transacted Chemicals")
        list_item = sample_df[['OldCode', 'Description']].drop_duplicates().reset_index(drop=True)
        list_item.index += 1
        st.dataframe(list_item , height=580)

        # Add a placeholder to ensure equal height
        st.write("")  # You can add any extra information or leave it empty if not needed

# st.markdown("---")



# ********** Display DataFrame info ***********************
# st.write("## Sample Original Data Overview")
# st.dataframe(sample_df)
# st.write(sample_df.shape)

# st.write("Dropped 'QtyBalRmStore', 'QtyBalPPC', 'QtyBalTotal' & added 'Year', 'Month' column. Filtered Transaction Type to 'Issued to Floor'")

st.write("## Tranaction Data")
st.dataframe(df)
st.write(f'Dataframe Shape : {df.shape}')


st.markdown("---")   
# ***** info about columns and plot ***********************************
col1 , col2 = st.columns(2)
with col1:
    st.write("### DataFrame Information:")
    st.write(analysis_backend.df_info(df))

with col2:
        null_df = analysis_backend.df_info(df)

        # Extract data types counts
        data_types = null_df['Data Type'].value_counts()

        # Create a bar plot for data types
        fig, ax = plt.subplots()
        data_types.plot(kind='bar', ax=ax, color='red')
        ax.set_title('Count of Different Data Types in DataFrame Columns')
        ax.set_xlabel('Data Type')
        ax.set_ylabel('Number of Columns')

        # Display the plot in Streamlit
        st.write('### Data Types of Columns:')
        st.pyplot(fig)



# ************* NUll count and plot *************************************


st.markdown("---")
col1 , col2 = st.columns(2)
with col1:
    st.write("### Missing Values in different columns:")
    st.write(analysis_backend.null_count(df))

with col2:
        null_df = analysis_backend.null_count(df)

        # Create a bar plot for null counts
        fig, ax = plt.subplots()
        ax.bar(null_df['Features'], null_df['Null Count'], color='red')
        ax.set_xticklabels(null_df['Features'], rotation=90)  # Rotate x-axis labels for better readability
        ax.set_title('Null Counts by Column')
        ax.set_xlabel('Column')
        ax.set_ylabel('Number of Nulls')

        # Display the plot in Streamlit
        st.write('### Null Counts in DataFrame Columns')
        st.pyplot(fig)
st.markdown("---")




# ******** printing filtered trasnsactions dataframes with plot *************

# monthly with transaction quantity

monthly_txn_df = analysis_backend.monthly_transaction_df(df,low_transaction_item_list)

st.write("## Monthly grouped Transactions:")
st.dataframe(monthly_txn_df)
st.write(f'Dataframe Shape : {monthly_txn_df.shape}')

  # Count occurrences of each 'OldCode'
counts = monthly_txn_df['OldCode'].value_counts()
ordered_codes = counts.index


st.markdown("---")
# Group by year and OldCode with transaction quantity
yearly_transaction = analysis_backend.yearly_transaction_df(df,low_transaction_item_list)

# Yearly Transactions over time
st.write("## Yearly Grouped Transactions:")
st.dataframe(yearly_transaction)
st.write(f'Dataframe Shape : {yearly_transaction.shape}')


# Plot of Monthly Transactions in Production Years 2021-2023
st.write("## Number of Monthly Transactions in Production Years 2021-2023:")
fig, ax = plt.subplots(figsize=(15, 6))
sns.countplot(data=monthly_txn_df, x='OldCode', order=ordered_codes, ax=ax)
plt.xticks(rotation=45)
plt.title('Transaction Throughout the Period:')
plt.tight_layout()
st.pyplot(fig)


#Plot of  Yearly Transactions over time
st.write("## Yearly Transactions:")
fig, ax = plt.subplots(figsize=(15, 6))
sns.barplot(data=yearly_transaction, x='OldCode', y='TransactionQty', hue='Year', ax=ax)
plt.xticks(rotation=45)
plt.title('Net Transaction of Different Material Throughout the Production Period:')
plt.tight_layout()
st.pyplot(fig)


st.markdown("---")
#Plot of Filtered transaction above 100 in total
st.write("## Filtered Transactions with Quantity >= 100:")
st.dataframe(total_transaction_df)
st.write(f'Dataframe Shape: {total_transaction_df.shape}')


# ************* bar plotting for different conditions ***********************

# Total Transaction
st.write("## Total Amount of Material Transacted")
fig, ax = plt.subplots(figsize=(15, 6))
sns.barplot(data=total_transaction_df, x='OldCode', y='TransactionQty', order=total_transaction_df['OldCode'], ax=ax)
plt.xticks(rotation=45)
plt.title('Net Transaction Throughout the Production Period:')
plt.tight_layout()
st.pyplot(fig)

st.markdown("---")


# return monthly_txn_df

