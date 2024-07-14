import os

# 
capital_range = [{"range_name": "small cap", "lower": 250000000, "upper": 2000000000},
                 {"range_name": "mid cap", "lower": 2000000000, "upper": 10000000000},
                 {"range_name": "large cap", "lower": 10000000000, "upper": 200000000000},
                 {"range_name": "mega cap", "lower": 200000000000, "upper": 20000000000000000}
                ]

sector_list = ['Consumer Defensive', 'Financial Services', 'Healthcare', 'Industrials', 'Technology', 'Basic Materials', 'Communication Services', 'Consumer Cyclical', 'Energy', 'Utilities', 'Real Estate']
                 

sector_list_ticker_etf = ["XLC", "XLY", "XLP", "XLE", "XLF", "XLV", "XLI", "XLB", "XLRE", "XLK", "XLU"]

industry_list = {
   "Consumer Defensive":[
      "Education & Training Services",
      "Farm Products",
      "Packaged Foods",
      "Food Distribution",
      "Beverages - Non-Alcoholic",
      "Discount Stores",
      "Household & Personal Products",
      "Grocery Stores",
      "Beverages - Wineries & Distilleries",
      "Tobacco",
      "Confectioners",
      "Beverages—Wineries & Distilleries",
      "Beverages—Non-Alcoholic"
   ],
   "Financial Services":[
      "Shell Companies",
      "Insurance - Life",
      "Banks - Regional",
      "Capital Markets",
      "Insurance - Diversified",
      "Insurance - Property & Casualty",
      "Insurance - Specialty",
      "Asset Management",
      "Credit Services",
      "Mortgage Finance",
      "Insurance Brokers",
      "Financial Data & Stock Exchanges",
      "Banks—Regional",
      "Insurance—Reinsurance",
      "Insurance—Diversified",
      "Insurance—Specialty",
      "Insurance—Property & Casualty",
      "Financial Conglomerates"
   ],
   "Healthcare":[
      "Biotechnology",
      "Drug Manufacturers - Specialty & Generic",
      "Health Information Services",
      "Medical Care Facilities",
      "Diagnostics & Research",
      "Medical Devices",
      "Medical Distribution",
      "Medical Instruments & Supplies",
      "Healthcare Plans",
      "Drug Manufacturers - General",
      "Pharmaceutical Retailers",
      "Drug Manufacturers—Specialty & Generic",
      "Drug Manufacturers—General"
   ],
   "Industrials":[
      "Airlines",
      "Building Products & Equipment",
      "Business Equipment & Supplies",
      "Staffing & Employment Services",
      "Electrical Equipment & Parts",
      "Consulting Services",
      "Farm & Heavy Construction Machinery",
      "Conglomerates",
      "Specialty Industrial Machinery",
      "Waste Management",
      "Trucking",
      "Pollution & Treatment Controls",
      "Airports & Air Services",
      "Aerospace & Defense",
      "Integrated Freight & Logistics",
      "Security & Protection Services",
      "Engineering & Construction",
      "Industrial Distribution",
      "Marine Shipping",
      "Rental & Leasing Services",
      "Specialty Business Services",
      "Metal Fabrication",
      "Railroads",
      "Tools & Accessories",
      "Infrastructure Operations"
   ],
   "Technology":[
      "Communication Equipment",
      "Consumer Electronics",
      "Software - Infrastructure",
      "Semiconductor Equipment & Materials",
      "Software - Application",
      "Semiconductors",
      "Computer Hardware",
      "Electronic Components",
      "Information Technology Services",
      "Solar",
      "Electronics & Computer Distribution",
      "Scientific & Technical Instruments",
      "Software—Application",
      "Software—Infrastructure"
   ],
   "Basic Materials":[
      "Other Industrial Metals & Mining",
      "Steel",
      "Specialty Chemicals",
      "Coking Coal",
      "Chemicals",
      "Other Precious Metals & Mining",
      "Agricultural Inputs",
      "Aluminum",
      "Gold",
      "Lumber & Wood Production",
      "Paper & Paper Products",
      "Building Materials"
   ],
   "Communication Services":[
      "Advertising Agencies",
      "Entertainment",
      "Internet Content & Information",
      "Telecom Services",
      "Broadcasting",
      "Electronic Gaming & Multimedia",
      "Publishing"
   ],
   "Consumer Cyclical":[
      "Travel Services",
      "Auto & Truck Dealerships",
      "Auto Manufacturers",
      "Furnishings, Fixtures & Appliances",
      "Internet Retail",
      "Leisure",
      "Footwear & Accessories",
      "Home Improvement Retail",
      "Specialty Retail",
      "Restaurants",
      "Lodging",
      "Apparel Retail",
      "Gambling",
      "Luxury Goods",
      "Auto Parts",
      "Resorts & Casinos",
      "Apparel Manufacturing",
      "Residential Construction",
      "Recreational Vehicles",
      "Textile Manufacturing",
      "Personal Services",
      "Packaging & Containers"
   ],
   "Energy":[
      "Oil & Gas Equipment & Services",
      "Oil & Gas Refining & Marketing",
      "Oil & Gas E&P",
      "Thermal Coal",
      "Oil & Gas Midstream",
      "Uranium",
      "Oil & Gas Drilling",
      "Oil & Gas Integrated"
   ],
   "Utilities":[
      "Utilities - Renewable",
      "Utilities - Regulated Electric",
      "Utilities - Regulated Water",
      "Utilities—Regulated Water",
      "Utilities—Renewable",
      "Utilities - Diversified",
      "Utilities - Regulated Gas",
      "Utilities—Diversified",
      "Utilities—Regulated Gas",
      "Utilities—Regulated Electric"
   ],
   "Real Estate":[
      "Real Estate - Development",
      "REIT - Specialty",
      "REIT - Mortgage",
      "Real Estate Services",
      "Real Estate - Diversified",
      "REIT - Office",
      "REIT - Healthcare Facilities",
      "REIT—Diversified",
      "REIT—Specialty",
      "REIT—Hotel & Motel",
      "REIT—Healthcare Facilities",
      "REIT—Industrial",
      "Real Estate—Development",
      "REIT—Mortgage",
      "REIT—Office",
      "REIT—Retail",
      "REIT - Hotel & Motel",
      "REIT - Diversified",
      "Real Estate—Diversified"
   ]
}

# Set environment variables
os.environ["DATABASE_URL"] = "mongodb://localhost:27017/"
os.environ["FTP_SERVER"] = "ftp.nasdaqtrader.com"
os.environ["SAVE_PATH"] = "./tickers/ticker_table"
os.environ["TARGET_PATH"] = "./tickers/ticker_table/nasdaqlisted.txt"
os.environ["sector_list_etf"] = ','.join(sector_list_ticker_etf)
os.environ["capital_range"] = str(capital_range)
os.environ["sector_list"] = str(sector_list)
os.environ["industry_list"] = str(industry_list)
