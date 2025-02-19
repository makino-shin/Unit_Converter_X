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

# Steamlit Layout
st.title("Unit Converter X")
colU1, colU2 = st.columns([2,1])
cont1 = st.container(border=False, height=60)
colL1, colL2 = st.columns([2,1])

with colL1:
    outputCol, buttonCol1, buttonCol2 = st.columns([4,1,1], vertical_alignment="center")

#with buttonCol1:
    #st.button("R/S", use_container_width=True)
    
#with buttonCol2:
    #st.button("Copy", use_container_width=True)

with colU1:
    user_input = st.text_input("Input Number", value = "2.06e2", key = "number_input", label_visibility = "collapsed")
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
        "Unit","GPa",key="input", label_visibility = "collapsed"
    )
    
    try:
        st.write(ureg(inputUnit).units)
       
    except pint.errors.UndefinedUnitError:
        st.warning("Undefined Unit")
    except :
        st.warning("Undefined Unit")



with colL2:
    outputUnit = st.text_input(
        "Unit","N/m^2",key="output", label_visibility = "collapsed"
    )
    try:
        st.write(ureg(outputUnit).units)
    except pint.errors.UndefinedUnitError:
        st.warning("Undefined Unit")
    except :
        st.warning("Undefined Unit")
   
try:
    inputQuantity = inputNum * ureg(inputUnit)
    outputQuantity = inputQuantity.to(outputUnit)
    with cont1:
        st.markdown("<p style='text-align: center; font-size: 40px; height:40px; line-height:40px;'>↓</p>", unsafe_allow_html=True)

    with outputCol:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:40px; line-height:40px;'>{outputQuantity.magnitude}</p>", unsafe_allow_html=True)

except pint.DimensionalityError:
    with cont1:
        st.markdown("<p style='text-align: center; font-size: 25px; height:40px; line-height:40px;'>↑↓Dimensional Mismatch</p>", unsafe_allow_html=True)

    with outputCol:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:40px; line-height:40px;'>🤔</p>", unsafe_allow_html=True)

except Exception as e:
    logging.error(f"Unexpected Error: {e}")
    with outputCol:
        st.markdown(f"<p style='text-align: center; font-size: 40px; height:40px; line-height:40px;'>😵</p>", unsafe_allow_html=True)
