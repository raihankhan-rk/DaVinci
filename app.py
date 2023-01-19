import streamlit as st
from engine import artGen, uploadNFT, mintNFT
import time
import json


def upload_and_mint():
    with st.spinner("Minting NFT..."):
        if st.session_state.name and st.session_state.desc and st.session_state.mint_to_address:
            cid = uploadNFT(st.session_state.img_url, st.session_state.prompt)
            mint_info = mintNFT(st.session_state.name, st.session_state.desc, cid, st.session_state.mint_to_address)
            st.success(f'NFT Minted successfully to {st.session_state.mint_to_address}')
            res = json.loads(mint_info)
            # st.json(res)
            st.info(f"""
                         Chain: {res['chain']}\n
                         Transaction Hash: {res['transaction_hash']}\n
                         Transaction External URL: {res['transaction_external_url']}\n
                         Contract Address: {res['contract_address']}\n\n
                         """)
            st.write(
                "Check out your NFT on OpenSea [https://opensea.io/account/private](https://opensea.io/account/private)")
        else:
            st.error("Please enter the Name, Description and the Minting Wallet Address!")


st.set_page_config(page_title="DaVinci - Generate & Mint NFTs with the help of AI within seconds", page_icon="🌄")
st.title("DaVinci")

st.subheader("Generate & Mint NFTs with the help of AI within seconds")

prompt = st.text_input('Prompt', placeholder="Type down your imagination and we'll turn it into an NFT...",
                       key='prompt')
print(f"\n{prompt}\n")

if st.button('Generate NFT'):
    with st.spinner("Generating NFT..."):
        st.session_state.img_url = artGen(prompt)
    st.image(image=st.session_state.img_url)
    time.sleep(5)
    st.success('NFT Generated Successfully!')

    with st.form(key='minting_form', clear_on_submit=False):
        name = st.text_input(label='', label_visibility='hidden', placeholder='Give your NFT a name', key='name')
        desc = st.text_area(label='', label_visibility='hidden', placeholder='Write a short description about your NFT',
                            key='desc')
        mint_to_address = st.text_input(label='', label_visibility='hidden', placeholder='Minting Wallet Address',
                                        key='mint_to_address')

        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.form_submit_button('Mint NFT', on_click=upload_and_mint)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer:before {content: '</> Developed by Raihan Khan | '}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
