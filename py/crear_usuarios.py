
from getpass import getpass
from werkzeug.security import generate_password_hash
from app import obtener_conexion


cuentas = [
    {
        "nombre": "Administrador",
        "usuario": "admin",
        "rol": "administrador",
        "departamento": None
    },
    {
        "nombre": "Atención Ciudadana",
        "usuario": "atencion",
        "rol": "departamento",
        "departamento": "Atención Ciudadana"
    },
    {
        "nombre": "Desarrollo Económico",
        "usuario": "economico",
        "rol": "departamento",
        "departamento": "Desarrollo Económico"
    },
    {
        "nombre": "Desarrollo Social",
        "usuario": "social",
        "rol": "departamento",
        "departamento": "Desarrollo Social"
    },
    {
        "nombre": "DIF",
        "usuario": "dif",
        "rol": "departamento",
        "departamento": "DIF"
    },
    {
        "nombre": "Casa Naranja",
        "usuario": "casa_naranja",
        "rol": "departamento",
        "departamento": "Casa Naranja"
    }
]


conexion = obtener_conexion()

try:
    for cuenta in cuentas:

        print("\nCuenta:", cuenta["nombre"])
        print("Usuario:", cuenta["usuario"])

        while True:
            contrasena = getpass("Crea una contraseña: ")
            confirmar = getpass("Confirma la contraseña: ")

            if contrasena == confirmar and contrasena:
                break

            print("Las contraseñas no coinciden o están vacías.")

        hash_contrasena = generate_password_hash(contrasena)

        existente = conexion.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            (cuenta["usuario"],)
        ).fetchone()

        if existente:
            conexion.execute(
                """
                UPDATE usuarios
                SET nombre = ?, contrasena = ?, rol = ?, departamento = ?
                WHERE usuario = ?
                """,
                (
                    cuenta["nombre"],
                    hash_contrasena,
                    cuenta["rol"],
                    cuenta["departamento"],
                    cuenta["usuario"]
                )
            )
        else:
            conexion.execute(
                """
                INSERT INTO usuarios
                (nombre, usuario, contrasena, rol, departamento)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    cuenta["nombre"],
                    cuenta["usuario"],
                    hash_contrasena,
                    cuenta["rol"],
                    cuenta["departamento"]
                )
            )

        print("Cuenta guardada correctamente.")

    conexion.commit()
    print("\n¡Las seis cuentas fueron registradas correctamente!")

finally:
    conexion.close()

from werkzeug.security import check_password_hash

conexion = obtener_conexion()

cuenta = conexion.execute(
    "SELECT contrasena FROM usuarios WHERE usuario = ?",
    ("atencion",)
).fetchone()

conexion.close()

if cuenta:
    prueba = input("Escribe la contraseña de atencion: ")

    if check_password_hash(cuenta["contrasena"], prueba):
        print("La contraseña coincide.")
    else:
        print("La contraseña NO coincide.")
