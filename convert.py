import streamlit as st
import pint
import re
import logging


# 正規表現で指数表記 or 普通の数値をチェック
def is_valid_number(s):
    return re.fullmatch(r"^\s*[+-]?(?:\d{1,3}(?:,\d{3})*|\d+)?(?:\.\d+)?(?:[eE][+-]?\d+)?\s*$", s) is not None

# 単位レジストリを作成
ureg = pint.UnitRegistry()

inputQuantity = None
outputQuantity = None

logging.basicConfig(filename='error.log',level=logging.ERROR)

st.title("Unit Converter")
colU1, colU2 = st.columns([2,1])

with colU1:
    user_input = st.text_input("Input Number", value = "1.23e0", key = "number_input")
    formatted_input = re.sub(r'\s+', '', user_input)

    #st.write(formatted_input)
    #st.write(st.session_state.formatted_input_text)

    # 入力が正しいかチェック
    if is_valid_number(formatted_input):
        inputNum = float(formatted_input.replace(",",""))
        #st.write(f"入力された数値: {num:.2e} （{num}）")
    else:
        inputNum = None
        st.warning("Input example: 3.14, 6.02e23")

with colU2:
    inputUnit = st.text_input(
        "Unit","N/mm^2",key="input"
    )
    
    try:
        st.write(ureg(inputUnit).units)
    except pint.errors.UndefinedUnitError:
        st.warning("Undefined Unit")
        

colM1, colM2 = st.columns([2,1])
with colM1:
    st.markdown("<h2 style='text-align: center;'>↓</h2>", unsafe_allow_html=True)

colL1, colL2 = st.columns([2,1])
with colL2:
    outputUnit = st.text_input(
        "Unit","N/m^2",key="output"
    )
    try:
        st.write(ureg(outputUnit).units)
    except pint.errors.UndefinedUnitError:
        st.warning("Undefined Unit")
   
try:
    inputQuantity = inputNum * ureg(inputUnit)
    outputQuantity = inputQuantity.to(outputUnit)
    with colL1:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:100px; line-height:100px;'>{outputQuantity.magnitude}</p>", unsafe_allow_html=True)

except pint.DimensionalityError:
    with colM2:
        st.markdown("""
        <h3 style='text-align: center; margin-bottom: 0px;'>😕</h3>
        <p style='text-align: center; font-size: 18px; line-height: 1; margin-top: 0px;'>↑↓Dimensional Mismatch</p>
        """, unsafe_allow_html=True)

    with colL1:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:100px; line-height:100px;'>🤔</p>", unsafe_allow_html=True)

except Exception as e:
    logging.error(f"Unexpected Error: {e}")
    with colL1:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:100px; line-height:100px;'>😵</p>", unsafe_allow_html=True)
