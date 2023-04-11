prefix = {
    "text": "---",
    "info": "<i>",
    "task": "(@)",
    "warn": "[!]",
}

def gui_print(txt, d:int, pre, f):
    print(f"{pre}{d*'    '}{prefix[f]} {txt}")

# these are cosmetic yes this is stupid idc
def text(txt, d=0, pre=""): gui_print(txt, d, pre, "text")
def info(txt, d=0, pre=""): gui_print(txt, d, pre, "info")
def task(txt, d=0, pre=""): gui_print(txt, d, pre, "task")
def warn(txt, d=0, pre=""): gui_print(txt, d, pre, "warn")

def options(items, intxt="> "):
    txt = "\n".join([f"    [{items.index(i)}] {i}" for i in items if i])
    print(txt)
    err = True
    while err:
        ii = input(intxt)
        if f"[{ii}]" in txt:
            return int(ii)
        warn("please provide a valid option!")