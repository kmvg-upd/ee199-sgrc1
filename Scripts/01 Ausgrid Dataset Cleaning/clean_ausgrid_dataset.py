
'''
    Extracts 1 week worth of data (Dec 5-11, 2010) from the Ausgrid dataset and removes invalid customers.
'''

# Add pandas and date offsets library.
import pandas as pd
from pandas.tseries.offsets import Day

# Import the csv file, assign it to variable fname.
fname = '2010-2011 Solar home electricity data.csv'
# Load the CSV into a DataFrame.
d_raw = pd.read_csv(fname,
                    skiprows=1, # Skip 1st row which is a whitespace
                    parse_dates=['date'], # Convert 'date' string column into datetime data type.
                    dayfirst=True, # Dayfirst allows International date format (YYYY-MM-DD).
                    na_filter=False) # Does not detect missing value markers which can improve the performance of reading a large file.

# Get customers with a CL consumption category on the first date.
df_CL = d_raw[(d_raw['date'] == pd.to_datetime('7/1/2010', format='%m/%d/%Y')) & (d_raw['Consumption Category'] == 'CL')]
print('Number of customers with CL: {0}'.format(len(df_CL.Customer.unique())))

# Get non CL customers by getting the complement of CL.
df_nonCL = d_raw[~(d_raw['Customer'].isin(df_CL.Customer))]
print('Number of customers without CL: {0}'.format(len(df_nonCL.Customer.unique())))

# Get nonCL entries from the selected time interval
df_nonCL = df_nonCL[(df_nonCL['date'] >= pd.to_datetime('12/5/2010', format='%m/%d/%Y')) & (df_nonCL['date'] <= pd.to_datetime('12/11/2010', format='%m/%d/%Y'))]

# Get range of selected time interval.
d0, d1 = df_nonCL.date.min(), df_nonCL.date.max()
# Returns a DatetimeIndex of 30-minute frequency during the set range (summer week)
index = pd.date_range(d0, d1 + Day(1), freq='30T', inclusive='left')
# Sort nonCL customers by their IDs.
customers = sorted(df_nonCL.Customer.unique())
# Get the GG and GC consumption categories.
channels = df_nonCL['Consumption Category'].unique()
# Separates the nonCL entries according to their customer ID and consumption category.
columns1 = pd.MultiIndex.from_product((customers, channels), names=['Customer', 'Channel'])
# Create a MultiIndex object for the customer and consumption category.
empty_cols = pd.MultiIndex(
    levels=[customers, channels],
    codes=[[],[]],
    names=['Customer', 'Channel'])
# Create a multiindex dataframe.
df = pd.DataFrame(index=index, columns=columns1)
# Placeholder for data with missing information.
missing_records = []

for c in customers:
    d_c = df_nonCL[df_nonCL.Customer == c] # Get entries for that specific customer 'c'.

    for ch in channels:
        d_c_ch = d_c[d_c['Consumption Category'] == ch] # Separate the specific customer data for each consumption category.
        ts = d_c_ch.iloc[:,5:53].values.ravel() # Get the meter readings only.
        if len(ts) != len(index):
            missing_records.append((c,ch, len(ts))) # Customers with missing information.
        else:
            df[c, ch] = ts # Customers with complete information.

i = 1
for c in customers:
    pth1 = "./load_profiles/load_profile_{0}.csv".format(i) # Path for load profiles
    pth2 = "./gen_profiles/gen_profile_{0}.csv".format(i) # Path for generation profiles
    df_l = df[c, 'GC'] # Dataframe for load profiles of customer 'c'.
    df_g = df[c, 'GG'] # Dataframe for generation profiles of customer 'c'.

    #
    df_l[:] = df_l[:]*2
    df_g[:] = df_g[:]*2

    df_l.to_csv(pth1, index=False, header=False)
    df_g.to_csv(pth2, index=False, header=False)
    i += 1