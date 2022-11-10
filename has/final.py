import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import path

path_dir = path.user_path()

def get_all_forms(url):
    res = requests.get( url )
    soup = bs( res.content, "html.parser" ) if res.status_code == 200 else "<form>SITE IS NOT AVAILABLE</form>"

    return soup.find_all("form")
    


def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()

    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    #print( "action: {0}\nmethod: {1}\ninputs: {2}".format( details[ "action" ], details[ "method" ], details[ "inputs" ] ) )
    return details


def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value
        return requests.get(target_url, params=data)

def scan_xss(url):
    forms  = get_all_forms(url)
    fnames = path_dir.payload_path()
    tags   = path_dir.get_files()
    ToFrontData = { "Tags":[], "RiskPayloads":[], "CntRisk":[], "CntTotal":[] }
    
    for fname, file in zip( fnames, tags ):
        with open(fname) as f:       # get payload: ex)payload.txt
            con = f.readlines()
        payloads = [x.strip() for x in con]

        is_vulnerable = "SAFE"
        msg = ''
        vul = []     # (RISK) payloads
        count   = 0
        riskCnt = 0
        safeCnt = 0

        for form in forms:
            form_details = get_form_details(form)
            for p_l in payloads:
                content = str( submit_form(form_details, url, p_l).content )
                count += 1

                if p_l in content:
                    riskCnt += 1
                    msg = "RISK"
                    vul.append(p_l)
                    is_vulnerable = "RISK"
                else:
                    msg = "SAFE"
                    safeCnt += 1
                
                print( "{0} / {1}: ({2}) {3}".format( count, len( payloads ) * len( forms ), msg, p_l ) )

        ToFrontData[ 'Tags' ].append(file[:-4])
        ToFrontData[ 'RiskPayloads' ].append( vul )
        ToFrontData[ 'CntRisk' ].append( riskCnt )
        ToFrontData[ 'CntTotal' ].append( len( payloads ) * len( forms ) )

        print( "tag: {0}\nTOTAL: {1}\nRISK: {2}\nSAFE: {3}\n\n".format( file[:-4] ,len( payloads ) * len( forms ), riskCnt, safeCnt ) )

    print( ToFrontData )
    vull = '\n'.join(s for s in vul)
    return is_vulnerable, str(vull)
