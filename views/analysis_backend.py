import pandas as pd


# ********* get the dataframe **************
def get_df(sample_df):
    # Drop undesired columns
    
    df = sample_df.drop(columns=['ItemLotId', 'QtyBalRmStore', 'QtyBalPPC', 'QtyBalTotal'])

    # Filter for 'Issued To Floor' transactions
    df = df[df['TransactionType'] == 'Issued To Floor'].reset_index(drop=True)

    # Insert year and month columns
    df.insert(3, 'Year', df['TransactionOn'].dt.year)
    df.insert(4, 'Month Name', df['TransactionOn'].dt.month_name())
    df.insert(5, 'Month', df['TransactionOn'].dt.month)

    # # Reset index to ensure it's clean
    # df.reset_index(drop=True, inplace=True)
    df.index += 1  # Adjust index to start from 1

    return df



# ****** getting info about data columns present************
def df_info(df):
        info_df = pd.DataFrame({
              'Column': df.columns,
              'Non-Null Count': df.notnull().sum(),
              'Data Type': df.dtypes
          })
        
        info_df = info_df.reset_index(drop=True)
        info_df.index +=1
        return info_df




# ************* NUll count*****************
def null_count(df):
    # Calculate null counts for each column
    null_count_series = df.isnull().sum()
    
    # Convert Series to DataFrame
    null_count_df = null_count_series.reset_index()
    
    # Rename columns
    null_count_df.columns = ['Features', 'Null Count']
    null_count_df.index +=1
    return null_count_df


# **************** getting yearly transaction dataframe***********************
def yearly_transaction_df(df,low_transaction_item_list):
        group_year = df.groupby(['OldCode', 'Description', 'Year'])['TransactionQty'].sum().reset_index()
        group_year = group_year[~group_year['OldCode'].isin(low_transaction_item_list)]
        group_year = group_year.sort_values(by=['Description','Year']).reset_index(drop=True)

        group_year.index += 1

        return group_year


#  *********** getting monthly and yearly group transaction ******************

def monthly_transaction_df(df,low_transaction_item_list):
        
        monthly_txn_df = df.groupby(['OldCode', 'Description', 'Year', 'Month','Month Name'])['TransactionQty'].sum().reset_index()
        monthly_txn_df = monthly_txn_df[~monthly_txn_df['OldCode'].isin(low_transaction_item_list)]
        monthly_txn_df = monthly_txn_df.sort_values(by = ['Description','Year','Month']).reset_index(drop=True)

        monthly_txn_df.index += 1

        return monthly_txn_df








# *********** fetching overall sum information***********************

def sum_overall_transaction(df):
          # Group by OldCode and Description with transaction quantity
          group = df.groupby(['OldCode', 'Description'])['TransactionQty'].sum().reset_index()

          # List and filter low transaction items
          low_trans_item_list = group[group['TransactionQty'] < 100]['OldCode']

          # filtering item having transaction aboce 100
          group = group[group['TransactionQty'] >= 100]
          group = group.sort_values(by='TransactionQty', ascending=True).reset_index(drop=True)

          group.index += 1

          return group,low_trans_item_list



          