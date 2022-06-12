# Introduction
수집한 데이터를 전처리하는 소스입니다.

## How to Run?
1. 데이터 전처리
    ``` 
    python3 preprocess.py
    ```

2. 상호작용 행렬 생성
    ```
    python3 cluster_item_interaction_matrix.py
    ```

<br>

## 디렉터리 구조
```
    📦Preprocessing
    ┣ 📜preprocess.py
    ┣ 📜cluster_item_interaction_matrix.py
    ┣ 📂utils
    ┃ ┣ 📂codi
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┗ 📜codi_preprocess_functions.py
    ┃ ┣ 📂item
    ┃ ┃ ┣ 📜__init__.py
    ┃ ┃ ┗ 📜item_preprocess_functions.py
    ┃ ┣ 📜utils_codi.py
    ┃ ┣ 📜utils_item.py
    ┃ ┣ 📜utils_item_fit.py
    ┃ ┗ 📜utils_item_four_season.py
    ┣ 📂testing_files
    ┃ ┣ 📜color_extraction_test.ipynb
    ┃ ┗ 📜imgae_loading_tester.ipynb
    ┗ 📜README.md
```

<br>

## Directory Explanation

<img src="https://user-images.githubusercontent.com/44887886/173222170-ae7ce245-a8ca-4e22-8e7d-65545a0647cf.png" width="700" height="320" align="center">

- 📜 `preprocess.py` : 위의 그림과 같이 정해진 순서대로 전처리를 진행합니다.
- 📜 `Cluster_item_interaction_matrix.py` : 룰베이스에 필요한 상호작용 행렬을 생성합니다.
- 📂 utils : 전처리에 필요한 함수가 모여있습니다.
- 📂 testing_files : 수집한 데이터를 검수합니다.
    - 📜 `color_extraction_test.ipynb` : 아이템 이미지에서 추출한 색상이 올바른지 검수합니다.
    - 📜 `imgae_loading_tester.ipynb` : 아이템 이미지가 로딩되는지 검수합니다.


<br>

## 데이터 전처리 설명

###  Item 속성 Table

1. Item Table

    | Table | Feature | 설명        | 결측치 처리                 | 비고 |
    |:-----:|:-------:|:---------:|:-------------------------:|:---:|
    |Item   |id       | 아이템 ID     | ❌                        |     |
    |Item   |name     | 상품명      | ❌                         |     |
    |Item   |big_class| 대분류      | ❌                         | 유사한 대분류 통일, 악세사리 및 기타 대분류 제거 |
    |Item   |mid_class| 중분류      | ❌                         | 유사한 중분류 통일     |
    |Item   |brand    | 브랜드      | ❌                         |      |
    |Item   |serial_number| 품번    | ❌                         |      |
    |Item   |price    | 가격        | ❌                         |      |
    |Item   |likes    | 좋아요 수    | 0                         |   |
    |Item   |R, G, B  | 색상 R, G, B| ❌                        | 이미지에서 가장 높은 비율을 차지하는 색상의 R, G, B 값 추출|
    |Item   |rating   | 평점        | 모든 아이템 평점의 평균|       |      |
    |Item   |gender   | 성별        | '유니섹스'                  |      |
    |Item   |season_year | 출시 연도 | NULL                      | season feature에서 추출 |
    |Item   |season   | 출시 시즌    | NULL                      | 출시 연도를 제거하고 계절 정보만 추출 |
    |Item   |view_count| 조회 수     | NULL                      | str에서 Int로 타입 변환 |
    |Item   |cum_sale  | 누적판매 수  | NULL                      | str에서 Int로 타입 변환 |
    |Item   |most_bought_age_class|구매 비율이 가장 높은 연령층 클래스|6 | Item_buy_age 테이블 참조 |
    |Item   |men_bought_ratio|남성 사용자의 구매 비율|50             | Item_buy_gender 테이블 참조 |
    |Item   |color_id| 색상 아이디    | ❌                         | R, G, B 값을 활용해 클러스터링 |
    |Item   |cluster_id|클러스터 아이디 | ❌                        | 중분류와 색상을 활용해 클러스터링 |
    |Item   |img_url   |이미지 주소   | ❌                         |         |
    |Item   |url       |상품 페이지 주소| ❌                        |         |


2. Item_fit Table

    |  Table | Feature | 설명        | 결측치 처리                 | 비고 |
    |:------:|:-------:|:----------:|:------------------------:|:---:|
    |Item_fit| id      | 아이템 ID    | ❌                       | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    |Item_fit| fit     | 핏         | 아이템 태그에서 핏 정보 활용    | Item_tag table 참조    |

3. Item_tag Table
    
    |  Table | Feature | 설명        | 결측치 처리                 | 비고 |
    |:------:|:-------:|:----------:|:------------------------:|:---:|
    |Item_tag| id      | 아이템 ID    | ❌                       | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    |Item_tag| tag     | 태그        | ❌                       |   |


4. Item_four_season Table

    |      Table     | Feature     | 설명        | 결측치 처리                 | 비고 |
    |:--------------:|:-----------:|:----------:|:------------------------:|:---:|
    |Item_four_season| id          | 아이템 ID    | ❌                   | Item table에서 대분류 필터링을 통해 제거된 아이템 제거 Id (동기화) | 
    |Item_four_season| four_season | 사계절 정보   | 아이템의 출시 시즌 정보 활용    | Item table 참조    |

5. Item_rel_codi_url Table

    |      Table     | Feature     | 설명        | 결측치 처리         | 비고 |
    |:--------------:|:-----------:|:----------:|:----------------:|:---:|
    |Item_rel_codi_url| id          | 아이템 ID    | ❌              | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) |
    |Item_rel_codi_url| rel_codi_url| 아이템이 사용된 코디 페이지 주소 | ❌|     |

6. Item_buy_gender Table

    |     Table     |   Feature   | 설명      | 결측치 처리   | 비고 |
    |:-------------:|:-----------:|:--------:|:----------:|:---:|
    |Item_buy_gender| id          | 아이템 ID  | ❌         | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    |Item_buy_gender| buy_men     | 남성 사용자 구매 비율    | ❌          |   |
    |Item_buy_gender| buy_women   | 여성 사용자 구매 비율    | ❌          |   |

7. Item_buy_age Table

    |     Table     |   Feature   | 설명      | 결측치 처리   | 비고 |
    |:-------------:|:-----------:|:--------:|:----------:|:---:|
    |Item_buy_age   | id          | 아이템 ID  | ❌         | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    |Item_buy_age   | buy_age_18  | ~18세 사용자 구매 비율      | ❌          |   |
    |Item_buy_age   | buy_age_19_23  | 19세~23세 사용자 구매 비율      | ❌          |   |
    |Item_buy_age   | buy_age_24_28  | 24세~28세 사용자 구매 비율      | ❌          |   |
    |Item_buy_age   | buy_age_29_33  | 29세~33세 사용자 구매 비율      | ❌          |   |
    |Item_buy_age   | buy_age_34_39  | 34세~39세 사용자 구매 비율      | ❌          |   |
    |Item_buy_age   | buy_age_40  | 40세~ 사용자 구매 비율      | ❌          |   |


8. Item_codi_id Table

    |     Table     |   Feature   | 설명      | 결측치 처리   | 비고 |
    |:-------------:|:-----------:|:--------:|:----------:|:---:|
    |Item_codi_id   | id          | 아이템 ID  | ❌         | Item table에서 대분류 필터링을 통해 제거된 아이템 Id 제거 (동기화) | 
    |Item_codi_id   | codi_id     | 코디 ID   | ❌         |      |    

### Codi 속성 Table

1. codi Table

    | Table | Feature | 설명          | 결측치 처리   | 비고 |
    |:-----:|:-------:|:------------:|:----------:|:---:|
    |codi   |id       | 코디 ID       | ❌         | Item_codi_id table에서 제거된 코디 Id 제거 (동기화) |
    |codi   |style    | 코디 스타일     | ❌         |     |
    |codi   |popularity| 조회 수       | ❌         |     |
    |codi   |img_url  | 코디 이미지 주소 | ❌         |     |
    |codi   |url      | 상품 페이지 주소 | ❌         |     |


2. codi_tag Table

    | Table | Feature | 설명          | 결측치 처리   | 비고 |
    |:-----:|:-------:|:------------:|:----------:|:---:|
    |codi   |id       | 코디 ID       | ❌         | codi table에서 제거된 코디 Id 제거 (동기화) |
    |codi   |tag      | 코디 태그     | ❌         |     |

<br>

