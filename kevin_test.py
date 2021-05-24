# Import libraries
# from synth import FakeCategoricalSeries
from h2o_wave import main, app, Q, ui, pack, data
import random
import pandas as pd
from datetime import datetime, timedelta
import scipy.stats as stats
import numpy as np
import uuid
import os
import matplotlib.pyplot as plt

print('import success')

##################################################################
##################################################################

item_csv = "item.csv"
manufacturer_csv = "manufacturer.csv"
supplier_csv = "supplier.csv"

p_id = 0
m_id = 0
s_id = 0

# !!!
# save tabs 
tabs = [
    ui.tab(name='#manufacturers', label='Manufacturers'),
    ui.tab(name='#suppliers', label='Suppliers'),
    ui.tab(name='#products', label='Products'), 
]

## Define fixed variables
uom = ['Strips', 'Ampoules', 'Boxes', 'Litres']
consumption = ['daily', 'weekly', 'monthly']

############################## DEFINE CLASS

## Product class
class Products:
    def __init__(self, 
        product: str, 
        manufacturer: str, 
        supplier: str
        # selling_price: float, 
        # uom: str, 
        # product_type: str,
        # product_subtype: str,
        # module: str,
        # brand: str,
        # branded_yn: str,
        # generic_yn: str,
        # substitute: str  
      ):
    
        global p_id
        p_id += 1
        self.id = f'I{p_id}'
        self.product = product
        self.manufacturer = manufacturer
        self.supplier = supplier
        # self.selling_price = selling_price
        # self.uom = uom
        # self.product_type = product_type
        # self.product_subtype = product_subtype
        # self.module = module
        # self.brand = brand
        # self.branded_yn = branded_yn
        # self.generic_yn = generic_yn
        # self.substitute = substitute

# Manufacturer class
class Manufacturers:
    def __init__(self, 
        manufacturer: str, 
        product: str, 
        # uom:str, 
      ):

        global m_id
        m_id += 1
        self.id = f'I{m_id}'
        self.manufacturer = manufacturer
        self.product = product
        # self.uom = uom

#Supplier class
class Suppliers:
    def __init__(self, 
        supplier: str,
        manufacturer: str, 
        product: str,
        # selling_price: float, 
        # uom: str, 
        # lead_time: str, 
        # delivery_time: str, 
        # country: str
        ):

        global s_id
        s_id += 1
        self.id = f'I{s_id}'
        self.supplier = supplier
        self.manufacturer = manufacturer
        self.product = product
        # self.selling_price = selling_price
        # self.uom = uom
        # self.lead_time = lead_time
        # self.delivery_time = delivery_time
        # self.country = country

# Define variables
products = []
manufacturers = []
suppliers = []

l_products = []
l_manufacturers = []
l_suppliers = []

############################## GET DATA

# !!! df_pr use the table name
try:
    df_pr = pd.read_csv("products.csv")
    # l_products = df_pr[['Item Name', 'Manufacturer Name', 'Supplier Name', 
    #               'Item Price', 'Unit of Measurement', 'Item Type', 'Item Subtype', 
    #               'Module', 'Brand', 'Branded YN', 'Generic YN', 'Substitute']].values.tolist()
    l_products = df_pr.values.tolist()
    
    products = [Products(product[0], product[1], product[2]) for product in l_products]
    
except:
  print("products.csv not found")

try:
    df_ma = pd.read_csv("manufacturers.csv")
    l_manufacturers = df_ma.values.tolist()
    print(l_manufacturers)
    manufacturers = [Manufacturers(manufacturer[0], manufacturer[1]) for manufacturer in l_manufacturers]
except:
    print('manufacturers.csv not found')

try:
    df_su = pd.read_csv("suppliers.csv")
    # l_suppliers = df_su[['Supplier Name','Manufacturer Name', 'Item Name', 'Item UoM']].values.tolist()
    l_suppliers = df_su.values.tolist()
    print(l_suppliers)
    suppliers = [Suppliers(supplier[0], supplier[1], supplier[2]) for supplier in l_suppliers]
except:
    print('suppliers.csv not found')

############################## DEFINE COLUMNS FOR EACH SECTION

# !!!
# Create columns for our product table.
column_product_table = [
    ui.table_column(name='product', label='Product', sortable=True, searchable=True),
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True),
    ui.table_column(name='supplier', label='Supplier', sortable=True, searchable=True)
    # ui.table_column(name='selling_price', label='Selling Price', sortable=True, data_type='number'),
    # ui.table_column(name='uom', label='Unit of Measurement')
    # ui.table_column(name='product_type', label='Type', sortable=True, searchable=True, ),
    # ui.table_column(name='product_subtype', label='Subtype', sortable=True, searchable=True, ),
    # ui.table_column(name='module', label='module', sortable=True, searchable=True, ),
    # ui.table_column(name='brand', label='Brand', sortable=True, searchable=True, ),
    # ui.table_column(name='branded_yn', label='Branded YN', sortable=True, searchable=True, ),
    # ui.table_column(name='generic_yn', label='Generic YN', sortable=True, searchable=True, ),
    # ui.table_column(name='substitute', label='Substitute', sortable=True, searchable=True, ),
]

# !!!
# Create columns for our manufacturer table.
column_manufacturer_table = [
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='product', label='Product', sortable=True, searchable=True, max_width='300'),
    # ui.table_column(name='Item UoM', label='Unit of Measurement')
]

# !!!
# Create columns for our supplier table
column_supplier_table = [
    ui.table_column(name='supplier', label='Supplier', sortable=True, searchable=True),
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True),
    ui.table_column(name='product', label='Product', sortable=True, searchable=True),
    # ui.table_column(name='Item UoM', label='Unit of Measurement')
]

##################################################################
##################################################################

current_tab = '#manufacturers' # set manufacturer section as default tab
@app('/test_catalogue_manager')
async def serve(q: Q):
  global current_tab

  q.page['header'] = ui.header_card(
    box='1 1 -1 1',
    title='Catalogue Manager',
    subtitle='',
    icon='ExploreData'
  )

  print('Current tab: ', current_tab, q.args)
  if q.args['#']:
    q.args.menu = '#'+q.args['#']

  if q.args.menu:
    current_tab = q.args.menu

  if q.args.goto_manufacturer:
    current_tab = '#manufacturers'
  elif q.args.goto_supplier:
    current_tab = '#suppliers'

  print('q args: ' + str(q.args))
  print('q args menu: ' + str(q.args.menu))

  if current_tab == '#products':
    await showProducts(q)
  elif current_tab == '#manufacturers':
    await showManufacturers(q)
  elif current_tab == '#suppliers':
    await showSuppliers(q)
  else:
    await showManufacturers(q)
  await q.page.save()

startDate = None
endDate = None
demo_product = None

# !!! manufacturer -> item -> supplier -> 
# handle Supplier Table
async def showSuppliers(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
  print('items in supplier: ' + str(items))

  ## if user clicks 'Add Supplier'
  if q.args.show_inputs:
    ## need to get manufacturer data first (later used for the dropdown when addiing new supplier)
    df_m = pd.DataFrame(l_manufacturers, columns=['manufacturer', 'product'])

    ## if there is no Manufacter data, then the user should add manufacturer data first
    if len(df_m) == 0:
      items.extend([ui.message_bar(type='info', text='Try adding manufacturer first'),
        ui.button(name='goto_manufacturer', label='Close', primary=True)
        ])

    ## there's a manufacturer data, then go here
    else:
      items.extend([ui.text_xl(content='Add Supplier'),
        ui.textbox(name='supplier', label='Supplier'),
        ui.dropdown(name='manufacturer', label='Manufacturer', choices=[ ## dropdown existing manufacturers
            ui.choice(name=x, label=x) for x in df_m['manufacturer'].unique()
        ]),
        ui.dropdown(name='product', label='Product', choices=[ ## dropdown existing items
            ui.choice(name=x, label=x) for x in df_m['product'].unique()
        ]), ## product should based on the what manufacturer have
        # ui.dropdown(name='uom', label='Unit of Measurement', choices=[ ## dropdown unit of measurement based on UOM variable above
        #     ui.choice(name=x, label=x) for x in uom
        # ]),
        # ui.textbox(name='selling_price', label='Price'),
        # ui.textbox(name='lead_time', label='Lead Time(days)'),
        # ui.textbox(name='delivery_time', label='Delivery Time(days)'),
        ui.button(name='show_tables', label='Submit', primary=True) ## submit button
        ])
  
  ## user hasn't clicked 'Add suppliers' button
  else:     
    ## user have click has clicked 'Submit' button after adding supplier
    if q.args.show_tables:
      l_suppliers.append([q.args.supplier, q.args.manufacturer, q.args.product]) ## !!!
      s = Suppliers(q.args.supplier, q.args.manufacturer, q.args.product)
      suppliers.append(s)
      items.append(ui.message_bar(type='success', text='You have successfully added a supplier'))

    ## default view (if there's suppliers data)
    if len(suppliers) > 0:
      items.append(
        ui.table(
          name='suppliers',
          columns=column_supplier_table,
          rows=[ui.table_row(
              name=supplier.id,
              cells=[supplier.supplier, supplier.manufacturer, supplier.product]
              ) for supplier in suppliers],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))

    ## default view (if there's a supplier data)
    else:
      items.append(ui.text_l(content='No Supplier found'))

    # items.append(ui.button(name='show_inputs', label='Add Supplier', primary=True))

    items.append(ui.buttons([
      ui.button(name='show_inputs', label='Add Supplier', primary=True),
      ui.button(name='delete_button', label='Delete Supplier'),
      ui.button(name='edit_button', label='Edit Supplier'),
    ]))

  q.page['example'] = ui.form_card(box='1 2 -1 -1', items=items)
  await q.page.save()

# !!!
# handle Manufacturer Table
async def showManufacturers(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]

  print('---------------------------')
  print('== MANUFACTURER TAB == ')

  ## when user is adding new manufacturer
  if q.args.show_inputs: 
    items.extend([ui.text_xl(content='Add Manufacturer'),
        ui.textbox(name='manufacturer', label='Manufacturer'),
        ui.textbox(name='product', label='Product'),
        # ui.dropdown(name='uom', label='Unit of Measurement', choices=[
        #     ui.choice(name=x, label=x) for x in uom
        # ]),
        ui.button(name='show_tables', label='Submit', primary=True)])

  # ## when user is editing existing manufacturer
  # elif q.args.edit_button:
  #   items.extend([ui.text_xl(content='Edit Manufacturer'),
  #   ui.textbox(name='manufacturer', label='Manufacturer'),
  #   # ui.textbox(name='product', label='Product'),
  #   # ui.dropdown(name='uom', label='Unit of Measurement', choices=[
  #   #     ui.choice(name=x, label=x) for x in uom
  #   # ]),
  #   ui.button(name='show_tables', label='Submit', primary=True)])

  ## default goes here
  else: 

    ## user have click has clicked 'Submit' button after adding supplier
    if q.args.show_tables: 
      l_manufacturers.append([q.args.manufacturer, q.args.product])
      m = Manufacturers(q.args.manufacturer, q.args.product)
      manufacturers.append(m)

      items.append(ui.message_bar(type='success', text='You have successfully added a product'))

      ## GET ALL MANUFACTURERS DATA

    ## default view (if there's a manufacturer data)
    if len(manufacturers) > 0:
      items.append( 
        ui.table(
          name='manufacturers',
          columns=column_manufacturer_table,
          rows=[ui.table_row(
              name=manufacturer.id,
              cells=[manufacturer.manufacturer, manufacturer.product]
              ) for manufacturer in manufacturers],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))

    ## GET ALL MANUFACTURERS DATA

    ## default view (if there's no manufacturer data)
    else:
      items.append(ui.text_l(content='No Manufacturer found'))

    # items.append(ui.button(name='show_inputs', label='Add Manufacturer', primary=True))
    items.append(ui.buttons([
      ui.button(name='show_inputs', label='Add Manufacturer', primary=True),
      ui.button(name='delete_button', label='Delete Manufacturer'),
      ui.button(name='edit_button', label='Edit Manufacturer'),
    ]))

  q.page['example'] = ui.form_card(box='1 2 -1 -1', items=items)
  await q.page.save()

filter_product = None
filter_manufacturer = None
filter_supplier = None
unit_measure = None
selling_price = None
qty = None

# !!!
# handle Product Table  
async def showProducts(q: Q):
  global filter_product
  global filter_manufacturer 
  global filter_supplier 
  global unit_measure
  global gqty

  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]

  print('---------------------------')
  print('== PRODUCT TAB == ')
  print('q.args.show_tables: ' + str(q.args.show_tables) + ', q.args.show_inputs: ' + str(q.args.show_inputs))
  
  ## the user have clicked 'Add' button but haven't clicked 'Submit' button yet
  if (q.args.show_tables==None or q.args.show_tables==False) and (q.args.show_inputs or q.args.product or q.args.manufacturer or q.args.supplier or q.args.qty):

    ## need to get manufacturer data first (later used for the dropdown when adding new supplier)
    df_m = pd.DataFrame(l_manufacturers, columns=['manufacturer', 'product'])
    df_s = pd.DataFrame(l_suppliers, columns=['supplier', 'manufacturer', 'product'])
    
    ## if there is no manufacturer data
    if len(df_m) == 0: 
      items.extend([ui.message_bar(type='info', text='Try adding manufacturer first'),
        ui.button(name='goto_manufacturer', label='Close', primary=True)
        ])

    ## if there is no supplier data
    elif len(df_s) == 0:
      items.extend([ui.message_bar(type='info', text='Try adding supplier first'),
        ui.button(name='goto_supplier', label='Close', primary=True) 
        ])
      
    ## if there is data on manufacturer and supplier, when the user click 'Add Product' button
    else: 
        items.append(ui.text_xl(content='Add Product'))
        print('q.args.product: ' + str(q.args.product) + ', q.args.manufacturer: ' + str(q.args.manufacturer) + ', q.args.supplier: ' + str(q.args.supplier))
        
        if q.args.product and (filter_product==None or q.args.product!=filter_product):
          filter_product = q.args.product
          filter_manufacturer = None 
          filter_supplier = None
          unit_measure = None
          # selling_price = None
          gqty = None
        elif q.args.manufacturer and (filter_manufacturer==None or q.args.manufacturer!=filter_manufacturer):
          filter_manufacturer = q.args.manufacturer
          filter_supplier = None
          unit_measure = None
          # selling_price = None
          gqty = None
        elif q.args.supplier and (filter_supplier==None or q.args.supplier!=filter_supplier):
          filter_supplier = q.args.supplier
          unit_measure = None
          # selling_price = None
          gqty = None
        if q.args.qty:
          gqty = q.args.qty

        print(filter_product, filter_manufacturer, filter_supplier)

        ## PRODUCT
        if filter_product!=None:
          items.append(ui.dropdown(name='product', label='Product', choices=[
                ui.choice(name=x, label=x) for x in df_m['product'].unique()
            ], trigger = True, value=filter_product))
          tmp_m = df_m[df_m['product']==q.args.product]['manufacturer'].unique()     

        else:
          items.append(ui.dropdown(name='product', label='Product', choices=[
                  ui.choice(name=x, label=x) for x in df_m['product'].unique()
              ], trigger = True))
          tmp_m = df_m['manufacturer'].unique()

        ## MANUFACTURER
        if filter_manufacturer!=None:
          items.append(ui.dropdown(name='manufacturer', label='Manufacturer', choices=[
              ui.choice(name=x, label=x) for x in tmp_m
          ], trigger = True, value = filter_manufacturer))
          tmp_s = df_s[(df_s['product']==filter_product)&(df_s['manufacturer']==filter_manufacturer)]['supplier'].unique()    
        
        else:
          items.append(ui.dropdown(name='manufacturer', label='Manufacturer', choices=[
              ui.choice(name=x, label=x) for x in tmp_m
          ], trigger = True))
          tmp_s = df_s['supplier'].unique()

        ## SUPPLIER
        if filter_supplier!=None:
          items.append(ui.dropdown(name='supplier', label='Supplier', choices=[
              ui.choice(name=x, label=x) for x in tmp_s
          ], trigger = True, value = filter_supplier))
          # selling_price = df_s[(df_s['product']==filter_product)&(df_s['manufacturer']==filter_manufacturer)
          #                   &(df_s['supplier']==filter_supplier)]['selling_price'].values[0]
          # unit_measure = df_s[(df_s['product']==filter_product)&(df_s['manufacturer']==filter_manufacturer)
          #                   &(df_s['supplier']==filter_supplier)]['uom'].values[0]
        
        else:
          items.append(ui.dropdown(name='supplier', label='Supplier', choices=[
              ui.choice(name=x, label=x) for x in tmp_s
          ], trigger = True))
          # selling_price = None

        # items.append(ui.date_picker(name='purchase_date', label='Purchase Date'))
        # items.append(ui.textbox(name='qty', label='Qty'))

        # ## SELLING PRICE
        # if selling_price!=None:
        #   items.append(ui.textbox(name='selling_price', label='Selling Price', value = str(selling_price)))
        # else:
        #   items.append(ui.textbox(name='selling_price', label='Selling Price'))

        # ## UOM
        # if unit_measure!=None:
        #   items.append(ui.textbox(name='uom', label='Unit of Measurement', value = unit_measure, readonly = True))
        # else:
        #   items.append(ui.dropdown(name='uom', label='Unit of Measurement', choices=[
        #       ui.choice(name=x, label=x) for x in uom
        #   ]))

        # items.extend([
        #   # ui.date_picker(name='mfg_date', label='Mfg Date'),
        #   # ui.date_picker(name='exp_date', label='Exp Date'),
        #   ui.textbox(name='selling_price', label='Selling Price'),
        #   # ui.textbox(name='operational_cost', label='Operational Cost'),
        #   # ui.textbox(name='lvl', label='Order Point by level(%)'),
        #   # ui.textbox(name='schedule', label='Order Point Schedule (days)'),
        #   # ui.textbox(name='schedule_qty', label='Scheduled Qty'),
        #   # ui.textbox(name='rate', label='Avg. Consumption'),
        #   # ui.dropdown(name='freq', label='Consumption Frequency', choices=[
        #   #     ui.choice(name=x, label=x, value='daily', readonly=True) for x in consumption
        #   # ]), 
        #   ui.button(name='show_tables', label='Submit', primary=True)])

        items.extend([
          # ui.textbox(name='selling_price', label='Selling Price'),
          ui.button(name='show_tables', label='Submit', primary=True)])

  else:  ## first iteration goes here
    filter_product = None    
    filter_manufacturer = None 
    filter_supplier = None
    unit_measure = None
    selling_price = None
    gqty = None

    ## if q.args.show_tables == True
    if q.args.show_tables:
      # l_products.append([q.args.product, q.args.manufacturer, q.args.supplier, q.args.purchase_date, q.args.qty,
      #             q.args.uom, q.args.selling_price, q.args.mfg_date, q.args.exp_date, q.args.selling_price, 
      #             q.args.operational_cost, q.args.lvl, q.args.schedule, q.args.schedule_qty, q.args.rate])
      # p = Products(q.args.product, q.args.manufacturer, q.args.supplier, q.args.purchase_date, q.args.qty,
      #             q.args.uom, q.args.selling_price, q.args.mfg_date, q.args.exp_date, q.args.selling_price, 
      #             q.args.operational_cost, q.args.lvl, q.args.schedule, q.args.schedule_qty, q.args.rate)
                  
      # l_products.append([q.args.product, q.args.manufacturer, q.args.supplier, 
      #             q.args.uom])
      l_products.append([q.args.product, q.args.manufacturer, q.args.supplier])
      # p = Products(q.args.product, q.args.manufacturer, q.args.supplier,
      #             q.args.uom)
      p = Products(q.args.product, q.args.manufacturer, q.args.supplier)
      products.append(p)
      items.append(ui.message_bar(type='success', text='You have successfully added a product'))

    ## if there is a product data
    if len(products) > 0: 
      items.append(
        ui.table(
          name='products',
          columns=column_product_table,
          rows=[ui.table_row(
              name=product.id,
              # cells=[product.product, product.manufacturer, product.supplier, product.selling_price,
              #     product.uom]
              cells=[product.product, product.manufacturer, product.supplier]
              ) for product in products],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))
    else: ## if there is no product data
      items.append(ui.text_l(content='No Product found'))

    # items.append(ui.button(name='show_inputs', label='Add Product', primary=True))

    items.append(ui.buttons([
      ui.button(name='show_inputs', label='Add Product', primary=True),
      ui.button(name='delete_button', label='Delete Product'),
      ui.button(name='edit_button', label='Edit Product'),
    ]))

  q.page['example'] = ui.form_card(box='1 2 -1 -1', items=items)
  await q.page.save()
