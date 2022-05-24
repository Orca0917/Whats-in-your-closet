from faulthandler import disable
import imp
from logging import PlaceHolder
import streamlit as st
from utils import paginator, get_images_url
from st_clickable_images import clickable_images
import pandas as pd
from rule_based import get_item_recommendation


st.image('https://www.noiremag.com/wp-content/uploads/2020/08/2020-fashion-trends-feature-696x392-1.jpg')
st.title('YUSINSA')

df=pd.read_excel('/opt/ml/input/data/raw_codishop/item_tag.xlsx',engine='openpyxl')
tags=pd.unique(df['tag'])
STATE_KEYS_VALS = [
    ("result", []),
    ("input_status", True),
    ("my_cloth",None),
    ("end_survey",False),
    ('clicked_item',-1),
    ('my_cloth_button',False), 
    ('survey_end',False),
    ('codi_click', None)
]
for k, v in STATE_KEYS_VALS:
    if k not in st.session_state:
        st.session_state[k] = v

def search(tag):
    if tag != []:
        temp=df[df['tag']==tag[0]] # 그 키워드를 가진 아이템
        st.session_state['result'] = temp.iloc[:,0].tolist()  #0:id column 

def input_status_change():
    st.session_state['input_status']=False

def set_value(key):
    st.session_state[key] = st.session_state["key_" + key]

survey_container=st.empty()
with survey_container.container():
    with st.container():
        # TODO : 검색 리스트 생성
        # TODO : 검색 이벤트 연결 -> on.click
        c1_col1,c1_col2 = st.columns(2)

        with c1_col1:
            input=st.multiselect(label='👕👖 갖고있는 옷을 검색하세요',options = tags,on_change=input_status_change)
            
        with c1_col2:
            st.write("")
            st.write("")
            input_button = st.button('🔍', on_click=search,args =(input,), disabled=st.session_state['input_status'])       
        

    if len(st.session_state['result'])!=0:
        st.markdown("""---""")
        image_dict=get_images_url(st.session_state['result'])  #['result']에는 키워드 #list 반환
        image_list=list(image_dict.values())
        item_ids=list(image_dict.keys())

        with st.container():
            st.markdown("### 갖고있는 옷과 가장 비슷한 사진을 골라주세요")
            image_iterator = paginator('',image_list,items_per_page=5,on_sidebar=False)
            indices_on_page, images_on_page = map(list, zip(*image_iterator))
            st.session_state['my_cloth']= clickable_images(images_on_page,titles=[f"Image #{str(i)}" for i in range(5)],
                                        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                        img_style={"margin": "5px", "height": "200px", "width" : "125px"},key='mySelect'
                                    )
            st.session_state['clicked_item']=item_ids[indices_on_page[st.session_state['my_cloth']]] # id가  들어옴

            st.session_state['my_cloth_button']=st.button('선택', disabled=st.session_state['clicked_item'] == -1)
if st.session_state['my_cloth_button']: # 버튼이 눌리면
    survey_container.empty() # 위의 내용들 삭제하기

    with st.container():
        st.write("선택한 아이템 : ")
        st.image(str(list(get_images_url([st.session_state['clicked_item']]).values())[0]), width=300) # st.session_state['clicked_item'] : id
        codis=get_item_recommendation(st.session_state['clicked_item'])

        st.markdown('### 관련 코디를 보고싶은 옷을 골라보세요')
        for codi in codis.keys():
            codi_id=codis[codi]
  
            if len(codi_id)!=0:
                st.markdown(f'#### {codi}')
                codi_list=list(get_images_url(codi_id).values())

                ######## 체크박스로 구현 한 후에 코디로 넘길 수 있을 것 같아요############################
                clickable_images(codi_list,titles=[f"Image #{str(i)}" for i in range(len(codi_id))],
                                            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
                                            img_style={"margin": "5px", "height": "200px", "width" : "125px"},key=f'{codi}Select')

        print(st.session_state)
        # if st.session_state[f'{codi}_click']:
        #     print(st.session_state[f'{codi}_click'])
        # st.markdown(f"Image #{top_click} clicked" if top_click > -1 else "No image clicked")

        # st.markdown("""---""")

        # with st.container():
        #     st.markdown('### 추천코디')
        #     fit_list=['https://image.msscdn.net/images/style/list/l_3_2022051912523500000002502.jpg' for i in range(5)]
        #     notfit_list=['https://image.msscdn.net/images/style/list/l_2_2022020309572400000037350.jpg' for i in range(5)]

        #     st.image(fit_list, use_column_width=False, caption=["some generic text"] * len(fit_list),width=125)
        #     st.markdown('#### 가진 옷과는 어울리지 않아요')
        #     st.image(notfit_list, use_column_width=False, caption=["some generic text"] * len(notfit_list),width=125)