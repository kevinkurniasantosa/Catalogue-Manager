# Form
# Use a form to collect data or show textual information.
# ---
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

product_csv = "product.csv"
manufacturer_csv = "manufacturer.csv"
supplier_csv = "supplier.csv"
logistic_csv = "logistic.csv" 

p_id = 0
m_id = 0
s_id = 0
l_id = 0

# !!!
# save tabs 
tabs = [
    ui.tab(name='#manufacturers', label='Manufacturers'),
    ui.tab(name='#suppliers', label='Suppliers'),
    ui.tab(name='#logistics', label='Logistics'),
    ui.tab(name='#products', label='Products'), 
    ui.tab(name='#simulate', label='Simulate'),
]

uom = ['Strips', 'Ampoules', 'Boxes', 'Litres']
logistics_category = ['Fragile', 'Boxes', 'Heavy', 'Priority']
consumption = ['daily', 'weekly', 'monthly']

class Products:
    def __init__(self, product: str, manufacturer: str, supplier: str, 
                purchase_date: str, qty: float, uom: str, 
                cost_price: float, mfg_date: str, exp_date: str, 
                selling_price: float, operational_cost: float, lvl: float, 
                schedule: int, schedule_qty: float, rate: float):
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
        #self.freq = freq

class Manufacturers:
    def __init__(self, manufacturer: str, country: str, product: str, uom:str, life:str):
        global m_id
        m_id += 1
        self.id = f'I{m_id}'
        self.product = product
        self.manufacturer = manufacturer
        self.country = country
        self.uom = uom
        self.life = life

class Suppliers:
    def __init__(self, product: str, manufacturer: str, supplier: str, uom: str, price: float, lead_time: int, delivery_time: int, country: str):
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

class Logistics:
    def __init__(self, provider: str, country: str, category: int, price_kg: float, price_km: float):
        global l_id
        l_id += 1
        self.id = f'I{l_id}'
        self.provider = provider
        self.country = country
        self.category = category
        self.price_kg = price_kg
        self.price_km = price_km

# Create some products
products = []
manufacturers = []
suppliers = []
logistics = []

l_products = []
l_manufacturers = []
l_suppliers = []
l_logistics = []

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

column_manufacturer_table = [
    ui.table_column(name='manufacturer', label='Manufacturer', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='country', label='Country', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='product', label='Product', sortable=True, searchable=True, max_width='300'),
    ui.table_column(name='uom', label='Unit of Measure'),
    ui.table_column(name='life', label='Shelf Life(days)')
]

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

column_logistic_table = [
    ui.table_column(name='provider', label='Provider', sortable=True, searchable=True, ),
    ui.table_column(name='country', label='Country', sortable=True, searchable=True),
    ui.table_column(name='category', label='Goods Category', sortable=True, searchable=True),
    ui.table_column(name='price_kg', label='Price per kg', sortable=True),
    ui.table_column(name='price_distance', label='Price per km', sortable=True),
] 

column_insight_table = [
    ui.table_column(name='product', label='Product', sortable=True, searchable=True, ),
    ui.table_column(name='turnover', label='Turnover', sortable=True, ),
    ui.table_column(name='expired qty%', label='Expired(%)', sortable=True),
    ui.table_column(name='spoilage($)%', label='Spoilage($)%', sortable=True),
    ui.table_column(name='cumulative_demand', label='Demand(%) Cumulative ', sortable=True, ),
    ui.table_column(name='sell-through', label='Sell-Through(%)', sortable=True, ),
    ui.table_column(name='demand met(%)', label='Demand Met(%)', sortable=True),  
    #ui.table_column(name='cumulative_soh_qty', label='SOH qty(%) Cumulative', sortable=True,),   
    ui.table_column(name='Revenue(%)', label='Revenue(%)', sortable=True),
    ui.table_column(name='Revenue Missed(%)', label='Revenue Missed(%)', sortable=True),
    ui.table_column(name='cumulative_operational_cost', label='Operational Cost(%) Cumulative', sortable=True),
]

current_tab = '#manufacturers'
@app('/catalogue_manager')
async def serve(q: Q):
  global current_tab
  print('current_tab',current_tab, q.args)
  if q.args['#']:
    q.args.menu = '#'+q.args['#']
  if q.args.menu:
    current_tab = q.args.menu
  if q.args.goto_manufacturer:
    current_tab = '#manufacturers'
  elif q.args.goto_supplier:
    current_tab = '#suppliers'
  
  if current_tab != '#simulate':
    del q.page['plot']
    del q.page['consumption_insight']
    del q.page['controls']
    del q.page['summary1']
    del q.page['summary2']
    del q.page['summary3']
    del q.page['summary4']
    del q.page['summary5']

  if current_tab == '#products':
    await showProducts(q)
  elif current_tab == '#manufacturers':
    await showManufacturers(q)
  elif current_tab == '#suppliers':
    await showSuppliers(q)
  elif current_tab == '#logistics':
    await showLogistics(q)
  elif current_tab == '#simulate':
    await generateInsights(q)
  else:
    await showManufacturers(q)
  await q.page.save()
  

def get_distribution(mu, days):
    sigma = random.randrange(1,mu)
    a, b = 0, 2*mu
    dist = stats.truncnorm((a - mu) / sigma, (b - mu) / sigma, loc=mu, scale=sigma)

    values = dist.rvs(days)
    return [int(x) for x in values]


startDate = None
endDate = None
demo_product = None

# !!!
# simulate and generate insights
async def generateInsights(q: Q):
  global l_products
  global startDate
  global endDate
  global demo_product
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
  items.append(ui.text_xl(content='Period'))
  print(q.args.show_tables,q.args.demo_product)
  if (startDate!=None and endDate!=None) or (q.args.show_tables!=None and q.args.show_tables==True) or q.args.demo_product!=None:
    if q.args.start:
      startDate = q.args.start
    if q.args.end:
      endDate = q.args.end
    if q.args.demo_product:
      demo_product = q.args.demo_product
    items.extend([ui.date_picker(name='start', label='From Date', value=startDate),
    ui.date_picker(name='end', label='To Date', value= endDate),
    ui.button(name='show_tables', label='Insights', primary=True)])
    #items.append(ui.message_bar(type='success', text='This is where we show insights'))
    print(q.args.start)
    
    start = pd.to_datetime(startDate, format='%Y-%m-%d', errors='ignore')
    end = pd.to_datetime(endDate, format='%Y-%m-%d', errors='ignore')
    day_count = (end - start).days
    df_products = pd.DataFrame(l_products,columns=['Product', 'Manufacturer', 'Supplier', 'Purchase Date', 'Qty',
       'Unit of Measure', 'Cost Price', 'Manufacturing Date', 'Expiry Date',
       'Selling Price', 'Operational Cost', 'Stockout level(%)',
       'Schedule(days)', 'Schedule Qty', 'Consumption'])
    df_products = df_products.dropna()
    if q.args.demo_Simulate:
        df_products.loc[df_products['Product']==q.args.demo_product,'Qty'] = float(q.args.demo_initialQty)
        df_products.loc[df_products['Product']==q.args.demo_product,'Stockout level(%)'] = float(q.args.demo_stockout_level)
        df_products.loc[df_products['Product']==q.args.demo_product,'Schedule Qty'] = float(q.args.demo_reorder_Qty)
        df_products.loc[df_products['Product']==q.args.demo_product,'Schedule(days)'] = float(q.args.demo_reorder_schedule)
        l_products = df_products.values.tolist()
    df_products['Purchase Date'] = pd.to_datetime(df_products['Purchase Date'])
    df_products['Manufacturing Date'] = pd.to_datetime(df_products['Manufacturing Date'])
    df_products['Expiry Date'] = pd.to_datetime(df_products['Expiry Date'])
    df_products['shelf_life'] = df_products['Expiry Date'] - df_products['Manufacturing Date']
    df_products['shelf_life'] = df_products.apply(lambda x: x['shelf_life'].days, axis =1)
    dict_life = {}
    for l in df_products[['Product','shelf_life']].values.tolist():
        dict_life[l[0]] = l[1] 

    expiry_status = {}
    orders = []
    price = {}
    initial_qty = {}
    sell_through = []
    for _,p in df_products.iterrows():
        price[p['Product']]={'CP':p['Cost Price'], 'SP':p['Selling Price'], 'OP':p['Operational Cost']}
        mu = p.Consumption
        days = day_count
        # if p.frequency =='weekly':
        #     days = 7
        # elif p.frequency == 'monthly':
        #     days = 30
        # else:
        #     days = 365
        
        soh = p.Qty
        initial_qty[p['Product']] = p.Qty
        expiry_date = {}
        expiry_date[p['Expiry Date']] = p.Qty
        list_expiry_dates = [p['Expiry Date']]
        sold_to_date = 0
        order_pt_level = p['Stockout level(%)']
        buffer = order_pt_level*soh/100
        #print(buffer)
        n_reorder = p['Schedule Qty']
        order_pt_schedule = p['Schedule(days)']
        sell_through_soh = p.Qty
        sell_through_sold_units = 0
        #for single_date in (start + timedelta(n) for n in range(0,day_count+1, days)):
        for i,demand in enumerate(get_distribution(mu,days)):
            simdate = start+ timedelta(i)
            placed_order = False
            #print(simdate,list_expiry_dates, expiry_date, soh) 
            
            if(simdate in expiry_date):
                #print("simdate in expiry_date <<", simdate,list_expiry_dates, expiry_date, soh)
                soh = soh - expiry_date[simdate]
                orders.append([simdate.strftime("%Y-%m-%d"),p['Product'],expiry_date[simdate], 'expired', soh])
                del expiry_date[simdate]
                list_expiry_dates.remove(simdate)
                list_expiry_dates.sort()
                #print("simdate in expiry_date >>", simdate,list_expiry_dates, expiry_date, soh)
                
            n2orders = 0
            if demand != 0:
                if soh >= demand:
                    soh = soh - demand
                    orders.append([simdate.strftime("%Y-%m-%d"),p['Product'],-demand,'consumed', soh])
                    sell_through_sold_units = sell_through_sold_units + demand
                    if demand < expiry_date[list_expiry_dates[0]]:
                        expiry_date[list_expiry_dates[0]] = expiry_date[list_expiry_dates[0]] - demand
                    else:
                        #print("demand < expiry_date[list_expiry_dates[0]] >>", simdate,list_expiry_dates, expiry_date, soh,demand)
                        old = expiry_date[list_expiry_dates[0]]
                        del expiry_date[list_expiry_dates[0]]
                        del list_expiry_dates[0]
                        if(len(list_expiry_dates)>0):
                            expiry_date[list_expiry_dates[0]] = expiry_date[list_expiry_dates[0]] - demand + old
                        #print("demand < expiry_date[list_expiry_dates[0]] <<", simdate,list_expiry_dates, expiry_date, soh)
            
                else:
                    orders.append([simdate.strftime("%Y-%m-%d"),p['Product'],-demand,'unfulfilled', soh])
            
            if (simdate != p['Purchase Date']) and ((simdate - p['Purchase Date']).days%order_pt_schedule == 0):
                soh = soh + n_reorder
                orders.append([simdate.strftime("%Y-%m-%d"),p['Product'],n_reorder, 'scheduled', soh])
                placed_order = True
                if simdate + timedelta(dict_life[p['Product']]) in expiry_date:
                    expiry_date[simdate + timedelta(dict_life[p['Product']])] = expiry_date[simdate + timedelta(dict_life[p['Product']])] + n_reorder
                else:
                    expiry_date[simdate + timedelta(dict_life[p['Product']])] = n_reorder
                    list_expiry_dates.append(simdate + timedelta(dict_life[p['Product']]))
                    list_expiry_dates.sort()
            while(soh <= buffer):
                soh = soh + n_reorder
                orders.append([simdate.strftime("%Y-%m-%d"),p['Product'],n_reorder, 'adhoc', soh])
                placed_order = True
                if simdate + timedelta(dict_life[p['Product']]) in expiry_date:
                    expiry_date[simdate + timedelta(dict_life[p['Product']])] = expiry_date[simdate + timedelta(dict_life[p['Product']])] + n_reorder
                else:
                    expiry_date[simdate + timedelta(dict_life[p['Product']])] = n_reorder
                    list_expiry_dates.append(simdate + timedelta(dict_life[p['Product']]))
                    list_expiry_dates.sort()
            if placed_order == True:  
                sell_through.append([simdate.strftime("%Y-%m-%d"),p['Product'],sell_through_sold_units,sell_through_soh])
                sell_through_sold_units = 0
                sell_through_soh = soh
        
        expiry_status[p['Product']] = expiry_date
        
    df_ledger = pd.DataFrame(orders, columns= ['date','product','qty','status','soh'])

    df_expired = df_ledger[df_ledger.status=='expired']
    if len(df_expired) > 0:
      df_expired = df_expired.groupby('product', as_index=False)['qty'].sum()
      df_expired['value'] = df_expired.apply(lambda x: x['qty']*price[x['product']]['CP'], axis =1)

    df_consumption = df_ledger[df_ledger.qty < 0]
    df_consumption['total_value'] = df_consumption.apply(lambda x:price[x['product']]['SP']*(-x['qty']), axis =1)
    df_consumption['total_purchase_cost'] = df_consumption.apply(lambda x:price[x['product']]['CP']*(-x['qty']), axis =1)
    consumption_fulfilled = len(df_consumption[df_consumption['status']=='consumed'])
    consumption_unfulfilled = len(df_consumption[df_consumption['status']=='unfulfilled'])
    units_fulfilled = -df_consumption[df_consumption['status']=='consumed']['qty'].sum()
    units_unfulfilled = -df_consumption[df_consumption['status']=='unfulfilled']['qty'].sum()
    total_units_requested = -df_consumption.qty.sum()
    value_fulfilled = int(df_consumption[df_consumption['status']=='consumed']['total_value'].sum())
    value_unfulfilled = df_consumption[df_consumption['status']=='unfulfilled']['total_value'].sum()
    value_units_requested = df_consumption.total_value.sum()
    total_purchase_cost = df_consumption[df_consumption['status']=='consumed']['total_purchase_cost'].sum()
    loss_expired_items = 0
    if len(df_expired) > 0:
      loss_expired_items = df_expired.value.sum()
      
    overall_units_fulfillment = "%.2f"%(100*units_fulfilled/total_units_requested)+'%'
    revenue_missed = str(f"{value_unfulfilled:,.2f}")+'  ('+str("%.2f" %(100*value_unfulfilled/(value_unfulfilled+value_fulfilled)))+'%)'
    total_purchase_cost = f"{total_purchase_cost:,.2f}"

    df_soh = pd.DataFrame(pd.DataFrame(expiry_status).sum())
    df_soh['cost'] = df_soh.apply(lambda x: price[x.name]['CP'], axis =1)
    df_soh['value'] = df_soh[0]*df_soh['cost']
    if len(df_expired) > 0:
      df_soh['expired'] = df_soh.apply(lambda x: df_expired[df_expired['product']==x.name]['qty'], axis =1)
      df_soh = df_soh.fillna(0)
    else:
      df_soh['expired'] = 0
    df_soh['total_qty'] = df_soh[0]+df_soh['expired']
    df_soh['exp%'] = 100*df_soh['expired']/df_soh['total_qty']
    df_soh['exp_value'] = df_soh['expired']*df_soh['cost']
    df_soh['total_value'] = df_soh['total_qty']*df_soh['cost']

    #q.page['bkg'] = ui.form_card(box='1 5 -1 5', items=[ui.text_xs(content='')])
    df_turnover = df_ledger[df_ledger['status']=='consumed'].groupby('product').sum().drop('soh', axis = 1)
    df_turnover['sales'] = df_turnover.apply(lambda x: price[x.name]['CP'], axis =1)
    df_turnover['sales'] = -df_turnover['sales']*df_turnover['qty']
    df_turnover['avg inventory'] = df_turnover.apply(lambda x: (initial_qty[x.name]+df_soh.loc[x.name]['total_qty'])/2, axis =1)
    df_turnover['avg inventory'] = df_turnover.apply(lambda x: x['avg inventory']*price[x.name]['CP'], axis =1)
    df_turnover['turnover'] = (365/day_count)*(df_turnover['sales']/df_turnover['avg inventory'])
    inventory_turnover_period = "%.2f" %((365/day_count)*(df_turnover['sales'].sum()/df_turnover['avg inventory'].sum()))

    df_sellthrough = pd.DataFrame(sell_through, columns = ['date', 'product','units_sold','SOH'])
 
    df_sellthrough['sellthrough'] = 100*df_sellthrough['units_sold']/df_sellthrough['SOH']
    df_sellthrough = df_sellthrough.groupby('product').sum()
    df_sellthrough['sellthrough'] = 100*df_sellthrough['units_sold']/df_sellthrough['SOH']
    sellthrough = "%.2f" %(100*df_sellthrough['units_sold'].sum()/df_sellthrough['SOH'].sum())

    q.page['summary1'] = ui.form_card(box='1 5 2 2', items=[
      ui.textbox(name='inventory_turnover_period', label='Inventory Turnover', value=inventory_turnover_period, readonly=True, tooltip="Number of times inventory was sold in a year. Low = weak sales and possibly excess inventory. High  = strong sales or insufficient inventory."),
      ui.textbox(name='sell_through_rate', label='Sell-Through Rate (%)', value=sellthrough, readonly=True, tooltip="Inventory sold between purchases ( >80% : good,  <40% : bad, 40% - 80% : fair )."),])
    q.page['summary2'] = ui.form_card(box='3 5 2 2', items=[
      ui.textbox(name='value_fulfilled', label='Total revenue($)', value=f"{value_fulfilled:,.2f}", readonly=True),
      ui.textbox(name='revenue_missed', label='Revenue Missed (Insufficient stock)', value=revenue_missed, readonly=True),])
    total_op_cost = 0
    for i in df_products['Product'].unique():
        total_op_cost = total_op_cost + day_count*price[i]['OP']
    q.page['summary3'] = ui.form_card(box='5 5 2 2', items=[
      ui.textbox(name='total_purchase_cost', label='Total Purchase Cost($)', value=total_purchase_cost, readonly=True),
      ui.textbox(name='total_op_cost', label='Total Operational Cost($)', value=f"{total_op_cost:,.2f}", readonly=True),])
    if len(df_expired) > 0:
      str_loss_expired_items = str(f"{loss_expired_items:,.2f}")+" ("+"%.2f"%(100*df_expired.value.sum()/df_soh['total_value'].sum())+"%)"
    else:
      str_loss_expired_items = loss_expired_items
    q.page['summary4'] = ui.form_card(box='7 5 2 2', items=[
      ui.textbox(name='inventry_valuation', label='Inventory Valuation($)', value=f"{df_soh['total_value'].sum():,.2f}", readonly=True),
      ui.textbox(name='loss_expired_items', label='Loss on Expired items($)', value= str_loss_expired_items, readonly=True),])
    total_purchase_cost = df_consumption[df_consumption['status']=='consumed']['total_purchase_cost'].sum()
    balance = f"{value_fulfilled - total_purchase_cost - total_op_cost -loss_expired_items:,.2f}"
    q.page['summary5'] = ui.form_card(box='9 5 2 2', items=[
      ui.textbox(name='balance', label='Balance($)', value=balance, readonly=True),
      #ui.textbox(name='overall_units_fulfillment', label='Overall Units Fulfillment', value=overall_units_fulfillment, readonly=True),
      ])
    
    df_revenue = df_consumption[df_consumption.status=='consumed'].groupby('product', as_index=False)['total_value'].sum()
    df_revenue['ranking'] = df_revenue.apply(lambda x: "%.2f"%(100*x['total_value']/df_revenue.total_value.sum()), axis =1)


    df_rank = df_consumption.groupby('product', as_index=False)['qty','total_value'].sum()
    df_rank['turnover']=df_rank.apply(lambda x: "%.2f" %df_turnover.loc[x['product']]['turnover'], axis =1)
    df_rank['expired qty%'] = df_rank.apply(lambda x: "%.2f" %df_soh.loc[x['product']].values[5], axis =1)
    df_rank['spoilage($)%'] = df_rank.apply(lambda x: "%.2f" %(100*df_soh.loc[x['product']].values[6]/df_soh['total_value'].sum()), axis =1)
    df_rank['cumulative demand(%)']=df_rank.apply(lambda x: "%.2f" %(100*x['qty']/df_rank.qty.sum()), axis =1)
    df_rank['sell-through']=df_rank.apply(lambda x: "%.2f" %df_sellthrough.loc[x['product']]['sellthrough'], axis =1)
    df_rank['demand met(%)'] = df_rank.apply(lambda x: "%.2f" %(100*df_consumption[(df_consumption['product']==x['product'])&(df_consumption['status']=='consumed')]['qty'].sum()/x['qty']), axis = 1)
    df_rank['Revenue(%)'] = df_rank.apply(lambda x: df_revenue[df_revenue['product']==x['product']]['ranking'].values[0], axis = 1)
    df_rank['Revenue Missed(%)'] = df_rank.apply(lambda x: "%.2f" %(100*df_consumption[(df_consumption['product']==x['product'])&(df_consumption['status']=='unfulfilled')]['total_value'].sum()/df_consumption[df_consumption['status']=='unfulfilled']['total_value'].sum()), axis =1)
    df_rank['cumulative operational cost(%)'] = df_rank.apply(lambda x:100*price[x['product']]['OP']/pd.DataFrame(price).T['OP'].sum(), axis=1)
    df_rank = df_rank.drop(['qty','total_value'], axis =1)

    rank = df_rank.values.tolist()
    q.page['consumption_insight'] = ui.form_card(box='1 7 -1 5', items=[
      ui.text_xl(content='Productwise'),
      ui.table(
          name='Insights',
          columns=column_insight_table,
          rows=[ui.table_row(
              name=r[0],
              cells=[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]]
              ) for r in rank],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='300px'
      )
    ])
    if demo_product!=None:
      selected_p = demo_product
    else:
      selected_p = df_products['Product'].unique()[0]  
    selected_p_stockout = "%.2f" %(df_products[df_products['Product']==selected_p]['Stockout level(%)'].values[0])
    selected_p_reorder = "%.2f" %(df_products[df_products['Product']==selected_p]['Schedule Qty'].values[0])
    selected_p_reorder_days = "%.2f" %(df_products[df_products['Product']==selected_p]['Schedule(days)'].values[0])
    q.page['controls'] = ui.form_card(
        box='1 12 5 6',
        items=[
            ui.text_xl("Try me for optimizing"),
            ui.dropdown(name='demo_product', label='Product', choices=[
                ui.choice(name=x, label=x) for x in df_products['Product'].unique()
            ],trigger = True, value=selected_p),
            ui.textbox(name='demo_initialQty', label='Initial Quantity', value=initial_qty[selected_p]),
            ui.textbox(name='demo_stockout_level', label='Stockout level (% of initial qty)', value=selected_p_stockout),
            ui.textbox(name='demo_reorder_Qty', label='Reorder Quantity', value=selected_p_reorder),
            ui.textbox(name='demo_reorder_schedule', label='Reorder Schedule (days)', value=selected_p_reorder_days),
            ui.button(name='demo_Simulate', label='Simulate', primary=True)
        ]
    )
    q.page['plot'] = ui.markdown_card(box='6 12 5 6', title='Your plot!', content='')
    image_path = {}
    df_ledger_ai = df_ledger.copy()
    df_ledger_ai['month_year'] = pd.to_datetime(df_ledger_ai['date']).dt.to_period('M')
    df_ledger_ai['init_soh'] = df_ledger_ai['soh'] - df_ledger_ai['qty']
    idx_exp = df_ledger_ai[df_ledger_ai['status']=='expired'].index
    df_ledger_ai.loc[idx_exp, 'init_soh'] = df_ledger_ai.loc[idx_exp, 'soh']  + df_ledger_ai.loc[idx_exp, 'qty'] 
    idx_unfulfilled = df_ledger_ai[df_ledger_ai['status']=='unfulfilled'].index
    df_ledger_ai.loc[idx_unfulfilled, 'init_soh'] = df_ledger_ai.loc[idx_unfulfilled, 'init_soh']  + df_ledger_ai.loc[idx_unfulfilled, 'qty'] 

    monthly_starting_SOH = df_ledger_ai.groupby(['product','month_year'], as_index = False).head(1)
    monthly_starting_SOH = monthly_starting_SOH[['product','month_year','init_soh']]
    monthly_starting_SOH['status'] = 'init_soh'
    monthly_starting_SOH = monthly_starting_SOH.rename(columns={'init_soh':'qty'})

    df_ledger_ai = df_ledger_ai.groupby(['product','month_year','status'], as_index=False)['qty'].sum()
    df_ledger_ai = df_ledger_ai[['product', 'status', 'month_year', 'qty']].append(monthly_starting_SOH[['product', 'status', 'month_year', 'qty']])
    df_ledger_ai = df_ledger_ai.groupby(['product','month_year','status'], as_index=False)['qty'].sum()
    for p in df_ledger_ai['product'].unique():
        print(p)
        df_ts = df_ledger_ai[df_ledger_ai['product'] == p].pivot(index ='month_year',columns='status', values='qty').fillna(0)
        df_ts['sold'] = -df_ts['consumed']
        df_ts = df_ts.drop(['consumed'], axis=1)
        try:
            df_ts['soh'] = df_ts['init_soh']+df_ts['scheduled']+df_ts['adhoc']
        except:
            try:
                df_ts['soh'] = df_ts['init_soh']+df_ts['scheduled']
            except:
                df_ts['soh'] = df_ts['init_soh']
        try:
            df_ts['unfulfilled'] = -df_ts['unfulfilled']
            df_ts['demand'] = df_ts['sold'] + df_ts['unfulfilled']
        except:
            df_ts['demand'] = df_ts['sold']       
        df_ts.reset_index(inplace=True)

        #print(df_ts)
        plt.subplots(1)
        plt.plot(df_ts.index,df_ts['demand'] ,label="demand")
        plt.plot(df_ts.index,df_ts['soh'], label ="SOH")
        plt.plot(df_ts.index,df_ts['sold'], label ="units sold")
        try:
          df_ts_exp = df_ts[df_ts['expired']>0]
          if len(df_ts_exp) > 0:
              plt.plot(df_ts_exp.index,df_ts_exp['expired'], 'x', color='red',label ="units expired")
        except:
          pass
        plt.xlabel('month')
        plt.ylabel('units')
        plt.legend()
        #image_filename = f'{str(uuid.uuid4())}.png'
        image_filename = f'{str(uuid.uuid4())}.png'
        plt.savefig(image_filename)
        image_path[p], = await q.site.upload([image_filename])
        os.remove(image_filename)
        df_ts.to_csv(p+'.csv')
    q.page['plot'].content = f'![plot]({image_path[selected_p]})'
    q.page['plot'].title = selected_p
  else:
    items.extend([ui.date_picker(name='start', label='From Date',),
    ui.date_picker(name='end', label='To Date'),
    ui.button(name='show_tables', label='Insights', primary=True)])
  q.page['example'] = ui.form_card(box='1 1 -1 4', items=items)
  await q.page.save()

# !!!
# handle logistics 
async def showLogistics(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
  if q.args.show_inputs:
    items.extend([ui.text_xl(content='Logistics'),
        ui.textbox(name='provider', label='Provider'),
        ui.textbox(name='country', label='Country'),
        ui.dropdown(name='category', label='Category', choices=[
            ui.choice(name=x, label=x) for x in logistics_category
        ]),
        ui.textbox(name='price_kg', label='Price per kg'),
        ui.textbox(name='price_km', label='Price per km'),
        ui.button(name='show_tables', label='Submit', primary=True)])
  else:     
    if q.args.show_tables:
      l_logistics.append(q.args.provider, q.args.country, q.args.category, q.args.price_kg, q.args.price_km)
      l = Logistics(q.args.provider, q.args.country, q.args.category, q.args.price_kg, q.args.price_km)
      logistics.append(l)
      items.append(ui.message_bar(type='success', text='You have successfully added a logistic provider'))
    if len(logistics) > 0:
      items.append(
        ui.table(
          name='logistics',
          columns=column_logistic_table,
          rows=[ui.table_row(
              name=provider.id,
              cells=[provider.provider, provider.country, provider.category, provider.price_kg, provider.price_km]
              ) for provider in logistics],
          groupable=True,
          downloadable=True,
          resettable=True,
          height='500px'
      ))
    else:
      items.append(ui.text_l(content='No Logistics Provider found'))
    items.append(ui.button(name='show_inputs', label='Add Provider', primary=True))
  q.page['example'] = ui.form_card(box='1 1 -1 11', items=items)
  await q.page.save()

# !!!
# handle Supplier Table
async def showSuppliers(q: Q):
  items = [ui.tabs(name='menu', value=q.args.menu, items=tabs)]
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
