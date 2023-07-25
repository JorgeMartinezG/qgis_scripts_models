import pandas as pd
import json
import requests
from datetime import timedelta, date
from qgis import processing
from qgis.PyQt.QtCore import QVariant
from qgis.processing import alg
from qgis.core import *
from functools import reduce

"""
countries_array = {
    "ECU": "Ecuador",
    "xAC": "Aksai Chin",
    "ALB": "Albania",
    "ASM": "American Samoa (USA)",
    "AGO": "Angola",
    "ARG": "Argentina",
    "ABW": "Aruba",
    "xAP": "Arunachal Pradesh",
    "TCA": "Turks and Caicos Islands",
    "AUS": "Australia",
    "AUT": "Austria",
    "PHL": "Philippines",
    "BVT": "Bouvet Island",
    "ATA": "Antarctica",
    "AZE": "Azerbaijan",
    "NGA": "Nigeria",
    "TCD": "Chad",
    "ATG": "Antigua and Barbuda",
    "BHS": "Bahamas",
    "BHR": "Bahrain",
    "BGD": "Bangladesh",
    "FRA": "France",
    "CAF": "Central African Republic",
    "COG": "Congo",
    "BRA": "Brazil",
    "GUF": "French Guiana",
    "PYF": "Clipperton Island",
    "ATF": "Bassas da India",
    "GAB": "Gabon",
    "GMB": "Gambia",
    "GEO": "Georgia",
    "DEU": "Germany",
    "BEN": "Benin",
    "GHA": "Ghana",
    "GIB": "Gibraltar",
    "BLZ": "Belize",
    "BTN": "Bhutan",
    "BLR": "Belarus",
    "BEL": "Belgium",
    "VEN": "Venezuela",
    "BOL": "Bolivia (Plurinational State of)",
    "BIH": "Bosnia and Herzegovina",
    "BWA": "Botswana",
    "GRC": "Greece",
    "GRL": "Greenland",
    "GRD": "Grenada",
    "VGB": "British Virgin Islands",
    "COM": "Comoros",
    "IND": "India",
    "BRN": "Brunei Darussalam",
    "BGR": "Bulgaria",
    "BFA": "Burkina Faso",
    "BDI": "Burundi",
    "KHM": "Cambodia",
    "CAN": "Canada",
    "CPV": "Cape Verde",
    "CYM": "Cayman Islands",
    "CHL": "Chile",
    "xxx": "China/India",
    "CHN": "China",
    "CXR": "Christmas Island",
    "IRN": "Iran (Islamic Republic of)",
    "IRQ": "Iraq",
    "COK": "Cook Islands",
    "CRI": "Costa Rica",
    "HRV": "Croatia",
    "CYP": "Cyprus",
    "CZE": "Czechia",
    "CIV": "Côte d'Ivoire",
    "PRK": "Democratic People's Republic of Korea",
    "DNK": "Denmark",
    "DOM": "Dominican Republic",
    "SLV": "El Salvador",
    "GNQ": "Equatorial Guinea",
    "ERI": "Eritrea",
    "EST": "Estonia",
    "ETH": "Ethiopia",
    "FLK": "Falkland Islands (Malvinas)",
    "FRO": "Faroe Islands",
    "FIN": "Finland",
    "ARM": "Armenia",
    "JOR": "Jordan",
    "GUM": "Guam (USA)",
    "LBN": "Lebanon",
    "GTM": "Guatemala",
    "UMI": "Palmyra Atoll",
    "LBY": "Libya",
    "xPI": "Paracel Islands",
    "CUW": "Curaçao",
    "AND": "Andorra",
    "GNB": "Guinea-Bissau",
    "HTI": "Haiti",
    "GIN": "Guinea",
    "GUY": "Guyana",
    "HND": "Honduras",
    "xIT": "Ilemi Triangle",
    "VAT": "Holy See",
    "HUN": "Hungary",
    "ISL": "Iceland",
    "IRL": "Ireland",
    "IMN": "Isle of Man",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JPN": "Japan",
    "MHL": "Marshall Islands",
    "MTQ": "Martinique",
    "MRT": "Mauritania",
    "xJK": "Jammu and Kashmir",
    "SYR": "Syrian Arab Republic",
    "UKR": "Ukraine",
    "TUR": "Republic of Türkiye",
    "KAZ": "Kazakhstan",
    "KEN": "Kenya",
    "KIR": "Kiribati",
    "xRI": "Kuril Islands",
    "KWT": "Kuwait",
    "KGZ": "Kyrgyzstan",
    "LAO": "Lao People's Democratic Republic",
    "LVA": "Latvia",
    "LSO": "Lesotho",
    "LBR": "Liberia",
    "MUS": "Mauritius",
    "PRY": "Paraguay",
    "PER": "Peru",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "MYS": "Malaysia",
    "MDG": "Madagascar",
    "MDV": "Maldives",
    "MLI": "Mali",
    "BLM": "Saint Barthélemy",
    "MCO": "Monaco",
    "MNG": "Mongolia",
    "FSM": "Micronesia (Federated States of)",
    "MEX": "Mexico",
    "MNP": "Northern Mariana Is. (USA)",
    "NOR": "Norway",
    "OMN": "Oman",
    "PAK": "Pakistan",
    "MAR": "Morocco",
    "MOZ": "Mozambique",
    "PLW": "Palau",
    "PAN": "Panama",
    "NAM": "Namibia",
    "NRU": "Nauru",
    "NPL": "Nepal",
    "NCL": "New Caledonia",
    "NZL": "New Zealand",
    "NIC": "Nicaragua",
    "NER": "Niger",
    "NLD": "Netherlands (Kingdom of the)",
    "POL": "Poland",
    "PRT": "Madeira Islands",
    "PRI": "Puerto Rico (USA)",
    "QAT": "Qatar",
    "KOR": "Republic of Korea",
    "ROU": "Romania",
    "REU": "Réunion",
    "SPM": "Saint Pierre et Miquelon",
    "VCT": "Saint Vincent and the Grenadines",
    "LCA": "Saint Lucia",
    "WSM": "Samoa",
    "SYC": "Seychelles",
    "SLE": "Sierra Leone",
    "SGP": "Singapore",
    "SVK": "Slovakia",
    "TON": "Tonga",
    "TLS": "Timor-Leste",
    "SUR": "Suriname",
    "SJM": "Svalbard and Jan Mayen Islands",
    "xSI": "Spratly Islands",
    "LKA": "Sri Lanka",
    "TTO": "Trinidad and Tobago",
    "STP": "Sao Tome and Principe",
    "TJK": "Tajikistan",
    "SVN": "Slovenia",
    "SLB": "Solomon Islands",
    "SOM": "Somalia",
    "ZAF": "South Africa",
    "xSK": "Senkaku Islands",
    "MKD": "North Macedonia",
    "xFR": "Glorioso Islands",
    "TKM": "Turkmenistan",
    "TKL": "Tokelau",
    "TGO": "Togo",
    "SWZ": "Eswatini",
    "SWE": "Sweden",
    "CHE": "Switzerland",
    "SGS": "South Georgia and the South Sandwich Islands",
    "ESP": "Canary Islands",
    "ARE": "United Arab Emirates",
    "MLT": "Malta",
    "NFK": "Norfolk Island",
    "SAU": "Saudi Arabia",
    "xSR": "Scarborough Reef",
    "GBR": "United Kingdom of Great Britain & Northern Ireland",
    "VIR": "United States Virgin Islands (USA)",
    "USA": "United States of America",
    "URY": "Uruguay",
    "UZB": "Uzbekistan",
    "VNM": "Viet Nam",
    "ESH": "Western Sahara",
    "ZWE": "Zimbabwe",
    "IDN": "Indonesia",
    "MMR": "Myanmar",
    "PNG": "Papua New Guinea",
    "FJI": "Fiji",
    "VUT": "Vanuatu",
    "SEN": "Senegal",
    "CUB": "Cuba",
    "SDN": "Hala'ib Triangle",
    "HKG": "Hong Kong",
    "SSD": "South Sudan",
    "TWN": "Taiwan",
    "ALA": "Åland Islands",
    "BES": "Bonaire",
    "SXM": "Sint Maarten",
    "SRB": "Serbia",
    "EGY": "Bi'r Tawīl",
    "xWB": "West Bank",
    "MNE": "Montenegro",
    "PSE": "State of Palestine",
    "TUN": "Tunisia",
    "MDA": "Moldova",
    "SHN": "Saint Helena",
    "COD": "Democratic Republic of the Congo",
    "RUS": "Russian Federation",
    "COL": "Colombia",
    "RWA": "Rwanda",
    "TZA": "United Republic of Tanzania",
    "UGA": "Uganda",
    "MWI": "Malawi",
    "ZMB": "Zambia",
    "CMR": "Cameroon",
    "MAC": "Macao",
    "xGA": "Gaza",
    "DZA": "Algeria",
    "AFG": "Afghanistan",
    "YEM": "Yemen",
    "DJI": "Djibouti",
    "AIA": "Anguilla",
    "LIE": "Liechtenstein",
    "IOT": "Chagos Archipelagio",
    "DMA": "Dominica",
    "MYT": "Mayotte",
    "NIU": "Niue",
    "PCN": "Pitcairn",
    "JEY": "Jersey",
    "BRB": "Barbados",
    "THA": "Thailand",
    "SMR": "San Marino",
    "KNA": "Saint Kitts and Nevis",
    "BMU": "Bermuda",
    "CCK": "Cocos (Keeling) Islands",
    "HMD": "Heard Island and McDonald Islands",
    "MSR": "Montserrat",
    "MAF": "Saint Martin",
    "GLP": "Guadeloupe",
    "xUK": "Dekelia",
    "WLF": "Wallis and Futuna",
    "TUV": "Tuvalu",
    "xAB": "Abyei",
    "GGY": "Guernsey",
    "xJL": "Sovereignty unsettled",
}
iso3_array = list(countries_array.keys())
iso3_array.sort()
"""


def flatten_row(row):
    name = row["region"]["name"]
    date = row["date"]

    flatten_metrics = [
        {f"{metric_key}_{key}".lower(): value for key, value in values.items()}
        for metric_key, values in row["metrics"].items()
    ]
    metrics = reduce(lambda acc, item: {**acc, **item}, flatten_metrics)

    return {"name": name, "date": date, **metrics}


@alg(
    name="download_hungermap",
    label="Download data from Hungermap",
    group="risk_analysis",
    group_label="Risk analysis",
)
@alg.input(type=alg.STRING, name="ISO3", label="Country ISO3", default="COL")
@alg.input(
    type=alg.DATETIME,
    name="START_DATE",
    label="start date",
    default=(date.today() - timedelta(days=90)).isoformat(),
)
@alg.input(
    type=alg.DATETIME,
    name="END_DATE",
    label="end date",
    default=date.today().isoformat(),
)
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")
def download_hungermap(instance, parameters, context, feedback, inputs):
    """
    Download data from hunger map api.
    """
    iso3 = instance.parameterAsString(parameters, "ISO3", context)
    start_date_str = instance.parameterAsString(
        parameters, "START_DATE", context
    )
    end_date_str = instance.parameterAsString(parameters, "END_DATE", context)

    start_date = start_date_str.split("T")[0]
    end_date = end_date_str.split("T")[0]

    url = f"https://api.hungermapdata.org/v1/foodsecurity/country/{iso3}/region?date_start={start_date}&date_end={end_date}"
    resp = requests.get(url)
    resp.raise_for_status()

    rows = json.loads(resp.content.decode("utf-8"))
    data_dict = [flatten_row(r) for r in rows]

    field_names = list(data_dict[0].keys())
    qgs_fields = []

    for field_name in field_names:
        if field_name == "name":
            qgs_field = QgsField(field_name, QVariant.String)
        elif field_name == "date":
            qgs_field = QgsField(field_name, QVariant.Date)
        else:
            qgs_field = QgsField(field_name, QVariant.Double)

        qgs_fields.append(qgs_field)

    output_fields = QgsFields()
    [output_fields.append(f) for f in qgs_fields]

    (sink, dest_id) = instance.parameterAsSink(
        parameters,
        "OUTPUT",
        context,
        output_fields,
    )

    for item in data_dict:
        feature = QgsFeature()
        feature.setFields(output_fields)

        feature.setAttributes(list(item.values()))

        sink.addFeature(feature, QgsFeatureSink.FastInsert)

    return {"OUTPUT": dest_id}
