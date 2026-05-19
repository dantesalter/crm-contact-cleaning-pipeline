import pandas as pd

#Reading files and creating DataFrames
df2 = pd.read_csv("C:\\Users\\dante\\Downloads\\contacts - contacts.csv")

#Creating Phone Other column in df2
df2.insert(6,'Phone Other', '') # adding 'phone other' column to dataframe.

# Renaming Columns in df2
df2 = df2.rename(columns={'E-mail 1 - Value': 'Email', 'Phone 1 - Value': 'Phone'})

#------------------------------------------------------------------------------\
# Domain to Organization Directory for domains with count >= 3
domain_to_org = {
    'jordanskala.com': 'Jordan & Skala Engineers',
    'southernco.com': 'Southern Company',
    'att.com': 'AT&T',
    'duke-energy.com': 'Duke Energy',
    'nwravin.com': 'Northwood Ravin',
    'zayo.com': 'Zayo Group',
    'quiktrip.com': 'QuikTrip',
    'charter.com': 'Charter Communications (Spectrum)',
    'fortune-johnson.com': 'Fortune-Johnson LLC',
    'atlantaga.gov': 'City of Atlanta',
    'westplan.com': 'Westplan Investors',
    'bradenfellman.com': 'Braden Fellman Group',
    'fpl.com': 'Florida Power & Light',
    'tcco.com': 'Turner Construction',
    'kimley-horn.com': 'Kimley-Horn',
    'comcast.com': 'Comcast',
    'portmanresidential.com': 'Portman Holdings',
    'juneaucc.com': 'Juneau Construction Company',
    'pike.com': 'Pike Corporation',
    'verizonwireless.com': 'Verizon',
    'mcrtrust.com': 'Mill Creek Residential',
    'broadbandplanning.com': 'Broadband Planning',
    'anywair.com': 'anywAIR',
    'allenmorris.com': 'Allen Morris'
    }
#------------------------------------------------------------------------------
# defining pipeline functions

def normalize_email(s):
    return s.str.strip().str.lower()

def normalize_phone(p):
    return (p.str.replace(r'\D', '', regex=True) # removes all non-digits
     .str.replace(r'^1(\d{10})$', r'\1', regex=True)) # removes leading 1

def normalize_firstname(fn):
    return fn.str.strip().str.title()

def normalize_lastname(ln):
    return ln.str.strip().str.title()

def domain_extract(e):
    return e.str.split('@').str[-1]
    # Must use an email for proper extraction
#------------------------------------------------------------------------------

# Changing Email to First Name containing Email
df2.loc[df2['First Name'].str.contains('@', na=False),'Email'] = df2['First Name']

# Name Corrections
df2.loc[4, 'Last Name'] = 'delcheccolo' # adding last name to amy in df2
df2.loc[199, 'First Name'] = 'Michael L' # Inserting Michael in First Name at 199
df2.loc[199, 'Last Name'] = 'Thomas' # Inserting Thomas in Last Name at 199
df2.loc[11, 'First Name'] = 'Ashley' # Correcting Ashley's name
df2.loc[[32,104,131,155,177,181,253,295], 'Last Name'] = ['Pait', # Filling in bulk nan last names
                                                      'Brock','Holmes',
                                                      'Culver','Brambut',
                                                      'Dooly','Croft',
                                                      'Niedermeier']

# Normalization and Cleaning
df2['Email'] = normalize_email(df2['Email']) # normalizing emails
df2['Phone'] = normalize_phone(df2['Phone']) # normalizing phone numbers
df2['First Name'] = normalize_firstname(df2['First Name']) # normalizing first names
df2['Last Name'] = normalize_lastname(df2['Last Name']) # normalizing last names

df2.loc[df2['Phone'].str.len() > 11,] # locating invalid length phone numbers
value = df2.loc[197,'Phone'] # getting the value for the combined phone numbers
df2.loc[197, 'Phone'] = value[:10] # setting first phone number into the Phone column
df2.loc[197,'Phone Other'] = value[10:] # setting second phone number into Phone Other column
df2.loc[263, 'Organization Name'] = 'ElectriCities'
phones_formatted = ('(' + df2['Phone'].str[:3] + ')' + # Formatting Phone to proper
                    df2['Phone'].str[3:6] + '-' + df2['Phone'].str[6:]) # Formatting Phone to proper

phones_other_formatted = ('(' + df2['Phone Other'].str[:3] + ')' + # Formatting Phone Other to proper
                          df2['Phone Other'].str[3:6] + '-' + df2['Phone Other'].str[6:]) # Formatting Phone to proper

df2['Phone'] = phones_formatted # Changing Phone to formatted
df2['Phone Other'] = phones_other_formatted # Changing Phone Other to formatted
df2['Phone Other'] = df2['Phone Other'].str.replace('()-','') # Replacing empty formatted numbers with ''


domains = domain_extract(df2['Email']) # Extracting the domains from email in df2
domains_formatted = 'Other (Check Domain)' # Formatting the domains for org name column

df2['Organization Name'] = (domains.map(domain_to_org) # Mapping the org dict to rows in org name column
                           .fillna(df2['Organization Name']) # keeping org name if value still null
                           .fillna(domains_formatted)) # Filling whats left with formatted domains
df2['domains'] = domains
#df2.to_excel("C:\\Users\\dante\\Downloads\\Contacts_Clean_Dashboard.xlsx", index = False)


#-----------------------------------------------------------------------------
# MASKING REAL DATA WITH FAKE DATA TO PRESERVE CONFIDENTIALITY


from faker import Faker

df_public = df2.copy()

fake = Faker()

df_public['First Name'] = [
    fake.first_name() for _ in range(len(df_public))
]

df_public['Last Name'] = [
    fake.last_name() for _ in range(len(df_public))
]

df_public['Email'] = [
    fake.email() for _ in range(len(df_public))]

domains = df_public['domains']

df_public['Email'] = [
    f"{fake.user_name()}@{domain}"
    for domain in domains
]

    
df_public['Phone Other'] = [
    fake.numerify(text='(###)###-####')
    for _ in range(len(df_public))
]

df_public['Phone'] = [
    fake.numerify(text='(###)###-####')
    for _ in range(len(df_public))
]