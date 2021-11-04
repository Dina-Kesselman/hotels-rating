import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import math

REQUEST_HEADER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"}
BOOKING_PREFIX = 'https://www.booking.com'
#MAIN_URL = 'https://www.booking.com/searchresults.en-gb.html?label=gog235jc-1DCAEoggI46AdIM1gDaGqIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ApSd8IsGwAIB0gIkNjlhYjk2MDAtZjIzMS00MjhhLTkyOTYtMTNlMmVhZmM0NjRl2AIE4AIB&sid=a9b62591d66290b566c1a75164c3906b&aid=397594&lang=en-gb&src=hotel&error_url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Fgb%2Fholiday-inn-london-regent-s-park.en-gb.html%3Faid%3D397594%3Blabel%3Dgog235jc-1DCAEoggI46AdIM1gDaGqIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ApSd8IsGwAIB0gIkNjlhYjk2MDAtZjIzMS00MjhhLTkyOTYtMTNlMmVhZmM0NjRl2AIE4AIB%3Bsid%3Da9b62591d66290b566c1a75164c3906b%3Ball_sr_blocks%3D3648712_244917015_2_2_0%3Bcheckin%3D2022-03-16%3Bcheckout%3D2022-03-21%3Bdest_id%3D-2601889%3Bdest_type%3Dcity%3Bdist%3D0%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Bhapos%3D0%3Bhighlighted_blocks%3D3648712_244917015_2_2_0%3Bhpos%3D0%3Bmatching_block_id%3D3648712_244917015_2_2_0%3Bno_rooms%3D1%3Breq_adults%3D2%3Breq_children%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bsr_order%3Dpopularity%3Bsr_pri_blocks%3D3648712_244917015_2_2_0__60690%3Bsrepoch%3D1635528357%3Bsrpvid%3Dcf5b7a91caa90021%3Btype%3Dtotal%3Bucfs%3D1%26%3B&highlighted_hotels=36487&hp_sbox=1&ss=London&is_ski_area=0&ssne=London&ssne_untouched=London&dest_id=-2601889&dest_type=city&checkin_year=2022&checkin_month=3&checkin_monthday=16&checkout_year=2022&checkout_month=3&checkout_monthday=21&group_adults=2&group_children=0&no_rooms=1&from_sf=1&nflt=price%3DILS-min-210-1'
MAIN_URL = 'https://www.booking.com/searchresults.html?label=gog235jc-1DCAEoggI46AdIM1gDaGqIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ApSd8IsGwAIB0gIkNjlhYjk2MDAtZjIzMS00MjhhLTkyOTYtMTNlMmVhZmM0NjRl2AIE4AIB&sid=a9b62591d66290b566c1a75164c3906b&aid=397594&src=searchresults&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Faid%3D397594%3Blabel%3Dgog235jc-1DCAEoggI46AdIM1gDaGqIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4ApSd8IsGwAIB0gIkNjlhYjk2MDAtZjIzMS00MjhhLTkyOTYtMTNlMmVhZmM0NjRl2AIE4AIB%3Bsid%3Da9b62591d66290b566c1a75164c3906b%3Btmpl%3Dsearchresults%3Bcheckin_month%3D12%3Bcheckin_monthday%3D1%3Bcheckin_year%3D2021%3Bcheckout_month%3D12%3Bcheckout_monthday%3D5%3Bcheckout_year%3D2021%3Bcity%3D-2601889%3Bclass_interval%3D1%3Bdest_id%3D-2601889%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bsrpvid%3Db14979dc8f070091%3Bss%3DLondon%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3DLondon%3Bssne_untouched%3DLondon%3Btop_ufis%3D1%26%3B&ss=London&is_ski_area=0&ssne=London&ssne_untouched=London&city=-2601889&checkin_year=2022&checkin_month=1&checkin_monthday=10&checkout_year=2022&checkout_month=1&checkout_monthday=17&group_adults=2&group_children=0&no_rooms=1&sb_changed_group=1&sb_changed_dates=1&from_sf=1&nflt=price%3DILS-min-500-1'
'''
'name', 'wifi', 'parking', 'luggage storage', '24-hour front desk', 'daily housekeeping',
                            'smoke-free', 'pets ok', 'room service', 'elevator', 'air conditioning', 'tv',
                            '24-hour security', 'wheelchair accessible', 'refrigerator', 'electric kettle'
'''
def parse_hotel_facilities(hotel_facilities, hotel_name, hotels_dict):
    hotel = np.array([hotel_name])
    if 'WiFi is available in the hotel rooms and is free of charge.' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'parking?????????????' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Luggage storage' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if '24-hour front desk' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Daily housekeeping' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Non-smoking throughout' or 'Non-smoking rooms' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Pets are allowed. Charges may be applicable.' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Room service' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Upper floors accessible by elevator' or 'Lift' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Air conditioning' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'TV' or 'Flat-screen TV' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if '24-hour security' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Wheelchair accessible' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Refrigerator' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)
    if 'Electric kettle' in hotel_facilities:
        hotel = np.append(hotel, 1)
    else:
        hotel = np.append(hotel, 0)

    hotels_dict[hotel_name] = hotel


def get_hotel_info(hotel_url, hotel_name, hotels_dict):
    response = requests.get(hotel_url, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.content, "lxml")
    res_text = soup.findAll('div', class_='hotel-facilities__list')
    res_text = res_text[0].get_text()
    hotel_facilities = re.split('\n+', res_text)
    parse_hotel_facilities(hotel_facilities, hotel_name, hotels_dict)


def get_booking_data():
    hotels = np.array([['name', 'wifi', 'parking', 'baggage storage', '24-hour front desk', 'daily housekeeping',
                        'smoke-free', 'pets', 'room service', 'elevator', 'air conditioning', 'tv',
                        '24-hour security', 'wheelchair accessible', 'refrigerator', 'electric kettle']])
    hotels_dict = {}
    response = requests.get(MAIN_URL, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.content, "lxml")
    num_results_meta = soup.findAll('div', class_='ea52000380')
    #num_results_meta = soup.findAll('div', class_='results-meta')
    num_hotel_results = num_results_meta[0].text.split(' ')[1]
    num_hotel_results = num_hotel_results.replace(',', '')
    num_hotel_results = int(num_hotel_results)
    num_pages = math.ceil(float(num_hotel_results)/25)
    offset = 0

    for i in range(0, num_pages+1):
        print(f'page num is: {i+1} ===================================')
        #hotel_urls = soup.findAll('a', class_='js-sr-hotel-link')
        hotel_urls = soup.findAll('a', class_='fb01724e5b')
        j=1
        for url in hotel_urls:
            print(f'url number {j}')
            #hotel_url = BOOKING_PREFIX + url.attrs['href'].replace('\n', '')
            hotel_url = url.attrs['href']
            print(hotel_url)
            #hotel_name = url.text.split('\n\n')[1]
            hotel_name = url.contents[0].text.replace(',', '').replace('\u200b', '')
            get_hotel_info(hotel_url, hotel_name, hotels_dict)
            j = j+1
        offset = offset + 25
        response = requests.get(f'{MAIN_URL}&offset={offset}', headers=REQUEST_HEADER)
        soup = BeautifulSoup(response.content, "lxml")


    for name in hotels_dict:
        hotels = np.vstack((hotels, hotels_dict[name]))

    np.savetxt("booking_data.csv", hotels, delimiter=",", fmt='%s')
    pass

if __name__ == '__main__':
    URL = 'https://www.booking.com/searchresults.en-gb.html?aid=397594&label=gog235jc-1FCAEoggI46AdIM1gDaGqIAQGYAQm4ARfIAQzYAQHoAQH4AQyIAgGoAgO4AuGcrooGwAIB0gIkYzUxNzRlZGQtMDg1Ni00N2IzLTk0NzYtMmM5OTljNDg1MGYx2AIG4AIB&sid=63c61e8945df8c2fd7e74ea082a476e0&tmpl=searchresults&checkin_month=3&checkin_monthday=8&checkin_year=2022&checkout_month=3&checkout_monthday=9&checkout_year=2022&class_interval=1&dest_id=-2601889&dest_type=city&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&raw_dest_type=city&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&src=index&srpvid=74679d54314d012e&ss=London&ss_all=0&ssb=empty&sshis=0&ssne=London&ssne_untouched=London&top_ufis=1&nflt=accessible_facilities%3D187%3B&rsf='
    '''
    offset = 25
    for i in range(1,5):
        url = f'{URL}&offset={offset}'
        response = requests.get(URL, headers=REQUEST_HEADER)
        offset = offset + 25
        pass
    pass
    
    response = requests.get(MAIN_URL, headers=REQUEST_HEADER)
    soup = BeautifulSoup(response.content, "lxml")
    num_results_meta = soup.findAll('div', class_='results-meta')
    num_hotel_results = num_results_meta[0].text.split(' ')[1]
    num_hotel_results = num_hotel_results.replace(',', '')
    num_hotel_results = int(num_hotel_results)
    num_pages = math.ceil(float(num_hotel_results)/25)
    pass
    '''
    get_booking_data()



