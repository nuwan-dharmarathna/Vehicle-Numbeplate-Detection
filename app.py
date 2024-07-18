import mysql.connector
from mysql.connector import Error

import streamlit as st

import os
from dotenv import load_dotenv

import pandas as pd

load_dotenv()

#Connect to database
DB_NAME = "gate_system"

try:
    connection = mysql.connector.connect(
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        database = DB_NAME
    )
    if connection.is_connected():
        print(f"Connected to database '{DB_NAME}'")
except Error as e:
    print(f"Error while connecting to MySQL: {e}")
    

# Building App

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title("Automated Gate System")

# display the options in sidebar

option = st.sidebar.selectbox("Select Option", ["Go to Database", "Go to Live"], placeholder="Choose an Option")

# Perform selected option
if option == "Go to Database":
    st.subheader("Welcome to '{}' Database".format(str.upper(DB_NAME)))
    talble = st.selectbox("Select Table", ["Vehicle Details", "Customer Details"])
    if talble == "Vehicle Details":
        st.subheader("---------------------------Vehicle Details----------------------------", )
        v_opt = st.selectbox("Vehicle Details", ["Display Vehicle Details", "Add Vehicle", "Update Vehicle", "Delete Vehicle"])
        if v_opt == "Display Vehicle Details":
            st.subheader("Display Vehicle Details")
            
            try:
                cursor = connection.cursor()
                cursor.execute("select * from vehicle")
                
                results = cursor.fetchall()
                
                df = pd.DataFrame(results, columns=cursor.column_names)
                st.dataframe(df, width=2000)
                
                
            except Error as e:
                print(f"Error while fetching data from MySQL: {e}")
            finally:
                cursor.close()
            
        elif v_opt == "Add Vehicle":
            st.subheader("Add Vehicle Details")
            
            v_number = st.text_input("Enter Vehicle Number")
            model = st.text_input("Model")
            
            # populate with owner_id
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM owner")
            result = cursor.fetchall()
            cursor.close()
            
            owner = st.selectbox("Select one", [row[0] for row in result])
            
            if st.button("Add Details"):
                try:
                    query = "insert into vehicle(vehicle_number, model, owner_id) values(%s, %s, %s)"
                    val = (v_number, model, owner)
                    connection.cursor().execute(query, val)
                    connection.commit()
                    st.success("Successfully Created")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.cursor().close()
            
        elif v_opt == "Update Vehicle":
            st.subheader("Update Vehicle")
            
            
            
        else:
            st.subheader("Delete Vehicle")
        
    elif talble == "Customer Details":
        st.subheader("---------------------------Customer Details---------------------------")
        
        c_opt = st.selectbox("Customer Details", ["Display Customer Details", "Add Customer", "Update Customer", "Delete Customer"])
        
        if c_opt == "Display Customer Details":
            st.subheader("Display Customer Details")
            
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM owner")
                
                results = cursor.fetchall()
                
                df = pd.DataFrame(results, columns=cursor.column_names)
                st.dataframe(df, width=2000)
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
            
        elif c_opt == "Add Customer":
            st.subheader("Add Customer Details")
            
            f_name = st.text_input("First Name")
            l_name = st.text_input("Last Name")
            phone = st.text_input("Phone")
            
            if st.button("Add Details"):
                try: 
                    query = "insert into owner(first_name, last_name, phone) values(%s, %s, %s)"
                    val = (f_name, l_name, phone)
                    
                    connection.cursor().execute(query, val)
                    connection.commit()
                    st.success("Successfully Created")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.cursor().close()
            
        elif c_opt == "Update Customer":
            st.subheader("Update Customer")
            
            # Populate customer data
            
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM owner")
                
                results = cursor.fetchall()
                

            
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
                
            f_name = st.text_input("First Name")
            l_name = st.text_input("Last Name")
            phone = st.text_input("Phone")
            
            
        else:
            st.subheader("Delete Customer")
            
else:
    st.subheader("Welcome to Live System")
    

