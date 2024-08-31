import pandas as pd
from bs4 import BeautifulSoup
import requests
from PIL import Image

# header for https requests,as otherwise server doesn't respond with the html page
head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
PAGES=1
def all_data():
    data = []
    i=1
    while True:  
        response = requests.get(
            "https://www.yoshops.com/products?page="+str(i), headers=head)

        soup = BeautifulSoup(response.text, "html.parser")

        # adding all html elements with clas product to data list.
        data += soup.select(".product")
        pager=len(soup.select(".arrow.disabled")) if i!=1 else 0

        if not(len(soup.select(".arrow")) and pager-1):
            break
        i+=1


    # little bit of cleaning of datas
    refined_data = []  # data after processing will be saved here
    for i in data:
        link = "https://www.yoshops.com/"+i.select_one(".product-link")["href"]
        title = i.select_one(".product-title").get_text()
        temp = i.select_one(".product-price").get_text().split("₹")
        old_price = temp[1]
        new_price = temp[2]
        div = i.find('div', {"class": "product-thumb-inner"})
        image_url = div.find('img').attrs['src']
        has_image = "true" if not("noimage" in image_url) else "false"
        refined_data.append([link, title, old_price, new_price, has_image])

    # saving data
    df = pd.DataFrame(refined_data)
    df.columns = ["link", "title", "old_price", "new_price", "has_image"]
    df.to_excel("data.xlsx",index=False)
    print("total no of products: ",len(df))

def all_category_data(base_url):
    data = []
    i=1
    while True: 
        response = requests.get(
            base_url+"?page="+str(i), headers=head)

        soup = BeautifulSoup(response.text, "html.parser")

        # adding all html elements with clas product to data list.
        data += soup.select(".product")
        pager=len(soup.select(".arrow.disabled")) if i!=1 else 0
        if not(len(soup.select(".arrow")) and pager-1):
            break
        i+=1

    # little bit of cleaning of datas
    refined_data = []  # data after processing will be saved here
    for i in data:
        link = "https://www.yoshops.com/"+i.select_one(".product-link")["href"]
        title = i.select_one(".product-title").get_text()
        temp = i.select_one(".product-price").get_text().split("₹")
        old_price = temp[1]
        new_price = temp[2]
        div = i.find('div', {"class": "product-thumb-inner"})
        image_url = div.find('img').attrs['src']
        has_image = "true" if not("noimage" in image_url) else "false"
        refined_data.append([link, title, old_price, new_price, has_image])

    # saving data
    df = pd.DataFrame(refined_data)
    df.columns = ["link", "title", "old_price", "new_price", "has_image"]
    df.to_excel(base_url.split("/t/")[1]+".xlsx",index=False)
    print("total no of products: ",len(df))
    print("file saved as: "+base_url.split("/t/")[1]+".xlsx")


def given_product(link):
    response = requests.get(link, headers=head)
    soup = BeautifulSoup(response.text, "html.parser")
    image = soup.select_one("#product-image")["src"]
    has_image = not("noimage" in image)
    title = soup.select_one("#product-name").get_text()
    regular_price = soup.select_one("#regular-price").get_text()[1:]
    sale_price = soup.select_one("#sale-price").get_text()[1:]
    description = soup.select_one(".single-product-description").get_text()
    print("\n")
    print("has image:            ", has_image)
    print("title:                ", title)
    print("regular price:        ", regular_price)
    print("sale price            ", sale_price)
    print("\n\n")
    print("product description: \n\n", description.strip())
    print("\n")
    df = pd.DataFrame(
        [[title, regular_price, sale_price, has_image, description]])
    df.columns = ["title", "regular_price",
                  "sale_price", "has_image", "description"]
    df.to_excel(title+".xlsx")

    print("\ndata saved in excel file as well.")
    if has_image:
        im = Image.open(requests.get(image, stream=True).raw)
        im.save("image.png")
    else:
        im = Image.open(requests.get(
            "https://media.istockphoto.com/photos/no-image-available-picture-id531302789", stream=True).raw)
        im.save("image.png")

string="\nselect the task: \n\t enter 1 to download whole data \n\t enter 2 to download for particular category \n\t enter 3 for particular product \n\t enter 4 to exit \n input: "
while True:
    operation=input(string).strip()
    if operation=="4":
        break
    if operation == '3':
            print("\n")
            link = input("enter the url of a product: ").strip()
            if "yoshops.com" not in link:
                print("please enter a valid link associated with yoshops.com product")
                continue
            link="https://www."+link[link.index("yoshops.com"):]
            try:
                given_product(link)
            except:
                print("\n oops!! something wrong happened,please check your url")
            continue
    if operation =='1':
        print("\n [   downloading...   ]")
        all_data()
        print("data.xlsx file created in current folder")
        continue
    if operation=='2':
        print("\n")
        link = input("enter the base url of a category: ").strip()
        if "yoshops.com/t/" not in link:
            print("please enter a valid link associated with yoshops.com category")
            continue
        link="https://www."+link[link.index("yoshops.com"):]
        try:
            print("\n [   downloading...   ]")
            all_category_data(link)
        except:
            print("\n oops!! something wrong happened,please check your url")
        continue
    
    print("\nplease enter a value between [1 and 4] \n")

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(product_data)

    # Save the DataFrame to an Excel file
    df.to_excel('products_missing_image.xlsx', index=False)

    print("Successfully saved products with missing images to 'products_missing_image.xlsx'")

if __name__ == '__main__':
    main()