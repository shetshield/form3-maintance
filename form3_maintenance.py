import streamlit as st
import time
import pandas as pd
from PIL import Image
import altair as alt


Clear = 4
Black = 3
Elastic = 1
Flexible = 1
Rigid10K = 1
Durable = 1
Tank = 1
Platform = 1
df_idx = ["Clear", "Black", "Elastic", "Flexible", "Rigid10K", "Durable", "탱크", "플랫폼"]
IPA = 0.8
cur_resin_stock = {'Clear': Clear, 'Black': Black, 'Elastic':Elastic, 'Flexible': Flexible,
             'Rigid10K': Rigid10K, 'Durable': Durable}
cur_etc_stock = {'Tank': Tank, 'Platform': Platform, 'IPA':IPA}

product_list = {'Clear': 100096, 'Black': 100096, 'Durable': 100146, 'IPA': 100829, 'Platform': 100552,
                'Tank': 100435, 'Elastic': 100434, 'Rigid10K': 100550, 'Flexible': 100698}

ipa_dict = pd.DataFrame(data=[IPA], index=["IPA"])
stock_dict = pd.DataFrame(data=[Clear, Black, Elastic,
                                Flexible, Rigid10K, Durable, Tank, Platform], index=df_idx)
stock_df = pd.DataFrame(stock_dict)
ipa_df = pd.DataFrame(ipa_dict)


def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages(
        "form3_maintance.py"
    )  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [
        standardize_name(config["page_name"]) for config in pages.values()
    ]

    raise ValueError(
        f"Could not find page {page_name}. Must be one of {page_names}"
    )


im = Image.open("./img/favicon.png")
st.set_page_config(
    page_title="Form3_재고",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="collapsed",
)
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;
    right: 0;}
     details {
            display: none;
        }
html, body {
    max-width: 80%;
    overflow-x: hidden !important;
    width: 80vw;
}
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)
st.markdown(
    """
    ##### Form3 <a href="https://formlabs.com/dashboard/" target="_blank">Dashboard </a>
    """, unsafe_allow_html=True
)
st.write("## 폼3 재고 관리 페이지")

data = pd.melt(stock_df.reset_index(), id_vars=["index"])
chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title="", axis=alt.Axis(tickMinStep=1)),
        y=alt.Y("index", type="nominal", title="", axis=alt.Axis(labelPadding=10)),
        color=alt.Color("variable", legend=None),
    ).properties(height=300).configure_scale(
    bandPaddingInner=0.5).configure_axis(labelFontSize=20, titleFontSize=20)
)
data_ipa = pd.melt(ipa_df.reset_index(), id_vars=["index"])
chart_ipa = (
    alt.Chart(data_ipa)
    .mark_bar()
    .encode(
        x=alt.X("value", type="quantitative", title="", axis=alt.Axis(tickMinStep=0.5), scale=alt.Scale(domain=[0, 1.0])),
        y=alt.Y("index", type="nominal", title="", axis=alt.Axis(labelPadding=10)),
        color=alt.Color("variable", legend=None)
    ).configure_axis(labelFontSize=20).configure_scale(bandPaddingInner=0.5).properties(height=100)
)

with st.container() :
    st.write("#### 레진 및 소모품 재고")
    st.altair_chart(chart, use_container_width=True)
    st.markdown(hide_img_fs, unsafe_allow_html=True)
with st.container() :
    st.write("#### IPA 잔량")
    st.altair_chart(chart_ipa, use_container_width=True)
    st.markdown(hide_img_fs, unsafe_allow_html=True)
st.markdown("""---""")

##### Form3 <a href="https://formlabs.com/dashboard/" target="_blank">Dashboard </a>
buy_resin = str()
buy_etc = str()
buy_ipa = str()
for key, val in cur_resin_stock.items() :
    if val < 2 :
        _product_num = product_list[key]
        buy_resin += "<p> <a href=\"https://www.lcorporation.co.kr/product/product_detail.asp?product_num={val}\" target=\"_blank\"> {key} </a> </p>".format(val=_product_num, key=key)
for key, val in cur_etc_stock.items() :
    if key == 'IPA' :
        if val < 0.3 :
            _product_num = product_list[key]
            buy_ipa += "<p> <a href=\"https://www.lcorporation.co.kr/product/product_detail.asp?product_num={val}\" target=\"_blank\"> {key} </a> </p>".format(val=_product_num, key=key)
    else :
        if val < 1 :
            _product_num = product_list[key]
            buy_etc += "<p> <a href=\"https://www.lcorporation.co.kr/product/product_detail.asp?product_num={val}\" target=\"_blank\"> {key} </a> </p>".format(val=_product_num, key=key)

st.markdown(
    """
    #### 구매해야할 제품 링크
    """
)
cols = st.columns(3)
with cols[0] :
    st.markdown(
        """
        레진 재고 1개 이하
        """
    )
    st.markdown(buy_resin, unsafe_allow_html=True)
with cols[1] :
    st.markdown(
        """
        탱크 or 플랫폼 재고 0
        """
    )
    st.markdown(buy_etc, unsafe_allow_html=True)
with cols[2] :
    st.markdown(
        """
        IPA 잔량 30% (0.3) 이하
        """
    )
    st.markdown(buy_ipa, unsafe_allow_html=True)
st.markdown("""---""")
st.markdown(
    """
    #### 개별 탱크 현황
    """
)
t1, t2, t3, t4, t5, t6, = st.tabs(df_idx[0:6])
with t1 :
    st.radio(
        label="탱크 상태",
        options=("양호", "불량"), horizontal=True, key=1
    )
    t12 = st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=2
    )
with t2 :
    st.radio(
        "탱크 상태",
        ("양호", "불량"), horizontal=True, key=3
    )
    st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=4
    )
with t3 :
    st.radio(
        "탱크 상태",
        ("양호", "불량"), horizontal=True, key=5
    )
    st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=6
    )
with t4 :
    st.radio(
        "탱크 상태",
        ("양호", "불량"), horizontal=True, key=7
    )
    st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=8
    )
with t5 :
    st.radio(
        "탱크 상태",
        ("양호", "불량"), horizontal=True, key=9
    )
    st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=10
    )
with t6 :
    st.radio(
        "탱크 상태",
        ("양호", "불량"), horizontal=True, key=11
    )
    st.radio(
        "탱크 수명",
        ("양호", "초과"), horizontal=True, key=12
    )