import os, traceback, requests, yaml, wget
import modules.gui as gui

wget = "wget -nv -P downloads --content-disposition"

manual = {}
skipped = []

def up_to_date(data, p, latest):
    return False # for debug purposes
    if p in data and "version" in data[p] and data[p]["version"] == latest:
        gui.task("download skipped, already up to date!",1)
        skipped.append(p)
        return True

# actual update script, iterates through assets discriminantly based off source
# to get a better idea of each source refer to /configs/sample_list.yaml
def update(yml:dict, data:dict):
    manual = {}
    skipped = []

    for p, pp in yml['assets'].items():
        gui.text(f"downloading {p} via {pp['source']}...",pre="\n")
        try:

            if pp["source"] == "modrinth":
                gui.text("sending request ...",1)
                req = requests.get("https://api.modrinth.com/v2/project/{}/version".format(pp["id"])).json()
                gui.text("processing response ...",1)
                if len(req) == 1: # if only 1 version file exists, select it
                    req = req[0]
                else:
                    for v in req:
                        if any(i in v["loaders"] for i in list(yml["loaders"])): # match loader type
                            req = v
                            break
                if up_to_date(data, p, req["version_number"]):
                    continue
                gui.task(f"downloading latest file ... [{data[p]['version'] if p in data else 'n/a'} -> {req['version_number']}]",1)

                os.system(f'{wget} {req["files"][0]["url"]}')
                data.update({p:{"version":req["version_number"]}})
            
            elif pp["source"] == "spigot":
                gui.text("sending request ...",1)
                req = requests.get("https://api.spiget.org/v2/resources/{}/".format(pp["id"])).json()
                gui.text("processing response ...",1)
                if up_to_date(data, p, req["version"]["id"]):
                    continue
                if req["file"]["type"] == "external": 
                    gui.task(f"downloading external file via {req['file']['externalUrl']} ... [{data[p]['version'] if p in data else 'n/a'} -> {req['version']['id']}]",1)
                    os.system(f'{wget} {req["file"]["externalUrl"]}')
                else:
                    gui.info(f"proxy url added to list",1)
                    manual[p] = "https://spigotmc.org/"+req["file"]["url"]
                data.update({p:{"version":req["version"]["id"]}})
            
            elif pp["source"] == "github":
                gui.text("sending request ...",1)
                req = requests.get("https://api.github.com/repos/{}/releases/latest".format(pp["id"])).json()
                gui.text("processing response ...",1)
                if up_to_date(data, p, req["id"]):
                    continue
                gui.task(f"downloading latest release file ... []",1)
                os.system(f'{wget} {req["assets"][0]["browser_download_url"]}')
                data.update({p:{"version":req["id"]}})
            
            elif pp["source"] == "curse":
                gui.task(f"downloading latest file ...",1)
                os.system(f'{wget} http://dev.bukkit.org/projects/{pp["id"]}/files/latest')

            elif pp["source"] == "permalink":
                gui.task(f"downloading file from static url ...",1)
                os.system(f'{wget} {pp["id"]}')
            
            elif pp["source"] == "manual":
                gui.info(f"manual url added to list",1)
                manual[p] = "https://"+pp["id"]
            else:
                gui.warn(f"indiscriminant source; typo maybe? ({pp['source']})")
        except Exception as error:
            print(''.join(traceback.format_exception(type(error), error, error.__traceback__))) # makes errors more readable

    if skipped:
        gui.info("the following are already up to date and were skipped:",pre="\n")
        print('      '+', '.join(skipped))
    if manual:
        gui.info("the following must be installed manually:",pre="\n")
        for p, url in manual.items():
            print(f"    - {p} @ {url}")

    print("")

    with open("configs/data.yml",'w') as data_file:
        yaml.safe_dump(data, data_file, sort_keys=True)