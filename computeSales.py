"""Compute Sales
"""

import sys
import time
import json


def read_json_file(file_name):
    """
    Read a JSON file
    Args:
        file path (string)
    Returns JSON data
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        data = ''
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            print("Invalid JSON file '" + file_name + "'")
            data = None
        else:
            print("Valid JSON file '" + file_name + "'")

        return data


def validate_json_file(json_1, json_2):
    """
    Validate what json file has Sales information and
    what json file has Products information.
    Args:
        json_1: list with the data of one json file
        json_2: list with the data of one json file
    Returns the json in a especific order: Sales - Prodcuts
    """
    sales = ''
    products = ''
    if "SALE_ID" in json_1[0] and "title" in json_2[0]:
        sales = json_1
        products = json_2
    elif "SALE_ID" in json_2[0] and "title" in json_1[0]:
        sales = json_2
        products = json_1
    else:
        products = None
        sales = None

    return sales, products


def process_total_sales(sales, products):
    """
    Process the total sales
    Args:
        sales (list): all the sales
        products (list): all the products
    """
    total = 0
    for sale in sales:
        p_name = sale.get('Product')
        if next((item for item in products if item['title'] == p_name), False):
            # print('exists')
            for product in products:
                if p_name == product.get('title'):
                    if product.get('price', 0) is not None:
                        total = (total +
                                 (sale.get('Quantity', 0) *
                                  product.get('price', 0)))
                    else:
                        print('[Error] Cannot get price for product ' +
                              product.get('title'))
        else:
            print('[Error] Product in Sales not found in Prodcuts.')

    print('total sales: ' + str(total))
    return total


def main():
    """
    main function
    """
    start_time = time.time()
    print('<<< Compute Sales >>>')

    file_name_1 = ''
    file_name_2 = ''
    if len(sys.argv) == 3:
        file_name_1 = sys.argv[1]
        file_name_2 = sys.argv[2]
    else:
        print("[Error] Not enough input parameters. ")
        print("Run scrip: " +
              "python compute_sales.py" +
              "[path]/ProductList.json [path]/Sales.json")
        sys.exit(0)

    print("file 1: " + file_name_1)
    print("file 2: " + file_name_2)

    json_file_1 = read_json_file(file_name_1)
    json_file_2 = read_json_file(file_name_2)
    total_sales = 0

    if json_file_1 is None or json_file_2 is None:
        print("Failed reading json files.")
    else:
        sales, products = validate_json_file(json_file_1, json_file_2)
        if sales is None or products is None:
            print("Failed reading json files.")
        else:
            total_sales = process_total_sales(sales, products)
            with open("SalesResults.txt", "w", encoding='utf-8') as res_file:
                res_file.write("Total cost of sales: " + str(total_sales))

    elapsed_time = time.time() - start_time
    print("Time taken: " + str(elapsed_time) + " seconds.\n")


if __name__ == '__main__':
    main()
