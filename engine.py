import openai
from dotenv import load_dotenv
import os
import nft_storage
from nft_storage.api import nft_storage_api
from PIL import Image
import requests

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
ipfs_endpoint = os.getenv('IPFS_ENDPOINT')
ipfs_gateway = os.getenv('IPFS_GATEWAY')
ipfs_api_key = os.getenv('IPFS_API_KEY')
ipfs_api_secret = os.getenv('IPFS_API_SECRET')
ipfs_jwt_token = os.getenv('IPFS_JWT_TOKEN')

def artGen(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']


def uploadNFT(img_url, filename):
    response = requests.get(img_url)
    if response.status_code:
        fp = open(f'arts/{filename}.png', 'wb')
        fp.write(response.content)
        fp.close()

    filepath = os.path.join(os.getcwd(), f'arts/{filename}.png')
    image = Image.open(filepath)
    image.save(f"arts/{filename}-c.png",
               "PNG",
               optimize=True,
               quality=10)
    os.remove(f'arts/{filename}.png')

    configuration = nft_storage.Configuration(
        access_token=os.getenv('ACCESS_TOKEN')
    )

    with nft_storage.ApiClient(configuration) as api_client:
        api_instance = nft_storage_api.NFTStorageAPI(api_client)
        body = open(f'arts/{filename}-c.png', 'rb')
        api_response = api_instance.store(body, _check_return_type=False)
        os.remove(f'arts/{filename}-c.png')
        return api_response['value']['cid']


def mintNFT(name, description, cid, mint_to_address):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": os.getenv('NFTPORT_API_KEY'),
    }
    body = {
        "chain": "polygon",
        "name": name,
        "description": description,
        "file_url": f"https://ipfs.io/ipfs/{cid}",
        "mint_to_address": mint_to_address
    }
    response = requests.post(os.getenv('NFTPORT_ENDPOINT'), headers=headers, json=body)
    return response.text
