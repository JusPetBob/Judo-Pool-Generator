import requests

def check(curr_ver:str) -> tuple[bool,str]:
    curr_ver = curr_ver.split(".")
    ver = curr_ver
    req = requests.get("https://api.github.com/repos/JusPetBob/Judo-Pool-Generator/releases")
    
    versions = req.json()
    
    for v in versions:
        if not v["prerelease"]:
            ver_=v["tag_name"].split(".")
            
            if int(ver_[0])>int(ver[0]):
                ver = ver_
            elif int(ver_[1])>int(ver[1]):
                ver = ver_
    
    return False if curr_ver == ver else True,".".join(ver)