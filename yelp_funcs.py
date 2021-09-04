
import requests
import numpy as np

MY_API_KEY = "yILzJVampuSNVKW8Qbdneiom6FdTeETngiBZ7iuzyP6ZyGQhSeQlVzsAPk0-TBcmMmk30ToXfLDtjaqiV3kYANb_1-x29A329LEfB7Et_0xFAA8XXkMdc7wVVJ4OYXYx"  # Replace this with your real API key

headers = {'Authorization': 'Bearer {}'.format(MY_API_KEY)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'


def get_yelp_data_by_location(lat, long, hotels_dict):

    offset = 0
    params_initial = {'term': 'hotel',

              'limit': '50',
              'latitude': lat,
              'longitude': long,
              'radius': 15000,
              'offset': offset}

    response = requests.get(search_api_url, headers=headers, params=params_initial, timeout=5)
    while (offset+50) <= 1000 and len(response.json()['businesses']) > 0:
        json_data = response.json()

        for business in json_data['businesses']:
            hotel_name = business.get('name').replace(',', '').replace('\u200b', '')
            hotel_id = business.get('id')
            hotel = np.array([hotel_name, business.get('review_count'), business.get('rating'),
                              business.get('coordinates').get('latitude'),
                              business.get('coordinates').get('longitude'),
                              business.get('price')])
            hotels_dict[hotel_id] = hotel


        offset += 50
        params = {'term': 'hotel',

                          'limit': '50',
                          'latitude': lat,
                          'longitude': long,
                          'radius': 15000,
                          'offset': offset}
        response = requests.get(search_api_url, headers=headers, params=params, timeout=5)

        print(len(hotels_dict))

if __name__ == '__main__':
    hotels = np.array([['name', 'review_count', 'rating', 'lat', 'long', 'price']])
    hotels_dict = {}

    get_yelp_data_by_location(51.59280743576024, -0.3194888029039521, hotels_dict)
    print('1111111111111111')
    get_yelp_data_by_location(51.57130427112887, 0.03694029137732054, hotels_dict)
    print('222222222222222')
    get_yelp_data_by_location(51.40754752916596, 0.0006052866204916811, hotels_dict)
    print('3333333333333333')
    get_yelp_data_by_location(51.42912807852067, -0.32121904122570577, hotels_dict)


    for hotel_id in hotels_dict:
        hotels = np.vstack((hotels, hotels_dict[hotel_id]))

    np.savetxt("yelp_data.csv", hotels, delimiter=",", fmt='%s')


