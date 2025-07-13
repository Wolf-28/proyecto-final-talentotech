#Proyecto Pre Entrega
import os
import sqlite3

def inicio():
    if crearTabla()==True:
        print("Tabla 'productos' existente\n")
    else:
        print("Error en la Base de Datos")
        return 0
    print("~~~~~~~~~~ BIENVENIDO ~~~~~~~~~~\n")
    volverMenu = True
    while volverMenu == True:
        entrada = menu()
        os.system('cls')
        match entrada:
            case 1: #Agregar nuevos productos a la tabla
                flag1 = True
                while flag1 == True:
                    producto = datosNuevoProducto()
                    try:
                        conexion = sqlite3.connect("inventario.db")
                        conexion.execute("BEGIN TRANSACTION")
                        conexion.execute('''
                            INSERT INTO productos (
                                nombre, descripcion, cantidad, precio, categoria) VALUES (?,?,?,?,?)
                            ''',(producto[0],producto[1],producto[2],producto[3],producto[4]))
                        conexion.commit()
                        os.system('cls')
                        print("Producto ingresado a la tabla correctamente\n")
                    except sqlite3.Error:
                        print("Ocurrio un error en el ingreso del producto a la tabla\n")
                        conexion.rollback()
                    finally:
                        conexion.close()
                    flag2 = True
                    while flag2 == True:
                        volver = input("¿Desea ingresar otro producto?\n1. Si\n2. No\nOpcion: ")
                        match volver:
                            case "1": 
                                os.system('cls')
                                print("Ingrese los datos del nuevo producto:")
                                flag2 = False
                            case "2":
                                flag2 = False
                                flag1 = False
                                os.system('cls')
                            case _:
                                os.system('cls')
                                print("Opcion incorrecta. Vuelva a intentarlo.\n")
            case 2: #Visualizar datos de los productos registrados en la tabla
                try:
                    conexion = sqlite3.connect("inventario.db")
                    cursor = conexion.cursor()
                    cursor.execute("BEGIN TRANSACTION")
                    cursor.execute("SELECT * FROM productos")
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"ID: {producto[0]} | Nombre: {producto[1]}\nDescripción: {producto[2]}\nCantidad: {producto[3]} | Precio unitario: ${producto[4]:.2f}\nCategoria: {producto[5]}\n")
                    conexion.commit()
                    if productos == []:
                        print("La tabla está vacía\n")
                except sqlite3.Error:
                    print("Ocurrio un error con la visualización de la base de datos")
                    conexion.rollback()
                finally:
                    conexion.close()
            case 3: #Actualizar datos de un producto existente mediante ID
                flag1=True
                while flag1==True:
                    id = input("Ingrese ID del producto: ")
                    if validarInt(id) == True and validarVacio(id) == True:
                        id=int(id)
                        flag1=False
                    else:
                        os.system('cls')
                        print("Error en el dato ingresado. Vuelva a intentarlo\n")
                    os.system('cls')
                if visualizarID(id) == True:
                    flag1 = True
                    while flag1:
                        cambio = input("Ingrese opción numérica:\n1. Modificar nombre\n2. Modificar descripción\n3. Modificar cantidad\n4. Modificar precio\n5. Modificar categoria\n\nOpcion: ")
                        if validarInt(cambio) == True and validarVacio(cambio) == True:
                            cambio=int(cambio)
                            if (cambio < 1) or (cambio > 5):
                                os.system('cls')
                                print("La opción elegida no es válida. Intente nuevamente\n")
                            else:
                                os.system('cls')
                                modificarProducto(cambio,id)
                                flag1=False
                        else:
                            os.system('cls')
                            print("Error en el dato ingresado. Vuelva a intentarlo\n")
            case 4: #Eliminar producto mediante ID
                flag1=True
                while flag1==True:
                    id = input("Ingrese ID del producto: ")
                    if validarInt(id) == True and validarVacio(id) == True:
                        id=int(id)
                        flag1=False
                    else:
                        os.system('cls')
                        print("Error en el dato ingresado. Vuelva a intentarlo\n")
                os.system('cls')
                if visualizarID(id) == True:
                    flag1 = True
                    while flag1:
                        eliminar = input("Ingrese opción numérica.\n¿Desea eliminar producto encontrado?\n1. Si\n2. No\n\nOpción: ")
                        match eliminar:
                            case "1":
                                try:
                                    conexion = sqlite3.connect("inventario.db")
                                    conexion.execute("BEGIN TRANSACTION")
                                    conexion.execute("DELETE FROM productos WHERE id=?",(id,))
                                    os.system('cls')
                                    print(f"Producto ID: {id} eliminado exitosamente\n")
                                    conexion.commit()
                                except sqlite3.Error:
                                    os.system('cls')
                                    print("Ocurrio un error con la eliminación del producto de la base de datos")
                                    conexion.rollback()
                                finally:
                                    conexion.close()
                                flag1 = False
                            case "2":
                                flag1 = False
                                os.system('cls')
                            case _:
                                os.system('cls')
                                print("Error en la opción ingresada, vuelva a intentarlo.\n")
            case 5: #Buscar un producto mediante ID
                flag1=True
                while flag1==True:
                    id = input("Ingrese ID del producto: ")
                    if validarInt(id) == True and validarVacio(id) == True:
                        id=int(id)
                        flag1=False
                    else:
                        os.system('cls')
                        print("Error en el dato ingresado. Vuelva a intentarlo\n")
                    os.system('cls')
                visualizarID(id)
            case 6: #Ver productos que tengan cantidad menor a límite específico
                flag1 = True
                while flag1:
                    limite = input("Ingrese la cantidad límite que deben tener los productos a mostrar: ")
                    os.system('cls')
                    if (validarInt(limite) == True) and (validarVacio(limite) == True):
                        flag1 = False
                    else:
                        os.system('cls')
                        print("Error en el dato ingresado. Vuelva a intentarlo\n")
                try:
                    conexion = sqlite3.connect("inventario.db")
                    cursor = conexion.cursor()
                    cursor.execute("BEGIN TRANSACTION")
                    cursor.execute("SELECT * FROM productos WHERE cantidad<=?",(limite,))
                    productos = cursor.fetchall()
                    for producto in productos:
                        print(f"ID: {producto[0]} | Nombre: {producto[1]}\nDescripción: {producto[2]}\nCantidad: {producto[3]} | Precio unitario: ${producto[4]:.2f}\nCategoria: {producto[5]}\n")
                    conexion.commit()
                    if productos == []:
                        print("No hay productos con cantidad igual o menor al límite especificado\n")
                except sqlite3.Error:
                    print("Ocurrio un error con la visualización de los productos.")
                    conexion.rollback()
                except IndexError:
                    print(f"Producto con ID: {id} inexistente\n")
                finally:
                    conexion.close()
            case 7:
                print("Fin de programa. Muchas gracias!")
        if entrada == 7:
            break
        volverMenu = volverInicio()



def crearTabla():
    try:
        conexion = sqlite3.connect("inventario.db")
        conexion.execute("BEGIN TRANSACTION")
        conexion.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT NOT NULL)
        ''')
        conexion.commit()
        conexion.close()
        return True
    except:
        print("Ocurrio un error con la creación de la tabla")
        conexion.rollback()
        conexion.close()
        return False


def menu():
    while True:
        print("Seleccione opción según número.\n")
        print("1. Agregar nuevos productos a la tabla")
        print("2. Visualizar datos de los productos registrados en la tabla")
        print("3. Actualizar datos de un producto existente mediante ID")
        print("4. Eliminar producto mediante ID")
        print("5. Buscar un producto mediante ID")
        print("6. Ver productos que tengan cantidad menor a límite específico")
        print("7. Salir")
        opcion = input("\nOpción: ")
        if (validar_num(opcion) == True):
            opcion = int(opcion)
            if (opcion < 1) or (opcion > 7):
                os.system('cls')
                print("La opción elegida no es válida. Intente nuevamente\n")
            else:
                break
        else:
            os.system('cls')
            print("La opción elegida no es válida. Intente nuevamente\n")
    return opcion
def validar_num(valor):
    try:
        entero = int(valor)
        return True
    except:
        return False
    menu()

def datosNuevoProducto():
    flag = True
    while flag == True: #Nombre
        nombre = input("Ingrese nombre del producto: ")
        if (validarStr(nombre) == True) and (validarVacio(nombre) == True):
            flag = False
        else:
            os.system('cls')
            print("Error en el dato ingresado. Vuelva a intentarlo\n")
    flag = True
    while flag: #descripcion
        descripcion = input("Ingrese breve descripción del producto: ")
        if (validarStr(descripcion) == True) and (validarVacio(descripcion) == True):
            flag = False
        else:
            os.system('cls')
            print("Error en el dato ingresado. Vuelva a intentarlo\n")
    flag = True
    while flag: #cantidad
        cantidad = input("Ingrese cantidad del producto: ")
        if (validarInt(cantidad) == True) and (validarVacio(cantidad) == True):
            flag = False
        else:
            os.system('cls')
            print("Error en el dato ingresado. Vuelva a intentarlo\n")
    flag = True
    while flag: #precio
        precio = input("Ingrese precio unitario del producto: ")
        if (validarReal(precio) == True) and (validarVacio(precio) == True):
            flag = False
        else:
            os.system('cls')
            print("Error en el dato ingresado. Vuelva a intentarlo\n")
    flag = True
    while flag: #categria
        categoria = input("Ingrese categoria del producto: ")
        if (validarStr(categoria) == True) and (validarVacio(categoria) == True):
            flag = False
        else:
            os.system('cls')
            print("Error en el dato ingresado. Vuelva a intentarlo\n")
    return nombre.capitalize(), descripcion.capitalize(), cantidad, precio, categoria.capitalize()
def visualizarID(id):
    try:
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("SELECT * FROM productos WHERE id=?",(id,))
        producto = cursor.fetchall()[0]
        print(f"Producto ID: {id} encontrado:\n\nNombre: {producto[1]} | Descripción: {producto[2]}\nCantidad: {producto[3]} | Precio: ${producto[4]:.2f}\nCategoría: {producto[5]}\n")
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error:
        print("Ocurrio un error con la visualización del producto.")
        conexion.rollback()
        conexion.close()
        return False
    except IndexError:
        print(f"Producto con ID: {id} inexistente\n")
        conexion.close()
        return False

def modificarProducto(cambio,id):
    match cambio:
        case 1: #nombre
            flag = True
            while flag == True: 
                nombre = input("Ingrese nuevo nombre del producto: ")
                if (validarStr(nombre) == True) and (validarVacio(nombre) == True):
                    flag = False
                else:
                    os.system('cls')
                    print("Error en el dato ingresado. Vuelva a intentarlo\n")
            try:
                conexion = sqlite3.connect("inventario.db")
                conexion.execute("BEGIN TRANSACTION")
                conexion.execute("UPDATE productos SET nombre = ? WHERE id = ?",(nombre,id))
                conexion.commit()
                os.system('cls')
                print("Nombre del producto modificado correctamente\n")
            except sqlite3.Error:
                os.system('cls')
                print("Ocurrio un error en la modificación solicitada\n")
                conexion.rollback()
            finally:
                conexion.close()
        case 2: #descripción
            flag = True
            while flag == True: 
                descripcion = input("Ingrese nueva descripción del producto: ")
                if (validarStr(descripcion) == True) and (validarVacio(descripcion) == True):
                    flag = False
                else:
                    os.system('cls')
                    print("Error en el dato ingresado. Vuelva a intentarlo\n")
            try:
                conexion = sqlite3.connect("inventario.db")
                conexion.execute("BEGIN TRANSACTION")
                conexion.execute("UPDATE productos SET descripcion = ? WHERE id = ?",(descripcion,id))
                conexion.commit()
                os.system('cls')
                print("Descripción del producto modificado correctamente\n")
            except sqlite3.Error:
                os.system('cls')
                print("Ocurrio un error en la modificación solicitada\n")
                conexion.rollback()
            finally:
                conexion.close()
        case 3: #cantidad
            flag = True
            while flag == True: 
                cantidad = input("Ingrese nueva cantidad del producto: ")
                if (validarInt(cantidad) == True) and (validarVacio(cantidad) == True):
                    flag = False
                else:
                    os.system('cls')
                    print("Error en el dato ingresado. Vuelva a intentarlo\n")
            try:
                conexion = sqlite3.connect("inventario.db")
                conexion.execute("BEGIN TRANSACTION")
                conexion.execute("UPDATE productos SET cantidad = ? WHERE id = ?",(cantidad,id))
                conexion.commit()
                os.system('cls')
                print("Cantidad del producto modificado correctamente\n")
            except sqlite3.Error:
                os.system('cls')
                print("Ocurrio un error en la modificación solicitada\n")
                conexion.rollback()
            finally:
                conexion.close()
        case 4: #precio
            flag = True
            while flag: 
                precio = input("Ingrese nuevo precio unitario del producto: ")
                if (validarReal(precio) == True) and (validarVacio(precio) == True):
                    flag = False
                else:
                    os.system('cls')
                    print("Error en el dato ingresado. Vuelva a intentarlo\n")
            try:
                conexion = sqlite3.connect("inventario.db")
                conexion.execute("BEGIN TRANSACTION")
                conexion.execute("UPDATE productos SET precio = ? WHERE id = ?",(precio,id))
                conexion.commit()
                os.system('cls')
                print("Precio del producto modificado correctamente\n")
            except sqlite3.Error:
                os.system('cls')
                print("Ocurrio un error en la modificación solicitada\n")
                conexion.rollback()
            finally:
                conexion.close()
        case 5: #categoria
            flag = True
            while flag: #categria
                categoria = input("Ingrese nueva categoria del producto: ")
                if (validarStr(categoria) == True) and (validarVacio(categoria) == True):
                    flag = False
                else:
                    os.system('cls')
                    print("Error en el dato ingresado. Vuelva a intentarlo\n")
            try:
                conexion = sqlite3.connect("inventario.db")
                conexion.execute("BEGIN TRANSACTION")
                conexion.execute("UPDATE productos SET categoria = ? WHERE id = ?",(categoria,id))
                conexion.commit()
                os.system('cls')
                print("Categoria del producto modificado correctamente\n")
            except sqlite3.Error:
                os.system('cls')
                print("Ocurrio un error en la modificación solicitada\n")
                conexion.rollback()
            finally:
                conexion.close()

def volverInicio():
    flag = True 
    while flag == True:
        try:
            volver=int(input("¿Desea volver al menú principal? (ingrese opción numérica)\n1. Si\n2. No\n\nOpcion: "))
            os.system('cls')
            match volver:
                case 1:
                    return True
                case 2:
                    os.system('cls')
                    print("Fin de programa. Muchas gracias!")
                    return False
                case _:
                    os.system('cls')
                    print("Opcion incorrecta. Vuelva a intentarlo.\n")
        except:
            os.system('cls')
            print("Error! Ingrese opción númerica.\n")

def validarStr(entrada):
    try:
        num = int(entrada)
        return False
    except:
        return True
def validarVacio(entrada):
    if (entrada == "") or (entrada == " "):
        return False
    else:
        return True
def validarInt(entrada):
    try: 
        num = int(entrada)
        return True
    except:
        return False
def validarReal(entrada):
    try:
        num = float(entrada)
        return True
    except:
        return False

inicio()


