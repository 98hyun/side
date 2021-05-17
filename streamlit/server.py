## library
import streamlit as st
import requests

## config
import config

def main():
    '''deploy on gcp'''
    api_key=config.api_key
    url=f'https://api.corona-19.kr/korea/country/new/?serviceKey={api_key}'
    info=f'https://api.corona-19.kr/korea/?serviceKey={api_key}'

    ## parse
    info_res=requests.get(info)
    info_json=info_res.json()
    res=requests.get(url)
    res_json=res.json()

    ## today - tinydb check
    from datetime import datetime 

    today=datetime.today().strftime('%Y-%m-%d')

    res_json['today']=today
    all_result=res_json.copy()
    all_result.update(info_json)

    from tinydb import TinyDB,Query

    db=TinyDB('corona_db.json')

    today_obj=sorted(db.all(),key=lambda k:k['today'])

    if today_obj[-1]['today']!=today:
        db.insert(all_result)

    ## get data from region select bar
    def getdata(region):
        # 신규확진환자수
        newcase=res_json[region]['newCase'].strip()
        # 확진환자수
        totalCase=res_json[region]['totalCase'].strip()
        # 완치자수
        recovered=res_json[region]['recovered'].strip()
        # 사망자
        death=res_json[region]['death'].strip()
        # 발생률
        percentage=res_json[region]['percentage'].strip()
        # 전일대비증감-지역발생
        newCcase=res_json[region]['newCcase'].strip()
        # 전일대비증감-해외유입
        newFcase=res_json[region]['newFcase'].strip()
        if region=='korea':
            day_recover=info_json['TodayRecovered']
            day_death=info_json['TodayDeath']
            day_patient=info_json['TotalCaseBefore']
            return newcase,totalCase,day_recover,day_death,percentage,newCcase,newFcase
        else:
            return newcase,totalCase,recovered,death,percentage,newCcase,newFcase

    st.title("코로나 현황 대쉬보드")

    st.write(f"""
    {info_json['updateTime']}
    """)

    region=("전국","서울","부산","대구","인천","광주","대전","울산","세종",
    "경기","강원","충북","충남","전북","전남","경북","경남","제주")
    select_region=st.sidebar.selectbox("지역 선택",region)

    if select_region=='전국':
        region='korea'
        result=getdata(region)
    elif select_region=='서울':
        region='seoul'
        result=getdata(region)
    elif select_region=='부산':
        region='busan'
        result=getdata(region)
    elif select_region=='대구':
        region='daegu'
        result=getdata(region)
    elif select_region=='인천':
        region='incheon'
        result=getdata(region)
    elif select_region=='광주':
        region='gwangju'
        result=getdata(region)
    elif select_region=='대전':
        region='daejeon'
        result=getdata(region)
    elif select_region=='울산':
        region='ulsan'
        result=getdata(region)
    elif select_region=='세종':
        region='sejong'
        result=getdata(region)
    elif select_region=='경기':
        region='gyeonggi'
        result=getdata(region)
    elif select_region=='강원':
        region='gangwon'
        result=getdata(region)
    elif select_region=='충북':
        region='chungbuk'
        result=getdata(region)
    elif select_region=='충남':
        region='chungnam'
        result=getdata(region)
    elif select_region=='전남':
        region='jeonnam'
        result=getdata(region)
    elif select_region=='전북':
        region='jeonbuk'
        result=getdata(region)
    elif select_region=='경북':
        region='gyeongbuk'
        result=getdata(region)
    elif select_region=='경남':
        region='gyeongnam'
        result=getdata(region)
    elif select_region=='제주':
        region='jeju'
        result=getdata(region)

    ## kpi setting
    kpi1,kpi2,kpi3=st.beta_columns(3)

    with kpi1:
        st.markdown("<h2 style='text-align:center'>신규확진자 수</h2>",unsafe_allow_html=True)
        newcase=int(result[0].replace(',',''))
        if newcase>0:
            st.markdown(f"<h2 style='text-align:center;color:red'>▲ {newcase}</h2>",unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='text-align:center;color:green'>▼ {newcase}</h2>",unsafe_allow_html=True)
    with kpi2:
        st.markdown("<h2 style='text-align:center'>누적 확진자 수</h2>",unsafe_allow_html=True)
        totalCase=int(result[1].replace(',',''))
        st.markdown(f"<h2 style='text-align:center;'>{totalCase}</h2>",unsafe_allow_html=True)
    with kpi3:
        st.markdown("<h2 style='text-align:center'>완치자 수</h2>",unsafe_allow_html=True)
        recovered=int(result[2].replace(',',''))
        if recovered>0:
            st.markdown(f"<h2 style='text-align:center;color:red'>{recovered}</h2>",unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='text-align:center;color:green'>{recovered}</h2>",unsafe_allow_html=True)

    kpi4,kpi5,kpi6,kpi7=st.beta_columns(4)

    with kpi4:
        st.markdown("<h2 style='text-align:center'>사망자 수</h2>",unsafe_allow_html=True)
        death=int(result[3].replace(',',''))

        if region=='korea':
            if newcase>0:
                st.markdown(f"<h2 style='text-align:center;color:red'>▲ {death}</h2>",unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='text-align:center;color:green'>▼ {death}</h2>",unsafe_allow_html=True)
        else:        
            if newcase>0:
                st.markdown(f"<h2 style='text-align:center;color:red'>{death}</h2>",unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='text-align:center;color:green'>{death}</h2>",unsafe_allow_html=True)
    with kpi5:
        st.markdown("<h2 style='text-align:center'>발생률</h2>",unsafe_allow_html=True)
        percentage=result[4]
        st.markdown(f"<h2 style='text-align:center;color:red;'>{percentage}%</h2>",unsafe_allow_html=True)
    with kpi6:
        st.markdown("<h2 style='text-align:center'>지역발생 수</h2>",unsafe_allow_html=True)
        newCcase=int(result[5].replace(',',''))
        st.markdown(f"<h2 style='text-align:center;color:red'>▲ {newCcase}</h2>",unsafe_allow_html=True)
    with kpi7:
        st.markdown("<h2 style='text-align:center'>해외유입 수</h2>",unsafe_allow_html=True)
        newFcase=int(result[6].replace(',',''))
        st.markdown(f"<h2 style='text-align:center;color:red'>▲ {newFcase}</h2>",unsafe_allow_html=True)

if __name__=='__main__':
    main()
    
## predict with fbprophet (plan to do)