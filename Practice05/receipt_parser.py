"""
RECEIPT PARSER - Practical Exercise 2.2
Parsing receipt data from raw.txt using Regular Expressions

This script demonstrates 6 main tasks:
1. Extract all prices from the receipt
2. Find all product names
3. Calculate total amount
4. Extract date and time information
5. Find payment method
6. Create a structured output (JSON or formatted text)
"""

import re
import json
from datetime import datetime

class ReceiptParser:
    def __init__(self, filename):
        """Initialize parser with receipt file"""
        self.filename = filename
        self.content = self._read_file()
        print("📄 Receipt file loaded successfully!")
        
    def _read_file(self):
        """Read the receipt file content"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"❌ Error: File '{self.filename}' not found!")
            return ""
    
    # ============================================================
    # TASK 1: EXTRACT ALL PRICES FROM THE RECEIPT
    # ============================================================
    def task1_extract_all_prices(self):
        """
        TASK 1: Extract all prices from the receipt
        Finds all price values including unit prices and total prices
        """
        print("\n" + "="*60)
        print("📌 TASK 1: EXTRACT ALL PRICES FROM THE RECEIPT")
        print("="*60)
        
        # Pattern to find prices (numbers with optional spaces and comma as decimal)
        # Examples: 154,00 | 1 200,00 | 7 330,00
        price_pattern = r'\b\d+(?:\s*\d+)*,\d{2}\b'
        
        # Find all prices
        all_prices = re.findall(price_pattern, self.content)
        
        # Convert to float for better representation
        prices_float = []
        for price in all_prices:
            # Remove spaces and replace comma with dot
            clean_price = price.replace(' ', '').replace(',', '.')
            prices_float.append(float(clean_price))
        
        # Display results
        print(f"\n🔍 Found {len(all_prices)} prices in the receipt:")
        print("-" * 40)
        
        # Show prices with context (where they appear)
        lines = self.content.split('\n')
        price_context = []
        
        for i, line in enumerate(lines):
            if re.search(price_pattern, line):
                # Clean up the line for display
                clean_line = line.strip()
                if clean_line:  # Only show non-empty lines
                    price_context.append(clean_line)
        
        for i, context in enumerate(price_context[:10]):  # Show first 10
            print(f"   {i+1}. {context}")
        
        if len(price_context) > 10:
            print(f"   ... and {len(price_context) - 10} more")
        
        # Summary statistics
        print("\n📊 Price Statistics:")
        print(f"   • Total prices found: {len(prices_float)}")
        print(f"   • Minimum price: {min(prices_float):.2f}")
        print(f"   • Maximum price: {max(prices_float):.2f}")
        print(f"   • Average price: {sum(prices_float)/len(prices_float):.2f}")
        
        return {
            'raw_prices': all_prices,
            'float_prices': prices_float,
            'count': len(prices_float)
        }
    
    # ============================================================
    # TASK 2: FIND ALL PRODUCT NAMES
    # ============================================================
    def task2_find_all_product_names(self):
        """
        TASK 2: Find all product names from the receipt
        Extracts product names from numbered lines
        """
        print("\n" + "="*60)
        print("📌 TASK 2: FIND ALL PRODUCT NAMES")
        print("="*60)
        
        # Pattern to match product lines (starts with number and dot)
        # Example: "1. Натрия хлорид 0,9%, 200 мл, фл"
        product_line_pattern = r'^\s*(\d+)\.\s*(.+?)(?:\s+\d+(?:\s*\d+)*,\d{2})?$'
        
        product_names = []
        lines = self.content.split('\n')
        
        for line in lines:
            match = re.match(product_line_pattern, line.strip())
            if match:
                product_number = match.group(1)
                product_name = match.group(2).strip()
                
                # Clean up product name (remove extra spaces)
                product_name = re.sub(r'\s+', ' ', product_name)
                product_names.append({
                    'number': int(product_number),
                    'name': product_name
                })
        
        # Display results
        print(f"\n🔍 Found {len(product_names)} products:")
        print("-" * 60)
        
        for i, product in enumerate(product_names, 1):
            # Truncate long names for display
            display_name = product['name'][:50] + "..." if len(product['name']) > 50 else product['name']
            print(f"   {i:2d}. [{product['number']:2d}] {display_name}")
        
        # Show unique products (in case of duplicates)
        unique_names = set([p['name'] for p in product_names])
        if len(unique_names) < len(product_names):
            print(f"\n📊 Note: {len(product_names) - len(unique_names)} duplicate products found")
        
        return product_names
    
    # ============================================================
    # TASK 3: CALCULATE TOTAL AMOUNT
    # ============================================================
    def task3_calculate_total_amount(self):
        """
        TASK 3: Calculate total amount from the receipt
        Finds the TOTAL line and extracts the value
        """
        print("\n" + "="*60)
        print("📌 TASK 3: CALCULATE TOTAL AMOUNT")
        print("="*60)
        
        # Method 1: Find explicit TOTAL line
        total_patterns = [
            r'ИТОГО:\s*(\d+(?:\s*\d+)*,\d{2})',           # ИТОГО: 18 009,00
            r'ИТОГО:\s*(\d+[.,]\d+)',                     # Alternative format
            r'^ИТОГО.*?(\d+(?:\s*\d+)*,\d{2})',           # ИТОГО anywhere in line
        ]
        
        total_amount = None
        method_used = ""
        
        for pattern in total_patterns:
            match = re.search(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            if match:
                total_str = match.group(1)
                # Clean and convert to float
                total_str_clean = total_str.replace(' ', '').replace(',', '.')
                total_amount = float(total_str_clean)
                method_used = "Explicit ИТОГО line"
                break
        
        # Method 2: If no TOTAL line, sum all item prices
        if total_amount is None:
            print("   ⚠ No explicit TOTAL line found, calculating from items...")
            
            # Find all item total prices (lines with just a price after items)
            item_total_pattern = r'^Стоимость\s*$.*?^(\d+(?:\s*\d+)*,\d{2})\s*$'
            item_totals = re.findall(item_total_pattern, self.content, re.MULTILINE | re.DOTALL)
            
            if item_totals:
                total_amount = 0
                for price in item_totals:
                    price_clean = price.replace(' ', '').replace(',', '.')
                    total_amount += float(price_clean)
                method_used = "Sum of item totals"
        
        # Display results
        print(f"\n💰 TOTAL AMOUNT: {total_amount:,.2f} KZT")
        print(f"   Method used: {method_used}")
        
        # Verify with bank card payment if present
        bank_match = re.search(r'Банковская карта:\s*(\d+(?:\s*\d+)*,\d{2})', self.content)
        if bank_match:
            bank_amount = float(bank_match.group(1).replace(' ', '').replace(',', '.'))
            print(f"   💳 Bank card payment: {bank_amount:,.2f} KZT")
            
            if abs(total_amount - bank_amount) < 0.01:
                print("   ✅ Verified: Total matches bank card payment")
            else:
                print(f"   ⚠ Warning: Total ({total_amount}) differs from bank payment ({bank_amount})")
        
        return total_amount
    
    # ============================================================
    # TASK 4: EXTRACT DATE AND TIME INFORMATION
    # ============================================================
    def task4_extract_datetime(self):
        """
        TASK 4: Extract date and time information from the receipt
        Finds the timestamp when the receipt was issued
        """
        print("\n" + "="*60)
        print("📌 TASK 4: EXTRACT DATE AND TIME INFORMATION")
        print("="*60)
        
        # Pattern for date and time
        # Format: Время: 18.04.2019 11:13:58
        datetime_patterns = [
            r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})',  # Date and time separate
            r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})',    # Date and time together
            r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})'            # Any date+time combo
        ]
        
        date_info = {}
        
        for pattern in datetime_patterns:
            match = re.search(pattern, self.content)
            if match:
                if len(match.groups()) == 2:
                    date_str = match.group(1)
                    time_str = match.group(2)
                    datetime_str = f"{date_str} {time_str}"
                else:
                    datetime_str = match.group(1)
                    # Try to split date and time
                    date_parts = datetime_str.split()
                    if len(date_parts) == 2:
                        date_str, time_str = date_parts
                    else:
                        date_str = datetime_str
                        time_str = "Unknown"
                
                date_info['raw_datetime'] = datetime_str
                date_info['date'] = date_str
                date_info['time'] = time_str if 'time_str' in locals() else "Unknown"
                
                # Try to parse as datetime object
                try:
                    dt = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')
                    date_info['parsed'] = dt
                    date_info['day'] = dt.day
                    date_info['month'] = dt.month
                    date_info['year'] = dt.year
                    date_info['hour'] = dt.hour
                    date_info['minute'] = dt.minute
                    date_info['second'] = dt.second
                    date_info['weekday'] = dt.strftime('%A')
                except (ValueError, TypeError):
                    date_info['parsed'] = None
                
                break
        
        # Display results
        print("\n📅 Date Information:")
        if date_info:
            print(f"   • Raw date/time: {date_info.get('raw_datetime', 'Not found')}")
            print(f"   • Date: {date_info.get('date', 'N/A')}")
            print(f"   • Time: {date_info.get('time', 'N/A')}")
            
            if date_info.get('parsed'):
                print(f"   • Day of week: {date_info['weekday']}")
                print(f"   • Year: {date_info['year']}")
                print(f"   • Month: {date_info['month']:02d}")
                print(f"   • Day: {date_info['day']:02d}")
                print(f"   • Time: {date_info['hour']:02d}:{date_info['minute']:02d}:{date_info['second']:02d}")
        else:
            print("   ❌ No date/time information found")
        
        return date_info
    
    # ============================================================
    # TASK 5: FIND PAYMENT METHOD
    # ============================================================
    def task5_find_payment_method(self):
        """
        TASK 5: Find payment method used in the transaction
        Identifies whether payment was by card, cash, or other
        """
        print("\n" + "="*60)
        print("📌 TASK 5: FIND PAYMENT METHOD")
        print("="*60)
        
        payment_info = {
            'method': None,
            'amount': None,
            'details': {}
        }
        
        # Check for different payment methods
        payment_patterns = {
            'bank_card': [
                r'Банковская карта:\s*(\d+(?:\s*\d+)*,\d{2})',
                r'Карта:\s*(\d+(?:\s*\d+)*,\d{2})',
                r'Card:\s*(\d+(?:\s*\d+)*,\d{2})'
            ],
            'cash': [
                r'Наличные:\s*(\d+(?:\s*\d+)*,\d{2})',
                r'Cash:\s*(\d+(?:\s*\d+)*,\d{2})'
            ],
            'qr_code': [
                r'QR.*?(\d+(?:\s*\d+)*,\d{2})',
                r'Kaspi.*?(\d+(?:\s*\d+)*,\d{2})'
            ]
        }
        
        for method, patterns in payment_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, self.content, re.IGNORECASE)
                if match:
                    payment_info['method'] = method.replace('_', ' ').title()
                    amount_str = match.group(1)
                    amount_clean = amount_str.replace(' ', '').replace(',', '.')
                    payment_info['amount'] = float(amount_clean)
                    
                    # Get the full line for context
                    line_pattern = f"^.*{pattern.replace('(', '\\(').replace(')', '\\)')}.*$"
                    line_match = re.search(line_pattern, self.content, re.IGNORECASE | re.MULTILINE)
                    if line_match:
                        payment_info['details']['full_line'] = line_match.group(0).strip()
                    
                    break
            if payment_info['method']:
                break
        
        # If no explicit payment method found, check for bank card indicator
        if not payment_info['method']:
            if re.search(r'Банковская карта', self.content, re.IGNORECASE):
                payment_info['method'] = 'Bank Card'
                # Try to find amount without pattern
                amount_match = re.search(r'Банковская карта:\s*(\d+(?:\s*\d+)*,\d{2})', self.content)
                if amount_match:
                    amount_str = amount_match.group(1)
                    payment_info['amount'] = float(amount_str.replace(' ', '').replace(',', '.'))
        
        # Display results
        print("\n💳 Payment Details:")
        if payment_info['method']:
            print(f"   • Method: {payment_info['method']}")
            if payment_info['amount']:
                print(f"   • Amount: {payment_info['amount']:,.2f} KZT")
            if 'full_line' in payment_info['details']:
                print(f"   • Raw: {payment_info['details']['full_line']}")
            
            # Check if payment matches total
            total = self.task3_calculate_total_amount()
            if payment_info['amount'] and abs(payment_info['amount'] - total) < 0.01:
                print("   ✅ Verified: Payment amount matches total")
        else:
            print("   ❌ No payment method found")
            print("   ℹ Available payment indicators:")
            # Show lines that might contain payment info
            for line in self.content.split('\n'):
                if re.search(r'(карта|cash|payment|наличные|kaspi)', line, re.IGNORECASE):
                    print(f"      • {line.strip()}")
        
        return payment_info
    
    # ============================================================
    # TASK 6: CREATE STRUCTURED OUTPUT (JSON or formatted text)
    # ============================================================
    def task6_create_structured_output(self, output_format='both'):
        """
        TASK 6: Create structured output (JSON or formatted text)
        Compiles all extracted data into a structured format
        """
        print("\n" + "="*60)
        print("📌 TASK 6: CREATE STRUCTURED OUTPUT")
        print("="*60)
        
        # Gather all data from previous tasks
        structured_data = {
            'receipt_info': {
                'filename': self.filename,
                'parser_version': '1.0',
                'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'pharmacy_details': {},
            'products': [],
            'financial': {},
            'datetime': {},
            'payment': {},
            'fiscal_data': {}
        }
        
        # Extract pharmacy information
        pharmacy_patterns = {
            'branch': r'Филиал\s+(.+)',
            'bin': r'БИН\s+(\d+)',
            'vat_series': r'НДС\s+Серия\s+(\d+)',
            'cash_register': r'Касса\s+(\d+-\d+)',
            'shift': r'Смена\s+(\d+)',
            'receipt_number': r'Порядковый номер чека №(\d+)',
            'check_number': r'Чек\s*№(\d+)',
            'cashier': r'Кассир\s+(.+)'
        }
        
        for key, pattern in pharmacy_patterns.items():
            match = re.search(pattern, self.content)
            if match:
                structured_data['pharmacy_details'][key] = match.group(1).strip()
        
        # Extract products
        product_pattern = r'^\s*(\d+)\.\s*(.+?)(?:\s+\d+(?:\s*\d+)*,\d{2})?$'
        lines = self.content.split('\n')
        current_product = None
        
        for i, line in enumerate(lines):
            # Check for product line
            match = re.match(product_pattern, line.strip())
            if match:
                if current_product:
                    structured_data['products'].append(current_product)
                
                current_product = {
                    'number': int(match.group(1)),
                    'name': match.group(2).strip(),
                    'quantity': None,
                    'unit_price': None,
                    'total_price': None
                }
                
                # Look ahead for quantity and price
                if i + 1 < len(lines):
                    qty_line = lines[i + 1].strip()
                    qty_match = re.match(r'^(\d+),\d{3}\s*x\s*(\d+(?:\s*\d+)*,\d{2})$', qty_line)
                    if qty_match:
                        current_product['quantity'] = float(qty_match.group(1))
                        unit_price_str = qty_match.group(2).replace(' ', '').replace(',', '.')
                        current_product['unit_price'] = float(unit_price_str)
                        
                        # Look for total price
                        if i + 2 < len(lines):
                            total_line = lines[i + 2].strip()
                            total_match = re.match(r'^(\d+(?:\s*\d+)*,\d{2})$', total_line)
                            if total_match:
                                total_str = total_match.group(1).replace(' ', '').replace(',', '.')
                                current_product['total_price'] = float(total_str)
        
        # Add last product
        if current_product:
            structured_data['products'].append(current_product)
        
        # Financial data
        structured_data['financial']['total'] = self.task3_calculate_total_amount()
        
        # Extract VAT if present
        vat_match = re.search(r'в\.т\.ч\.\s*НДС\s*\d+%:\s*(\d+(?:\s*\d+)*,\d{2})', self.content)
        if vat_match:
            vat_str = vat_match.group(1).replace(' ', '').replace(',', '.')
            structured_data['financial']['vat'] = float(vat_str)
        
        # DateTime data
        datetime_info = self.task4_extract_datetime()
        structured_data['datetime'] = datetime_info
        
        # Payment data
        payment_info = self.task5_find_payment_method()
        structured_data['payment'] = payment_info
        
        # Fiscal data
        fiscal_patterns = {
            'fiscal_sign': r'Фискальный признак:\s*(\d+)',
            'fiscal_receipt': r'ФИСКАЛЬНЫЙ ЧЕК',
            'fp': r'ФП',
            'ofd_code': r'ИНК ОФД:\s*(\d+)',
            'kkm_code': r'Код ККМ КГД \(РНМ\):\s*([\d\s]+)',
            'znm': r'ЗНМ:\s*(\w+)'
        }
        
        for key, pattern in fiscal_patterns.items():
            match = re.search(pattern, self.content)
            if match:
                if match.groups():
                    structured_data['fiscal_data'][key] = match.group(1).strip()
                else:
                    structured_data['fiscal_data'][key] = True
        
        # Address
        address_match = re.search(r'г\.\s*([^,]+(?:,[^,]+)*)', self.content)
        if address_match:
            structured_data['pharmacy_details']['address'] = address_match.group(1).strip()
        
        # Create outputs based on requested format
        if output_format in ['json', 'both']:
            # Save JSON file
            json_filename = 'receipt_parsed.json'
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 JSON output saved to: {json_filename}")
        
        if output_format in ['text', 'both']:
            # Create formatted text output
            self._print_formatted_output(structured_data)
        
        return structured_data
    
    # ============================================================
    # Helper method for formatted text output
    # ============================================================
    def _print_formatted_output(self, data):
        """Print formatted text output of receipt data"""
        print("\n" + "="*70)
        print("📋 FORMATTED RECEIPT OUTPUT")
        print("="*70)
        
        # Header
        print("\n🏥 PHARMACY RECEIPT")
        print("-" * 70)
        
        # Pharmacy info
        if data['pharmacy_details']:
            print(f"   Branch: {data['pharmacy_details'].get('branch', 'N/A')}")
            print(f"   BIN: {data['pharmacy_details'].get('bin', 'N/A')}")
            print(f"   Address: {data['pharmacy_details'].get('address', 'N/A')}")
            print(f"   Cash Register: {data['pharmacy_details'].get('cash_register', 'N/A')}")
            print(f"   Cashier: {data['pharmacy_details'].get('cashier', 'N/A')}")
            print(f"   Receipt #: {data['pharmacy_details'].get('receipt_number', 'N/A')}")
        
        # Date and Time
        if data['datetime']:
            print(f"\n📅 Date/Time: {data['datetime'].get('raw_datetime', 'N/A')}")
        
        # Products
        print(f"\n🛒 PURCHASED ITEMS ({len(data['products'])} items)")
        print("-" * 70)
        
        total_sum = 0
        for i, product in enumerate(data['products'], 1):
            name_display = product['name'][:40] + "..." if len(product['name']) > 40 else product['name']
            print(f"   {i:2d}. {name_display:42s}", end="")
            
            if product.get('quantity') and product.get('unit_price'):
                print(f"  {product['quantity']} x {product['unit_price']:8.2f}", end="")
                if product.get('total_price'):
                    print(f" = {product['total_price']:8.2f}")
                    total_sum += product['total_price']
                else:
                    print()
            else:
                print()
        
        # Financial summary
        print("-" * 70)
        print(f"\n💰 FINANCIAL SUMMARY")
        print(f"   Subtotal: {total_sum:,.2f} KZT")
        print(f"   TOTAL: {data['financial'].get('total', 0):,.2f} KZT")
        
        if 'vat' in data['financial']:
            print(f"   VAT (12%): {data['financial']['vat']:,.2f} KZT")
        
        # Payment
        if data['payment'].get('method'):
            print(f"\n💳 PAYMENT: {data['payment']['method']}")
            if data['payment'].get('amount'):
                print(f"   Amount paid: {data['payment']['amount']:,.2f} KZT")
        
        # Fiscal data
        if data['fiscal_data']:
            print(f"\n🔐 FISCAL INFORMATION")
            for key, value in data['fiscal_data'].items():
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        print("\n" + "="*70)
        print("✅ END OF RECEIPT")
        print("="*70)


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    """Main function to run all tasks"""
    print("\n" + "="*70)
    print("🏁 RECEIPT PARSING WITH REGULAR EXPRESSIONS")
    print("="*70)
    print("Processing file: raw.txt")
    print("="*70)
    
    # Create parser instance
    parser = ReceiptParser('raw.txt')
    
    if not parser.content:
        print("❌ Cannot proceed without receipt content!")
        return
    
    # Run all tasks sequentially
    print("\n" + "🚀"*35)
    print("🚀 EXECUTING ALL 6 TASKS")
    print("🚀"*35)
    
    # Task 1
    task1_result = parser.task1_extract_all_prices()
    
    # Task 2
    task2_result = parser.task2_find_all_product_names()
    
    # Task 3
    task3_result = parser.task3_calculate_total_amount()
    
    # Task 4
    task4_result = parser.task4_extract_datetime()
    
    # Task 5
    task5_result = parser.task5_find_payment_method()
    
    # Task 6 - with both JSON and text output
    task6_result = parser.task6_create_structured_output(output_format='both')
    
    # Summary
    print("\n" + "="*70)
    print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
    print("="*70)
    print("\n📊 Summary:")
    print(f"   • Task 1: Found {len(task1_result['raw_prices'])} prices")
    print(f"   • Task 2: Found {len(task2_result)} products")
    print(f"   • Task 3: Total amount = {task3_result:,.2f} KZT")
    print(f"   • Task 4: Date = {task4_result.get('date', 'N/A')}")
    print(f"   • Task 5: Payment method = {task5_result.get('method', 'N/A')}")
    print(f"   • Task 6: JSON saved to 'receipt_parsed.json'")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()