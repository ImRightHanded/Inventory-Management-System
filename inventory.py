import os

def print_title(title: str):
    """
    Clear the console then display the menu header
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n -- {title} -- \n")

def duplicate_check(input_prompt: str, data_content) -> str:
    """
    Check if the input data already exist or not in the database
    """
    while True:
        user_input = input(f"{input_prompt}").upper()
        for data_list in data_content:
            if data_list[0] == user_input:
                print("The ID already exist on the database")
                break
        else:
            return user_input

def format_file_header(file_name):
    """
    Return the header of the file if the file has it.
    Append a predefined header if the file does not contain any
    """
    headers = {
        "products.txt": "Product ID | Product Name | Qty | Description | Price (MYR)",
        "suppliers.txt": "Supplier ID | Name | Contact",
        "orders.txt": "Order ID | Product Name | Qty | Clients"
    }

    with open(file_name, 'r') as file:
        first_line = file.readline().strip()

    if first_line == headers[file_name]:
        return first_line

    with open(file_name, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(headers[file_name] + "\n" + original_content)

def load_data(file_name):
    """
    Load data from the file
    """
    data = []

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()[1:]
            data = [line.strip().split(',') for line in lines]
    else:
        with open(file_name, 'w'):
            pass
        format_file_header(file_name)

    return data

def save_data(file_name, data_content):
    """
    Save data to the file
    """
    file_header = format_file_header(file_name)

    with open(file_name, 'w') as file:
        file.write(file_header + '\n')
        for data in data_content:
            file.write(','.join([str(item) for item in data]) + '\n')

def add_product(products_data):
    """
    Add a new product
    """
    print_title("ADDING PRODUCT")
    try:
        product_id = duplicate_check("Enter your product id: ", products_data).strip()
        product_name = input("Enter product name: ").strip()
        product_count = int(input("Enter how many product: "))
        product_description = input("Enter description of product: ").strip()
        product_price = float(input("Enter product price (in MYR): "))
    except ValueError:
        print("Wrong Value Type")
    else:
        products_data.append([product_id, product_name, product_count, product_description, product_price])
        save_data("products.txt", products_data)
        print(f"Number of product added: {len(products_data)}")
        print("Product is successfully added")

def update_product(products_data):
    """
    Update product details
    """
    print_title("UPDATE PRODUCT")
    item_number = 0
    print("Product ID | Product Name | Qty | Description | Price (MYR)")

    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    product_id = input("\nEnter the product ID : ").strip().upper()
    for product in products_data:
        if product[0] == product_id:
            try:
                product[1] = input(f"Enter new Name (current: {product[1]}): ").strip()
                product[2] = int(input(f"Enter new Qty (current: {product[2]}): "))
                product[3] = input(f"Enter new Description (current: {product[3]}): ").strip()
                product[4] = float(input(f"Enter new price (current: {product[4]}): "))
            except ValueError:
                print("Wrong Value Type")
                return
            else:
                save_data("products.txt", products_data)
                print("Product updated successfully!")
                return
    print("Product not found")

def add_supplier(suppliers_data):
    """
    Add a new supplier
    """
    print_title("ADDING SUPPLIER")
    try:
        supplier_id = duplicate_check("Enter supplier ID: ", suppliers_data).strip()
        name = input("Enter supplier name: ").strip()
        contact = int(input("Enter supplier contact number: "))
    except ValueError:
        print("Wrong Value Type")
    else:
        suppliers_data.append([supplier_id, name, contact])
        save_data("suppliers.txt", suppliers_data)
        print("Suppliers successfully added!")

def place_order(products_data, orders_data):
    """
    Place an order from the products.txt
    Ordering a product will reduce the quantity from products.txt
    """
    print_title("ORDERING PRODUCT")
    item_number = 0
    order_id = len(orders_data)

    if not products_data:
        print("Sorry, we don't have any product right now")
        return

    print("Product Available currently: \n\n"
          "Product ID | Product Name | Qty | Description | Price (MYR)")
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

    order_product = input("\nSelect the product (ID): ").strip().upper()

    for product in products_data:
        if product[0] == order_product:
            order_id += 1
            try:
                order_customer = input("Input the client name: ").strip()
                order_quantity = int(input(f"How many products would you like to order (Available: {product[2]}): "))
            except ValueError:
                print("Wrong value type, please input number type")
                return
            else:
                if order_quantity >= int(product[2]):
                    print("\nSorry, insufficient product")
                    return
                orders_data.append([f"{order_id:04d}", product[1], order_quantity, order_customer])
                product[2] = int(product[2]) - order_quantity
                save_data("orders.txt", orders_data)
                save_data("products.txt", products_data)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("Details:\n"
                      f"ID = {order_id:04d} | Product = {product[1]} | Order = {order_quantity} | Client = {order_customer} \n\n"
                      "Orders added successfully!")
                return
    print("Product not found")

def view_inventory(products_data):
    """
    Print out the content of products.txt file with additional format
    """
    print_title("VIEW INVENTORY")
    item_number = 0
    print("Product ID | Qty | Price | Description | Price (MYR)")
    for product in products_data:
        item_number += 1
        print(f"{item_number}. {product[0]}, {product[1]}, {product[2]}, {product[3]}, {product[4]}")

def generate_reports(products_data, orders_data, suppliers_data):
    """
    Generate a report for low stock, product sales, and view suppliers
    """
    print_title("GENERATE REPORTS")

    def low_stock_report(products_info):
        print_title("LOW STOCK REPORT")
        item_number = 0
        for product in products_info:
            if int(product[2]) <= 10:
                item_number += 1
                print(f"{item_number}. {product[0]} stock is at {product[2]}")

    def product_sales_report(products_info, orders_info):
        print_title("PRODUCT SALES REPORT")
        item_number = 0
        for product in products_info:
            for order in orders_info:
                if order[1] == product[1]:
                    item_number += 1
                    revenue = int(order[2]) * float(product[4])
                    print(f"{item_number}. {product[1]}: {order[2]} unit{'s'[:int(order[2]) ^ 1]} sold for {revenue} MYR")

    def view_suppliers(suppliers_info):
        print_title("SUPPLIER LIST REPORT")
        item_number = 0
        print("Supplier ID | Name | Contact")
        for supplier in suppliers_info:
            item_number += 1
            print(f"{item_number}. {supplier[0]}, {supplier[1]}, {supplier[2]}")

    print("1. Low Stock\n"
          "2. Product Sales\n"
          "3. Supplier List")
    report_type = input("Pick the report you want: ").strip()
    match report_type:
        case "1": low_stock_report(products_data)
        case "2": product_sales_report(products_data, orders_data)
        case "3": view_suppliers(suppliers_data)
        case _: print("Invalid option, pick something within the range of 1-3")

def main():
    """
    Main menu option screen
    """
    while True:
        print_title("Main Menu")
        products_data = load_data('products.txt')
        suppliers_data = load_data('suppliers.txt')
        orders_data = load_data('orders.txt')

        print("1. Add a new product \n"
              "2. Update product details \n"
              "3. Add a new supplier \n"
              "4. Place an order \n"
              "5. View inventory \n"
              "6. Generate reports \n"
              "7. Exit \n")

        user_input = input("Enter Number: ").strip()
        match user_input:
            case "1": add_product(products_data)
            case "2": update_product(products_data)
            case "3": add_supplier(suppliers_data)
            case "4": place_order(products_data, orders_data)
            case "5": view_inventory(products_data)
            case "6": generate_reports(products_data, orders_data, suppliers_data)
            case "7": break
            case _: print("Invalid option, pick something within the range of 1-7")

        input("\nPress enter to continue... ")

if __name__ == "__main__":
    main()
