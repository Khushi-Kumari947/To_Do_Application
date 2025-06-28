import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

client=MongoClient(st.secrets["mongo"]["uri"])
db=client["Todo_DB"]    #making database
todos=db["todos"]       #making collection

# Streamlit App UI

st.title("Plan your day!")

st.subheader("Add a Task")
new_task=st.text_input("Enter a task")

if st.button("Add Task"):
    if new_task.strip()!="":
        todos.insert_one({"task":new_task,"status":"Incomplete"})
        st.success("Task added!")
        st.rerun()
    else:
        st.warning("Task cannot be empty!")

st.subheader("Your Tasks")

tasks=list(todos.find())

if tasks:
    for task in tasks:
        col1,col2,col3=st.columns([6,2,2])
    
        #display task with status
        if task["status"]=="Complete":
            col1.markdown(f"✅Completed:{task["task"]}")
        else:
            col1.markdown(f"🕘Due:{task["task"]}")
    
    
        #complete button
        if task["status"]=="Incomplete":
            if col2.button("✅Done",key=f"done{task["_id"]}"):
                todos.update_one({"_id":task["_id"]},{"$set":{"status":"Complete"}})
                st.rerun()
    
        #delete button
        if col3.button("Delete",key=f"del{task["_id"]}"):
            todos.delete_one({"_id":task["_id"]})
            st.rerun()
    

else:
    st.info("No tasks yet.Add one above!")

    

