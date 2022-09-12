import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import path

path_dir = path.user_path()

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
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
    forms = get_all_forms(url)

    fname = path_dir.payload_path()
    
    with open(fname) as f:
        con = f.readlines()
    payloads = [x.strip() for x in con]

    is_vulnerable = "SAFE"
    vul = []
    count = 0
    for form in forms:
        form_details = get_form_details(form)
        for p_l in payloads:
            content = str( submit_form(form_details, url, p_l).content )
            count += 1
            print( "{0} / {1}".format( count, len( payloads ) * len( forms ) ) )

            if p_l in content:
                
                vul.append(p_l)
                is_vulnerable = "RISK"
    vull = ', '.join(s for s in vul)
    return is_vulnerable, str(vull)
