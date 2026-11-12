# envios.py
CONFIG = {
    "L1": 4,               # <- pon tus valores
    "L2": 10,
    "RECARGO_RURAL": 0.20,    # como fracción, ej. 0.15
    "RECARGO_NACIONAL": 0.40,
    "DESC_VIP": 0.20,
    "RECARGO_FINDE": 2000,    # en pesos
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 40:
        raise ValueError("peso inválido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    # fin de semana
    if d == 6 or d == 7:
        t = t + CONFIG["RECARGO_FINDE"]
    desc = 0
    if c == "frecuente":
        desc = 0.05
    if c == "vip":
        desc = CONFIG["DESC_VIP"]
    if cup == "ENVIO10":
        desc = max(desc, 0.10)
    t = t - t * desc
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(t / 100) * 100