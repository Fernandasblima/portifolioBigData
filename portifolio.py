import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import pandas as pd
from faker import Faker
from datetime import datetime

client = MongoClient("mongodb://mongo:27017/")
db = client["eshop"]
collection = db["clients"]
collection2 = db["products"]
collection3 = db["orders"]

fake = Faker()

def generate_fake_clients(num_records):
    return [{
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
    } for _ in range(num_records)]

def generate_fake_products(num_records):
    base_names = [f"Produto {chr(65 + i % 26)}{i//26 if i >= 26 else ''}" for i in range(num_records)]
    return [{
        "name": base_names[i],
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 1000)
    } for i in range(num_records)]

def generate_fake_orders(num_records):
    clients = list(collection.find())
    products = list(collection2.find())
    if not clients or not products:
        return []
    return [{
        "client_id": random.choice(clients)["_id"],
        "product_id": random.choice(products)["_id"],
        "quantity": random.randint(1, 5),
        "purchase_date": fake.date_time_this_year()
    } for _ in range(num_records)]

st.set_page_config(page_title="E-Shop Big Data App", layout="wide")
st.title("E-Shop Brasil - Gestão de Dados")

st.sidebar.title("🔧 Seções")
section = st.sidebar.radio("Escolha uma seção:", [
    "Clientes", "Produtos", "Pedidos", "Análise de Dados"])

  
if section == "Clientes":
    st.header("Clientes")
    num = st.number_input("Nº de clientes falsos:", 1, 1000, 5)
    if st.button("Gerar Clientes"):
        data = generate_fake_clients(num)
        collection.insert_many(data)
        st.success(f"{num} clientes inseridos.")

    if st.button("Visualizar Clientes"):
        clients = list(collection.find())
        for c in clients:
            c["_id"] = str(c["_id"])
        st.dataframe(pd.DataFrame(clients))

    client_id = st.text_input("ID do Cliente para excluir:")
    if st.button("Excluir Cliente"):
        try:
            collection.delete_one({"_id": ObjectId(client_id)})
            st.success("Cliente excluído com sucesso!")
        except:
            st.error("ID inválido.")

    st.subheader("Atualizar Cliente")
    update_client_id = st.text_input("ID do Cliente para atualizar:")
    update_field = st.selectbox("Campo:", ["name", "email", "address", "phone_number"])
    update_value = st.text_input("Novo valor:")
    if st.button("Atualizar Cliente"):
        try:
            collection.update_one(
                {"_id": ObjectId(update_client_id)},
                {"$set": {update_field: update_value}}
            )
            st.success("Cliente atualizado com sucesso!")
        except:
            st.error("Erro ao atualizar cliente.")

elif section == "Produtos":
    st.header("Produtos")
    num = st.number_input("Nº de produtos falsos:", 1, 1000, 5)
    if st.button("Gerar Produtos"):
        data = generate_fake_products(num)
        collection2.insert_many(data)
        st.success(f"{num} produtos inseridos.")

    if st.button("Visualizar Produtos"):
        products = list(collection2.find())
        for p in products:
            p["_id"] = str(p["_id"])
        st.dataframe(pd.DataFrame(products))

    product_id = st.text_input("ID do Produto para excluir:")
    if st.button("Excluir Produto"):
        try:
            collection2.delete_one({"_id": ObjectId(product_id)})
            st.success("Produto excluído com sucesso!")
        except:
            st.error("ID inválido.")

    st.subheader("Atualizar Produto")
    update_product_id = st.text_input("ID do Produto para atualizar:")
    update_field = st.selectbox("Campo:", ["name", "price", "stock"])
    update_value = st.text_input("Novo valor:")
    if st.button("Atualizar Produto"):
        try:
            value = float(update_value) if update_field == "price" else int(update_value) if update_field == "stock" else update_value
            collection2.update_one(
                {"_id": ObjectId(update_product_id)},
                {"$set": {update_field: value}}
            )
            st.success("Produto atualizado com sucesso!")
        except:
            st.error("Erro ao atualizar produto.")

elif section == "Pedidos":
    st.header("Pedidos")
    num = st.number_input("Nº de pedidos falsos:", 1, 1000, 5)
    if st.button("Gerar Pedidos"):
        data = generate_fake_orders(num)
        if data:
            collection3.insert_many(data)
            st.success(f"{num} pedidos inseridos.")
        else:
            st.error("Clientes ou produtos insuficientes.")

    if st.button("Visualizar Pedidos"):
        pedidos = list(collection3.find())
        for p in pedidos:
            p["_id"] = str(p["_id"])
            p["client_id"] = str(p["client_id"])
            p["product_id"] = str(p["product_id"])
        st.dataframe(pd.DataFrame(pedidos))

    pedido_id = st.text_input("ID do Pedido para excluir:")
    if st.button("Excluir Pedido"):
        try:
            collection3.delete_one({"_id": ObjectId(pedido_id)})
            st.success("Pedido excluído com sucesso!")
        except:
            st.error("ID inválido.")

    st.subheader("Atualizar Pedido")
    update_pedido_id = st.text_input("ID do Pedido para atualizar:")
    update_field = st.selectbox("Campo:", ["client_id", "product_id", "quantity", "purchase_date"])
    update_value = st.text_input("Novo valor:")
    if st.button("Atualizar Pedido"):
        try:
            if update_field in ["quantity"]:
                value = int(update_value)
            elif update_field in ["client_id", "product_id"]:
                value = ObjectId(update_value)
            elif update_field == "purchase_date":
                value = pd.to_datetime(update_value)
            else:
                value = update_value

            collection3.update_one(
                {"_id": ObjectId(update_pedido_id)},
                {"$set": {update_field: value}}
            )
            st.success("Pedido atualizado com sucesso!")
        except:
            st.error("Erro ao atualizar pedido.")

