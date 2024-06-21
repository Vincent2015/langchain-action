#from langchain.utilities import SerpAPIWrapper
from langchain_community.utilities import SerpAPIWrapper
def get_UID(flower: str): 
    """Searches for Linkedin or twitter Profile Page.""" 
    search = SerpAPIWrapper() 
    try:
        res = search.run(f"{flower}") 
    except Exception as e:
        print(e)
    return res