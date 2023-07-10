import toml, glob, jinja2
import pandas as pd
from pprint import pprint as print
from astropy import units as u
from astropy.coordinates import SkyCoord
import numpy as np

make_html = True #if True, will save gbt820.html
make_csv = True #if True, will save gbt820.csv
make_tex = False #if True, will save gbt820.tex

##########
#Make catalog table
##########

#These two get displayed in the HTML file
header_keys = ["Name", "Period", "DM", "Single Pulse", "Discovered by", "Search Type"]
units = [" ", "ms", "pc cm^-3", " ", " ", " "]

#Key names in the TOML files
table_keys = ["Name", "Period", "DM", "SinglePulse", "Discovery", "Search"]
df_keys = table_keys + [x+"_ref" for x in table_keys]

unit_keys=[]
for i in range(len(header_keys)):
    if len(units[i]) > 1:
        unit_keys.append(header_keys[i] + '   (' + units[i] + ')')
    else:
        unit_keys.append(header_keys[i])


if __name__ == "__main__":
    psr_list = glob.glob("J*.toml")
    psr_list.sort()
    display_dict = {}
    psr_dict = {}

    for key in df_keys:
        display_dict[key] = []
        psr_dict[key] = []


    full_display_df = pd.DataFrame(psr_dict)
    #print(full_display_df.columns)

    for psr in psr_list:
        display_dict={}
        for key in table_keys:
            display_dict[key] = []
            display_dict[key+"_ref"] = []
        try:
            psr_toml = toml.load(psr)

            for key in table_keys:
                if "value" in psr_toml[key]:
                    display_dict[key].append(str(psr_toml[key]["value"]))
                    if "ref" in psr_toml[key] and len(str(psr_toml[key]["ref"])) > 0:
                        display_dict[key+"_ref"].append(psr_toml[key]["ref"])
                    else:
                        display_dict[key + "_ref"].append('--')

                else:
                    display_dict[key].append('--')
                    display_dict[key + "_ref"].append('--')


            display_df = pd.DataFrame(display_dict)
            full_display_df = pd.concat([full_display_df,display_df],ignore_index=True)

        except toml.decoder.TomlDecodeError as exc:
            print(psr)
            print(exc)
            pass

    #print(full_display_df)

##########
#Output
##########

    if make_csv==True:
        full_display_df.to_csv('gbt820.csv',columns=df_keys)

    if make_html==True:
        templateLoader = jinja2.FileSystemLoader(searchpath='./')
        env = jinja2.Environment(loader=templateLoader,trim_blocks=True,lstrip_blocks=True)
        template = env.get_template('template.html')
        with open("gbt820.html", "w") as fh:
            out = template.render(header=unit_keys, tableinfo=table_keys, df=full_display_df)
            fh.write(out)

    if make_tex==True:
        full_display_df.to_latex(buf='gbt820.tex',index=False)
