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

option = st.sidebar.selectbox("Select Option", ["Go to Database ⌸", "Go to Live ◎"], placeholder="Choose an Option")

# Perform selected option
if option == "Go to Database ⌸":
    #heading_1
    st.subheader("Welcome to '{}' Database".format(str.upper(DB_NAME)))
    
    #select table
    talble = st.selectbox("Select Table", ["Vehicle Details", "Customer Details"])
    
    #vehicle table
    if talble == "Vehicle Details":
        st.subheader("Vehicle Details 🚗")
        v_opt = st.selectbox("Vehicle Details", ["Display Vehicle Details", "Add Vehicle", "Update Vehicle", "Delete Vehicle"])
        # Display vehicle
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
            
        # Add vehicle
        elif v_opt == "Add Vehicle":
            st.subheader("Add Vehicle Details")
            
            v_number = st.text_input("Enter Vehicle Number")
            model = st.text_input("Model")
            
            # populate with owner_id
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM owner")
            result = cursor.fetchall()
            cursor.close()
            
            options = [f"{row[0]} - {row[1]} - {row[3]}" for row in result]
            
            owner = st.selectbox("Select one", options)
            
            if st.button("Add Details"):
                try:
                    query = "insert into vehicle(vehicle_number, model, owner_id) values(%s, %s, %s)"
                    val = (v_number, model, owner[0])
                    connection.cursor().execute(query, val)
                    connection.commit()
                    st.success("Successfully Created")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.cursor().close()
            
        # Update vehicle
        elif v_opt == "Update Vehicle":
            st.subheader("Update Vehicle")
            
            # Populate vehile data
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicle")
                
                results = cursor.fetchall()
                
                options = [f"{row[0]} - {row[1]} - {row[2]}"for row in results]
                
                vehicle = st.selectbox("Select vehicle", options)
                vehicle_details = vehicle.split(" - ")
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
            
            st.write("-"*20)
            
            if vehicle:
                # vehicle_number = st.text_input("Number Plate", vehicle_details[0])
                model = st.text_input("Model", vehicle_details[1])
                owner_id = st.text_input("owner ID", vehicle_details[2])
                vehicle_number = vehicle_details[0]
                
                if st.button("Update"):
                    try:
                        query = """ UPDATE vehicle
                                    SET model = %s, owner_id = %s
                                    WHERE vehicle_number = %s
                                    """
                        val = (model, owner_id, vehicle_number)
                        connection.cursor().execute(query, val)
                        connection.commit()
                        st.success("Successfully Updated")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.cursor().close()
            else:
                st.warning("Please select a vehicle to update")
            
        # Delete vehicle
        else:
            st.subheader("Delete Vehicle")
            
            # Populate vehile data
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicle")
                
                results = cursor.fetchall()
                
                options = [f"{row[0]} - {row[1]} - {row[2]}"for row in results]
                
                vehicle = st.selectbox("Select vehicle", options)
                vehicle_details = vehicle.split(" - ")
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
                
            if st.button("Delete"):
                try:
                    #get vehicle_number
                    vehicle_number = vehicle_details[0]
                    
                    query = "DELETE FROM vehicle WHERE vehicle_number = %s"
                    val = (vehicle_number,)
                    connection.cursor().execute(query, val)
                    connection.commit()
                    st.success("Successfully Deleted")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.cursor().close()
    
    #owner table    
    elif talble == "Customer Details":
        
        st.subheader("Customer Details 👨‍💼")
        
        c_opt = st.selectbox("Customer Details", ["Display Customer Details", "Add Customer", "Update Customer", "Delete Customer"])
        
        #Display Customer
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
            
        #Add Customer
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
            
        #Update Customer
        elif c_opt == "Update Customer":
            st.subheader("Update Customer")
            
            # Populate customer data
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM owner")
                
                results = cursor.fetchall()
                
                # Create the options for the select box
                options = [f"{row[0]} - {row[1]} - {row[2]} - {row[3]}" for row in results]
                
                owner = st.selectbox("Select one", options)
                
                owner_details = owner.split(" - ")
            
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
                
            st.write("-"*20)
                
            if owner:
                f_name = st.text_input("First Name", owner_details[1])
                l_name = st.text_input("Last Name", owner_details[2])
                phone = st.text_input("Phone", owner_details[3])
                owner_id = int(owner_details[0])
                
                if st.button("Update"):
                    try:
                        query = """ UPDATE owner
                                    SET first_name = %s, last_name = %s, phone = %s
                                    WHERE owner_id = %s
                                    """
                        val = (f_name, l_name, phone, owner_id)
                        connection.cursor().execute(query, val)
                        connection.commit()
                        st.success("Successfully Updated")
                    except Error as e:
                        st.error(f"Error: {e}")
                    finally:
                        connection.cursor().close()
                else:
                    st.error("Please fill in all the fields")
    
        #Delete Customer
        else:
            st.subheader("Delete Customer")
            
            # Populate customer data
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM owner")
                
                results = cursor.fetchall()
                
                # Create the options for the select box
                options = [f"{row[0]} - {row[1]} - {row[2]} - {row[3]}" for row in results]
                
                owner = st.selectbox("Select one", options)
                
                owner_details = owner.split(" - ")
            
            except Error as e:
                st.error(f"Error: {e}")
            finally:
                cursor.close()
            
            if st.button("Delete"):
                try:
                    #get owner_id
                    owner_id = int(owner_details[0])
                    
                    query = "DELETE FROM owner WHERE owner_id = %s"
                    val = (owner_id,)
                    connection.cursor().execute(query, val)
                    connection.commit()
                    st.success("Successfully Deleted")
                except Error as e:
                    st.error(f"Error: {e}")
                finally:
                    connection.cursor().close()
            
            
else:
    st.subheader("Welcome to Live System")
    

