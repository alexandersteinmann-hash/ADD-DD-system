import streamlit as st
import uuid

# --- SEITENKONFIGURATION ---
st.set_page_config(page_title="DD Server- & Tausch-Manager", page_icon="👑", layout="wide")

# --- DATENBANK-SIMULATION (Session State) ---
if "servers" not in st.session_state:
    st.session_state.servers = {}  # Struktur: {server_id: {name, creator, admins: [], members: [], balances: {}, pending_trades: [], vouchers: {}}}
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- LOGIN / USER-WAHL ---
st.title("👑 DD Server, Rechte & Tausch-System")

if not st.session_state.current_user:
    st.subheader("Anmelden / Benutzer wählen")
    username = st.text_input("Gib deinen Benutzernamen ein:").strip()
    if st.button("Einloggen") and username:
        st.session_state.current_user = username
        st.rerun()
    st.stop()

# Sidebar-Info & Logout
st.sidebar.write(f"Eingeloggt als: *{st.session_state.current_user}*")
if st.sidebar.button("Abmelden"):
    st.session_state.current_user = None
    st.rerun()

# --- URL-PARAMETER FÜR EINLADUNGEN & GUTSCHEINE ---
query_params = st.query_params
invite_server_id = query_params.get("invite")
voucher_id = query_params.get("voucher")

# Server-Beitritt via Einladungslink
if invite_server_id and invite_server_id in st.session_state.servers:
    server = st.session_state.servers[invite_server_id]
    user = st.session_state.current_user
    if user not in server["members"]:
        server["members"].append(user)
        server["balances"][user] = 0  # Startguthaben für neue Mitglieder: 0 DD
        st.success(f"🎉 Du bist erfolgreich dem Server *{server['name']}* beigetreten!")
        st.query_params.clear()

# Gutschein via URL-Parameter einlösen
if voucher_id:
    voucher_found = False
    for sid, s in st.session_state.servers.items():
        if voucher_id in s["vouchers"]:
            voucher_found = True
            server = s
            voucher = s["vouchers"][voucher_id]
            user = st.session_
