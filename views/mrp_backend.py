# import streamlit as st
import pandas as pd

def get_mrp(df,selected_material):
      material_table = df[df['Description'] == selected_material]
      material_table.sort_values(by = ['Year' , 'Month'])

      # print('\nMaterial transaction in the production period : \n')
      # st.dataframe(material_table)

      pivot_table = material_table.pivot_table(values = "TransactionQty" , index = "Month" , columns = "Year").fillna(0)
      # st.write(pivot_table)
      return material_table,pivot_table
      


def create_mrp_record(material_table,n=3):
      data = {
          'Period' : ['Demand' , 'Beg. Inventory' , 'End. Inventory' , 'P.O.R'],
          'quarter1' : [0,0,0,0],
          'quarter2' : [0,0,0,0],
          'quarter3' : [0,0,0,0],
          'quarter4' : [0,0,0,0]

      }

      mrp_table = pd.DataFrame(data)
      monthly_usage = material_table.nlargest(n, 'TransactionQty')['TransactionQty'].mean()

      return mrp_table,monthly_usage





def create_new_col(data,demand ,beg_inventory_q1,lead_time):
    n=1
    for i , quarter in enumerate(data.columns) :
        new_columns = []

        if i > 0 :

            data.loc[0,quarter] = demand

            if(quarter == 'quarter1'):
              data.loc[1 , 'quarter1'] = beg_inventory_q1

            quarter = 'quarter' + str(i - lead_time)
            if quarter not in data.columns and quarter not in new_columns:
                  data.insert(n, quarter, 0)  # Insert new column at index 1
                  new_columns.append(quarter)  # Track newly inserted column
                  n+=1

    data.loc[2,'quarter0'] = data.loc[1,'quarter1']

    return data

def update_table(data,lead_time,safety_stock,por_value):  # Track recursion depth

    for i,  quarter in enumerate(data.columns):
        if lead_time < i < len(data.columns) :

            prev_quarter = 'quarter' + str(i -lead_time - 1)
            prev_por_colmn = 'quarter' + str(i - 2*lead_time )

            # update beg inventory
            if prev_quarter in data.columns:
              data.loc[1,quarter] = data.loc[2,prev_quarter] + data.loc[3, prev_por_colmn]

            # update end inventory
            data.loc[2,quarter] = float(data.loc[1,quarter]) - float(data.loc[0,quarter])
            if float(data.loc[2,quarter]) < safety_stock :
              data.loc[3,prev_por_colmn] = por_value
              data.loc[1,quarter] = data.loc[2,prev_quarter] + data.loc[3, prev_por_colmn]
              data.loc[2,quarter] = float(data.loc[1,quarter]) - float(data.loc[0,quarter])
              # update(data)



    return data