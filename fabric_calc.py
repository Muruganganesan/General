import streamlit as st

# Page layout and style
st.set_page_config(page_title="Textile Fabric Rate Calculator", layout="centered")
st.markdown("""
    <style>
    .stButton>button {
        background-color: #ffcc99;
        color: black;
        font-weight: bold;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 24px;
        box-shadow: 2px 2px 5px grey;
    }
    .output-box {
        background-color: #ffcc99;
        color: black;
        font-weight: bold;
        font-size: 20px;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px grey;
        text-align: center;
        margin: 10px 0;
    }
    .red-val {
        color: red;
        font-weight: bold;
    }
    input[type=number] {
        -moz-appearance: textfield;
    }
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧵 Fabric GSM & Cost Calculator")

# 🧮 Sort Details in one row (without + - and default float)
st.subheader("🧮 Sort Details")
s1, s2, s3, s4, s5, s6 = st.columns([1, 0.3, 1, 0.3, 1, 1])
with s1:
    warp_count = st.number_input("Warp", value=0, step=1, format="%d", label_visibility="collapsed")
with s2:
    st.markdown("<p style='text-align:center'><b>X</b></p>", unsafe_allow_html=True)
with s3:
    weft_count = st.number_input("Weft", value=0, step=1, format="%d", label_visibility="collapsed")
with s4:
    st.markdown("<p style='text-align:center'><b>X</b></p>", unsafe_allow_html=True)
with s5:
    epi = st.number_input("EPI", value=0, step=1, format="%d", label_visibility="collapsed")
with s6:
    ppi = st.number_input("PPI", value=0, step=1, format="%d", label_visibility="collapsed")

# Width separate
fabric_width = st.number_input("Width (in inches)", value=0, step=1, format="%d")

# 📥 Rate Inputs
st.subheader("💰 Rate Inputs")
rcol1, rcol2 = st.columns(2)
with rcol1:
    warp_yarn_rate = st.number_input("Warp Yarn Rate (₹)", value=0, step=1, format="%d")
    sizing_rate = st.number_input("Sizing Rate (₹)", value=0, step=1, format="%d")
with rcol2:
    weft_yarn_rate = st.number_input("Weft Yarn Rate (₹)", value=0, step=1, format="%d")
    pick_rate = st.number_input("Pick Rate (₹)", value=0.0, step=0.01)

# Apply Button
apply = st.button("APPLY")

# Calculations
if apply:
    waste_percent = 10
    waste_multiplier = 1 + (waste_percent / 100)

    try:
        warp_weight = (epi * fabric_width) / (1693 * warp_count) * waste_multiplier
        weft_weight = (ppi * (fabric_width + 4)) / (1693 * weft_count) * waste_multiplier
        fabric_weight = warp_weight + weft_weight
        gsm = (fabric_weight * 39.37) / fabric_width

        warp_rate = warp_yarn_rate * warp_weight
        weft_rate = weft_yarn_rate * weft_weight
        pick_total = pick_rate * ppi
        sizing_total = sizing_rate * warp_weight

        fabric_rate = warp_rate + weft_rate + pick_total + sizing_total

        # Display
        st.markdown("---")
        st.subheader("📤 Output Details")

        st.write(f"🔸 Warp Weight : {warp_weight:.3f}")
        st.write(f"🔸 Weft Weight : {weft_weight:.3f}")
        st.markdown(f"<div class='output-box'>FABRIC WT : <span class='red-val'>{fabric_weight:.3f}g</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='output-box'>GSM : <span class='red-val'>{gsm:.3f}g</span></div>", unsafe_allow_html=True)
        

        st.write(f"🔹 Warp Rate : ₹{warp_rate:.2f}")
        st.write(f"🔹 Weft Rate : ₹{weft_rate:.2f}")
        st.write(f"🔹 Pick Rate : ₹{pick_total:.2f}")
        st.write(f"🔹 Sizing Rate : ₹{sizing_total:.2f}")
        st.markdown(f"<div class='output-box'>FABRIC RATE : <span class='red-val'>Rs:{fabric_rate:.2f}/-</span></div>", unsafe_allow_html=True)
         
    except ZeroDivisionError:
        st.error("Please enter non-zero values for Warp and Weft Count to avoid division by zero.")
        st.markdown("---")
        st.caption("Developed by Murugan Ganesan")
