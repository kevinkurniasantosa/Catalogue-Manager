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

uom = ['Strips', 'Ampoules', 'Boxes', 'Litres']
consumption = ['daily', 'weekly', 'monthly']


# Item Name: 
# Manufacturer
# Supplier
# Item Price
# Item UoM
# Item Type
# Item Subtype
# Module Name
# Brand Name
# Branded YN
# Generic YN
# Substitute

############################## DEFINE CLASS

## Product class
class Products:
    def __init__(self, 
        product: str, 
        manufacturer: str, 
        supplier: str, 
        purchase_date: str, 
        qty: float, 
        uom: str, 
        cost_price: float, 
        mfg_date: str, 
        exp_date: str, 
        selling_price: float, 
        operational_cost: float, 
        lvl: float, 
        schedule: int, 
        schedule_qty: float, 
        rate: float):

        global p_id
        p_id += 1
        self.id = f'I{p_id}'
        self.product = product
        self.manufacturer = manufacturer
        self.supplier = supplier
        self.purchase_date = purchase_date
        self.qty = qty
        self.uom = uom
        self.cost_price = cost_price
        self.mfg_date = mfg_date
        self.exp_date = exp_date
        self.selling_price = selling_price
        self.operational_cost = operational_cost
        self.lvl = lvl
        self.schedule = schedule
        self.schedule_qty = schedule_qty
        self.rate = rate

# Manufacturer Name
# Item Name
# Item Price
# Item UoM
# Shelf Life (days)

string
string
float
string
string/integer(?)

# Manufacturer class
class Manufacturers:
    def __init__(self, 
        manufacturer: str, 
        product: str, 
        product: str, 
        uom:str, 
        life:str):

        global m_id
        m_id += 1
        self.id = f'I{m_id}'
        self.product = product
        self.manufacturer = manufacturer
        self.country = country
        self.uom = uom
        self.life = life

# Supplier class
class Suppliers:
    def __init__(self, 
        product: str, 
        manufacturer: str, 
        supplier: str, 
        uom: str, 
        price: float, 
        lead_time: int, 
        delivery_time: int, 
        country: str):

        global s_id
        s_id += 1
        self.id = f'I{s_id}'
        self.product = product
        self.manufacturer = manufacturer
        self.supplier = supplier
        self.uom = uom
        self.price = price
        self.lead_time = lead_time
        self.delivery_time = delivery_time
        self.country = country

# Define variables
products = []
manufacturers = []
suppliers = []

l_products = []
l_manufacturers = []
l_suppliers = []

############################## GET DATA

try:
  df_pr = pd.read_csv("products.csv")
  l_products = df_pr[['Product', 'Manufacturer', 'Supplier', 
                'Purchase Date', 'Qty', 'Unit of Measure', 
                'Cost Price', 'Manufacturing Date', 'Expiry Date', 
                'Selling Price', 'Operational Cost', 'Stockout level(%)', 
                'Schedule(days)', 'Schedule Qty', 'Consumption']].values.tolist()
  products = [Products(product[0], product[1], product[2],
              product[3], product[4], product[5],
              product[6], product[7], product[8],
              product[9], product[10], product[11],
              product[12], product[13], product[14]) for product in l_products]
except:
  print("products.csv not found")

try:
  df_ma = pd.read_csv("manufacturers.csv")
  l_manufacturers = df_ma.values.tolist()
  manufacturers = [Manufacturers(manufacturer[0],manufacturer[1],manufacturer[2],manufacturer[3],manufacturer[4]) for manufacturer in l_manufacturers]
except:
  print('manufacturers.csv not found')

try:
  df_su = pd.read_csv("suppliers.csv")
  l_suppliers = df_su[['Product', 'Manufacturer', 'Supplier', 'Unit of Measure', 'Unit Price', 'Lead Time(days)', 'Delivery Time(days)', 'Country']].values.tolist()
  suppliers = [Suppliers(supplier[0],supplier[1],supplier[2],supplier[3],supplier[4],supplier[5],supplier[6],supplier[7]) for supplier in l_suppliers]
except:
  print('suppliers.csv not found')

############################## DEFINE COLUMNS FOR EACH SECTION

# !!!
# Create columns for our product table.
column_product_table = [
    ui.table_column(name='product', label='Product', sortable=True, searchable=True),
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True),
    ui.table_column(name='supplier', label='Supplier', sortable=True, searchable=True, ),
    ui.table_column(name='purchase_date', label='Purchase Date', sortable=True, data_type='time'),
    ui.table_column(name='qty', label='Qty', sortable=True, data_type='number'),
    ui.table_column(name='uom', label='Unit of Measure'),
    ui.table_column(name='cost_price', label='Cost Price', sortable=True, data_type='number'),
    ui.table_column(name='mfg_date', label='Manufacturing Date', sortable=True, data_type='time'),
    ui.table_column(name='exp_date', label='Expiry Date', sortable=True, data_type='time'),
    ui.table_column(name='selling_price', label='Selling Price', sortable=True, data_type='number'),
    ui.table_column(name='operational_cost', label='Operational Cost', sortable=True, data_type='number'),
    ui.table_column(name='lvl', label='Stockout level(%)', sortable=True, data_type='number'),
    ui.table_column(name='schedule', label='Schedule(days)', sortable=True, data_type='number'),
    ui.table_column(name='schedule_qty', label='Schedule Qty', sortable=True, data_type='number'),
    ui.table_column(name='rate', label='Avg. daily Consumption', sortable=True, data_type='number'),
    #ui.table_column(name='freq', label='frequency', sortable=True, data_type='number'),
]

# Manufacturer Name
# Item Name
# Item Price
# Item UoM
# Shelf Life (days)

# !!!
# Create columns for our manufacturer table.
column_manufacturer_table = [
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='country', label='Country', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='product', label='Product', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='uom', label='Unit of Measure'),
    ui.table_column(name='life', label='Shelf Life(days)')
]

# !!!
# Create columns for our supplier table
column_supplier_table = [
    ui.table_column(name='supplier', label='Supplier', sortable=True, searchable=True, ),
    ui.table_column(name='country', label='Country', sortable=True, searchable=True),
    ui.table_column(name='product', label='Product', sortable=True, searchable=True),
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True,),
    ui.table_column(name='uom', label='Unit of Measure'),
    ui.table_column(name='price', label='Unit Price'),
    ui.table_column(name='lead_time', label='Lead Time(days)'),
    ui.table_column(name='delivery_time', label='Delivery Time(days)')
]

##################################################################
##################################################################

current_tab = '#manufacturers' # set manufacturer section as default tab
@app('/test_catalogue_manager')
async def serve(q: Q):
  global current_tab
  print('Current tab: ', current_tab, q.args)
  if q.args['#']:
    q.args.menu = '#'+q.args['#']
  if q.args.menu:
    current_tab = q.args.menu
  if q.args.goto_manufacturer:
    current_tab = '#manufacturers'
  elif q.args.goto_supplier:
    current_tab = '#suppliers'
  
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

# !!!
# handle Supplier Table
async def showSuppliers(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
  print('items in supplier: ' + str(items))

  if q.args.show_inputs:
    df_m = pd.DataFrame(l_manufacturers, columns=['manufacturer', 'country', 'product', 'uom', 'life'])
    if len(df_m) == 0:
      items.extend([ui.message_bar(type='info', text='Try adding manufacturer first'),
        ui.button(name='goto_manufacturer', label='Close', primary=True)
        ])
    else:
      items.extend([ui.text_xl(content='Suppliers'),
        ui.textbox(name='supplier', label='Supplier'),
        ui.textbox(name='country', label='Country'),
        ui.dropdown(name='product', label='Product', choices=[
            ui.choice(name=x, label=x) for x in df_m['product'].unique()
        ]),
        ui.dropdown(name='manufacturer', label='Manufacturer', choices=[
            ui.choice(name=x, label=x) for x in df_m['manufacturer'].unique()
        ]),
        ui.dropdown(name='uom', label='Unit of Measure', choices=[
            ui.choice(name=x, label=x) for x in uom
        ]),
        ui.textbox(name='price', label='Price'),
        ui.textbox(name='lead_time', label='Lead Time(days)'),
        ui.textbox(name='delivery_time', label='Delivery Time(days)'),
        ui.button(name='show_tables', label='Submit', primary=True)
        ])

  else:     
    if q.args.show_tables:
      l_suppliers.append([q.args.product,q.args.manufacturer,q.args.supplier,q.args.uom, q.args.price, q.args.lead_time, q.args.delivery_time, q.args.country])
      s = Suppliers(q.args.product,q.args.manufacturer,q.args.supplier,q.args.uom, q.args.price, q.args.lead_time, q.args.delivery_time, q.args.country)
      suppliers.append(s)
      items.append(ui.message_bar(type='success', text='You have successfully added a supplier'))
    if len(suppliers) > 0:
      items.append(
        ui.table(
          name='suppliers',
          columns=column_supplier_table,
          rows=[ui.table_row(
              name=supplier.id,
              cells=[supplier.supplier, supplier.country, supplier.product, supplier.manufacturer, supplier.uom, supplier.price, supplier.lead_time, supplier.delivery_time]
              ) for supplier in suppliers],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))
    else:
      items.append(ui.text_l(content='No Supplier found'))

    items.append(ui.button(name='show_inputs', label='Add Supplier', primary=True))

  q.page['example'] = ui.form_card(box='1 1 -1 11', items=items)
  await q.page.save()

# !!!
# handle Manufacturer Table
async def showManufacturers(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
  if q.args.show_inputs:
    items.extend([ui.text_xl(content='Manufacturers'),
        ui.textbox(name='manufacturer', label='Manufacturer'),
        ui.textbox(name='country', label='Country'),
        ui.textbox(name='product', label='Product'),
        ui.dropdown(name='uom', label='Unit of Measure', choices=[
            ui.choice(name=x, label=x) for x in uom
        ]),
        ui.textbox(name='life', label='Shelf Life(days)'),
        ui.button(name='show_tables', label='Submit', primary=True)])
  else:     
    if q.args.show_tables:
      l_manufacturers.append([q.args.manufacturer, q.args.country, q.args.product, q.args.uom, q.args.life])
      m = Manufacturers(q.args.manufacturer, q.args.country, q.args.product, q.args.uom, q.args.life)
      manufacturers.append(m)
      items.append(ui.message_bar(type='success', text='You have successfully added a product'))
    if len(manufacturers) > 0:
      items.append(
        ui.table(
          name='manufacturers',
          columns=column_manufacturer_table,
          
          rows=[ui.table_row(
              name=manufacturer.id,
              cells=[manufacturer.manufacturer, manufacturer.country, manufacturer.product, manufacturer.uom, manufacturer.life]
              ) for manufacturer in manufacturers],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))
    else:
      items.append(ui.text_l(content='No Manufacturer found'))
    items.append(ui.button(name='show_inputs', label='Add Manufacturer', primary=True))
  q.page['example'] = ui.form_card(box='1 1 -1 11', items=items)
  await q.page.save()


filter_product = None
filter_manufacturer = None
filter_supplier = None
unit_measure = None
cost_price = None
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
  print(q.args.show_tables,q.args.show_inputs)
  if (q.args.show_tables==None or q.args.show_tables==False) and (q.args.show_inputs or q.args.product or q.args.manufacturer or q.args.supplier or q.args.qty):
    df_m = pd.DataFrame(l_manufacturers, columns=['manufacturer', 'country', 'product', 'uom', 'life'])
    df_s = pd.DataFrame(l_suppliers, columns=['product','manufacturer','supplier','uom', 'price', 'lead_time', 'delivery_time', 'country'])
    if len(df_m) == 0:
      items.extend([ui.message_bar(type='info', text='Try adding manufacturer first'),
        ui.button(name='goto_manufacturer', label='Close', primary=True)
        ])
    elif len(df_s) == 0:
      items.extend([ui.message_bar(type='info', text='Try adding supplier first'),
        ui.button(name='goto_supplier', label='Close', primary=True)
        ])
    else:
        items.append(ui.text_xl(content='Product'))
        print(q.args.product , q.args.manufacturer, q.args.supplier)
        if q.args.product and (filter_product==None or q.args.product!=filter_product) :
          filter_product = q.args.product
          filter_manufacturer = None 
          filter_supplier = None
          unit_measure = None
          cost_price = None
          gqty = None
        elif q.args.manufacturer and (filter_manufacturer==None or q.args.manufacturer!=filter_manufacturer):
          filter_manufacturer = q.args.manufacturer
          filter_supplier = None
          unit_measure = None
          cost_price = None
          gqty = None
        elif q.args.supplier and (filter_supplier==None or q.args.supplier!=filter_supplier):
          filter_supplier = q.args.supplier
          unit_measure = None
          cost_price = None
          gqty = None
        if q.args.qty:
          gqty = q.args.qty

        print(filter_product, filter_manufacturer, filter_supplier)
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

        if filter_supplier!=None:
          items.append(ui.dropdown(name='supplier', label='Supplier', choices=[
              ui.choice(name=x, label=x) for x in tmp_s
          ], trigger = True, value = filter_supplier))
          cost_price = df_s[(df_s['product']==filter_product)&(df_s['manufacturer']==filter_manufacturer)
                            &(df_s['supplier']==filter_supplier)]['price'].values[0]
          unit_measure = df_s[(df_s['product']==filter_product)&(df_s['manufacturer']==filter_manufacturer)
                            &(df_s['supplier']==filter_supplier)]['uom'].values[0]
        else:
          items.append(ui.dropdown(name='supplier', label='Supplier', choices=[
              ui.choice(name=x, label=x) for x in tmp_s
          ], trigger = True))
          cost_price = None

        items.append(ui.date_picker(name='purchase_date', label='Purchase Date'))
        items.append(ui.textbox(name='qty', label='Qty'))

        if unit_measure!=None:
          items.append(ui.textbox(name='uom', label='Unit of Measure', value = unit_measure, readonly = True))
        else:
          items.append(ui.dropdown(name='uom', label='Unit of Measure', choices=[
                ui.choice(name=x, label=x) for x in uom
            ]))

        if cost_price!=None:
          items.append(ui.textbox(name='cost_price', label='Cost Price', value = str(cost_price)))
        else:
          items.append(ui.textbox(name='cost_price', label='Cost Price'))

        items.extend([ui.date_picker(name='mfg_date', label='Mfg Date'),
          ui.date_picker(name='exp_date', label='Exp Date'),
          ui.textbox(name='selling_price', label='Selling Price'),
          ui.textbox(name='operational_cost', label='Operational Cost'),
          ui.textbox(name='lvl', label='Order Point by level(%)'),
          ui.textbox(name='schedule', label='Order Point Schedule (days)'),
          ui.textbox(name='schedule_qty', label='Scheduled Qty'),
          ui.textbox(name='rate', label='Avg. Consumption'),
          # ui.dropdown(name='freq', label='Consumption Frequency', choices=[
          #     ui.choice(name=x, label=x, value='daily', readonly=True) for x in consumption
          # ]), 
          ui.button(name='show_tables', label='Submit', primary=True)])
  else: 
    filter_product = None    
    filter_manufacturer = None 
    filter_supplier = None
    unit_measure = None
    cost_price = None
    gqty = None
    if q.args.show_tables:
      l_products.append([q.args.product, q.args.manufacturer, q.args.supplier, q.args.purchase_date, q.args.qty,
                  q.args.uom, q.args.cost_price, q.args.mfg_date, q.args.exp_date, q.args.selling_price, 
                  q.args.operational_cost, q.args.lvl, q.args.schedule, q.args.schedule_qty, q.args.rate])
      p = Products(q.args.product, q.args.manufacturer, q.args.supplier, q.args.purchase_date, q.args.qty,
                  q.args.uom, q.args.cost_price, q.args.mfg_date, q.args.exp_date, q.args.selling_price, 
                  q.args.operational_cost, q.args.lvl, q.args.schedule, q.args.schedule_qty, q.args.rate)
      products.append(p)
      items.append(ui.message_bar(type='success', text='You have successfully added a product'))
    if len(products) > 0:
      items.append(
        ui.table(
          name='products',
          columns=column_product_table,
          rows=[ui.table_row(
              name=product.id,
              cells=[product.product, product.manufacturer, product.supplier, product.purchase_date, product.qty,
                  product.uom, product.cost_price, product.mfg_date, product.exp_date, product.selling_price, 
                  product.operational_cost, product.lvl, product.schedule, product.schedule_qty, product.rate]
              ) for product in products],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))
    else:
      items.append(ui.text_l(content='No Product found'))
    items.append(ui.button(name='show_inputs', label='Add Product', primary=True))
  q.page['example'] = ui.form_card(box='1 1 -1 11', items=items)
  await q.page.save()
