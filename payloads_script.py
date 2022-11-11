import re
import copy
import sys

# ----- File Read -----
with open( sys.argv[1], "r" ) as f:
    readPayloads = f.readlines()

with open( "payloads_filter.txt", "r" ) as f:
    readFilters  = f.readlines()

# ----- Data Struct -----
filters  = []
payloads = []
for rF in readFilters:
    filters.append( "".join( re.findall( ".", rF ) ) )

for rP in readPayloads:
    payloads.append( rP.strip("\n") )

# ----- Filtering -----
category   = {}
payloadEnd = []
for filter in filters:
    payloadList = []

    for payload in payloads:
        if re.search( "([<]|[&]lt[;])/?{0}([ >/]|[&]gt[;])".format( filter ), payload, re.I ):
            payloadList.append( payload )
        else:
            payloadEnd.append( payload )
    
    if payloadEnd: 
        payloads   = copy.deepcopy( payloadEnd )
        payloadEnd = []

    category[filter] = payloadList
category["others"] = payloads


# ----- File Write -----
print( "원본: {0}개\n".format( len( readPayloads ) ) )
for key, valueList in category.items():
    data = ''
    if len( valueList ) != 0:
        print( "{0}: {1}개".format( key, len( valueList ) ) )
        with open( "payload_filtered/{0}.txt".format(key), "w" ) as f:
            for value in valueList:
                data += value + "\n"
            data.rstrip("\n")
            f.write(data)

