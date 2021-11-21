#Tests incrementales
from parser_meta import parser

def test_correct_metadata():
    meta ='''
    [prueba "loca"]
    [Nzscf5qWgtg~NVX "56B~n~nQIeAhy"]
    [gvk7dX-kliRpR "2LAkQJGhz81"]
    [~NFS-5lBHW4Mm~NmJsP "e4ZhVulzl"]
    [yZ1PSI4r78KP "XwWzscEtUqkAu~nNt7Hq5"]
    [GArzOdNa~nITcsbFO9ES "WUodxeqxI"]
    '''.split("\n")
    for metaData in meta:
       parser.parse(metaData)
