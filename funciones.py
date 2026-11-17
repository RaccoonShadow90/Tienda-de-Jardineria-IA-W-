from math import isfinite

from datos import categorias


def buscar_producto(productos, identificador):
    for producto in productos:
        if producto["id"] == identificador:
            return producto
    return None


def filtrar_productos(productos, criterio, valor):
    if not valor.strip():
        return [], "Introduce un valor para realizar la consulta."

    if criterio == "nombre":
        resultados = []
        for producto in productos:
            if valor.casefold() in producto["nombre"].casefold():
                resultados.append(producto)
        return resultados, ""

    if criterio == "categoria":
        resultados = []
        for producto in productos:
            if producto["categoria"].casefold() == valor.casefold():
                resultados.append(producto)
        return resultados, ""

    if criterio == "precio":
        try:
            precio_maximo = float(valor.replace(",", "."))
        except ValueError:
            return [], "El precio máximo debe ser un número."
        if not isfinite(precio_maximo) or precio_maximo < 0:
            return [], "El precio máximo debe ser un número finito mayor o igual que 0."
        resultados = []
        for producto in productos:
            if producto["precio"] <= precio_maximo:
                resultados.append(producto)
        return resultados, ""

    return [], "Selecciona un criterio válido."


def validar_producto(formulario):
    errores = []
    nombre = formulario.get("nombre", "").strip()
    categoria = formulario.get("categoria", "").strip()
    descripcion = formulario.get("descripcion", "").strip()
    precio_texto = formulario.get("precio", "").strip()
    stock_texto = formulario.get("stock", "").strip()
    precio = 0
    stock = 0

    if not nombre:
        errores.append("El nombre es obligatorio.")
    if categoria not in categorias:
        errores.append("Selecciona una categoría de la lista.")
    if not descripcion:
        errores.append("La descripción es obligatoria.")

    try:
        precio = float(precio_texto.replace(",", "."))
        if not isfinite(precio) or precio <= 0 or precio > 10000:
            errores.append("El precio debe ser mayor que 0 y no superar 10000 euros.")
        elif precio != round(precio, 2):
            errores.append("El precio puede tener como máximo dos decimales.")
    except ValueError:
        errores.append("El precio es obligatorio y debe ser un número.")

    try:
        stock = int(stock_texto)
        if stock < 0 or stock > 10000:
            errores.append("El stock debe estar entre 0 y 10000 unidades.")
    except ValueError:
        errores.append("El stock es obligatorio y debe ser un número entero.")

    producto = {"nombre": nombre, "categoria": categoria, "precio": precio,
                "stock": stock, "descripcion": descripcion}
    return producto, errores


def siguiente_id(productos):
    mayor_id = 0
    for producto in productos:
        if producto["id"] > mayor_id:
            mayor_id = producto["id"]
    return mayor_id + 1


def calcular_resumen(productos):
    total = len(productos)
    suma_precios = 0
    unidades = 0
    valor_inventario = 0
    por_categoria = {}
    for categoria in categorias:
        por_categoria[categoria] = 0
    for producto in productos:
        suma_precios += producto["precio"]
        unidades += producto["stock"]
        valor_inventario += producto["precio"] * producto["stock"]
        por_categoria[producto["categoria"]] += 1
    precio_medio = suma_precios / total if total > 0 else 0
    return {"total": total, "precio_medio": precio_medio, "unidades": unidades,
            "valor_inventario": valor_inventario, "por_categoria": por_categoria}


def productos_para_reponer(productos):
    pendientes = []
    for producto in productos:
        if producto["stock"] <= 5:
            pendientes.append(producto)
    return sorted(pendientes, key=lambda producto: producto["stock"])
