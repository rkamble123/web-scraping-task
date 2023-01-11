from bs4 import BeautifulSoup
from selenium import webdriver
import time

scraper= webdriver.Chrome('./cromedriver.exe')

scraper.get('https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fb%2F%3F_encoding%3DUTF8%26node%3D15325111031%26pf_rd_r%3D4C9M81834J9NNFF2TMJ2%26pf_rd_p%3Dbcaa488e-fdfb-4f34-b9a7-8ba0071ce298%26pd_rd_r%3Dcc247a59-8129-487e-9319-c8b98249452c%26pd_rd_w%3DAs07O%26pd_rd_wg%3DIYI2X%26ref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')

time.sleep(3)

mob_number = scraper.find_element('xpath','//*[@id="ap_email"]').send_keys('9920220422')
continue_btn = scraper.find_element('xpath','//*[@id="continue"]').click()
time.sleep(3)
password = scraper.find_element('xpath','//*[@id="ap_password"]').send_keys('test@123')
log_in_btn = scraper.find_element('xpath','//*[@id="signInSubmit"]').click()
time.sleep(3)

returns_and_orders = scraper.find_element('xpath','//*[@id="nav-orders"]/span[1]').click()
time.sleep(5)

select_year = scraper.find_element('xpath','//*[@id="a-autoid-1-announce"]').click()
time.sleep(3)

required_url= scraper.current_url
print(required_url)

# enter_year = scraper.find_element('xpath','//*[@id="a-popover-1"]/div/div/ul/li[8]').click()

# time.sleep(3)
# current_url= scraper.current_url
# print(current_url)

page_html  = scraper.page_source
# print(page_source)

soup = BeautifulSoup(page_html,'lxml')
# print(soup)


year_list = soup.find('ul',class_ = 'a-nostyle a-list-link')
# print(year_list)
year_list = year_list.find_all('li',class_='a-dropdown-item')
# print(year_list)
# print(len(year_list))

final_yesr_list =[]
for i in year_list:
    # print(i)
    if 'Archived Orders' not in str(i):
        final_yesr_list.append(i)

# print(len(final_yesr_list))

# time.sleep(3)
# scraper.get(required_url)
# time.sleep(3)

data_dict = {}
data_found_dict = {}

for year_data in final_yesr_list :
    # print(type(year_data))
    year_no=year_data.text
    # print(year_no)
    # print(type(year_no))
    yesr_no=year_no.replace('\n','')
    year_no= year_no.strip()
    if year_no == 'last 30 days':
        year_no = 'last30'
    elif year_no == 'past 3 months':
        year_no = 'months-3'
    else:
        year_no= f'year-{year_no}'

    path = fr'https://www.amazon.in/gp/your-account/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter={year_no}'
    # print(path)

    scraper.get(path)
    time.sleep(2)

    order_container = scraper.find_element('xpath','//*[@id="ordersContainer"]').text
    # print(order_container)
    if 'You have not placed any orders' in order_container:
        data_dict[year_no] = 'No Data'
        pass
    else: 
        # scraper.find_element
        product_name = scraper.find_element('xpath','//*[@id="ordersContainer"]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]').text

        time.sleep(2)

        scraper.find_element('xpath', '//*[@id="ordersContainer"]/div[2]/div[1]/div/div/div/div[2]/div[2]/ul/a').click()

        order_id=scraper.find_element('xpath','//*[@id="orderDetails"]/div[2]/div[1]/div/span[2]').text
        # print(product_name)
        order_id = order_id.replace('\n','')
        order_id = order_id.replace('Order#','')
        # print('order_id',order_id)
        order_shiping_address = scraper.find_element('xpath','//*[@id="orderDetails"]/div[4]/div/div/div/div[1]/div/div[1]/div[1]').text
        order_shiping_address = order_shiping_address.replace('\n',' ')
        order_shiping_address = order_shiping_address.replace("Shipping Address",'')
        # print('order_shiping_address', order_shiping_address)
        payment_method = scraper.find_element('xpath','//*[@id="orderDetails"]/div[4]/div[1]/div/div/div/div[1]/div/div[2]/div[1]/div').text
        payment_method = payment_method.replace('\n','')
        payment_method = payment_method.replace('Payment Method','')
        # print('payment_method', payment_method)
        order_summery = scraper.find_element('xpath','//*[@id="od-subtotals"]').text
        order_summery = order_summery.replace('\n',',')
        order_summery = order_summery.replace('Order Summary','')
        # print('order_summery', order_summery)


        product_dict= {
            'product_name':product_name,
            'order_id':order_id,
            'Shiping_address':order_shiping_address,
            'Payment_method':payment_method,
            'order_summary':order_summery
        }

        data_found_dict[product_name] = product_dict
        print()
        print(data_found_dict)

        time.sleep(2)
        break

# print(data_found_dict)

    # break
time.sleep(3)
# print(data_dict)

