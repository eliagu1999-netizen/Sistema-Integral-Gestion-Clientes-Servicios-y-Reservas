
from abc import ABC, abstractmethod
import re


# ==========================================
# 1. EXCEPCION PERSONALIZADA
# ==========================================

class ErrorValidacion(Exception):
    """Controla los errores de validacion del sistema."""
    pass


# ==========================================
# 2. CLASE ABSTRACTA ENTIDAD
# ==========================================

class Entidad(ABC):

    def __init__(self, identificacion, nombre):

        if not isinstance(identificacion, str) or not identificacion.strip():
            raise ErrorValidacion("La identificacion es obligatoria.")

        if not isinstance(nombre, str) or not nombre.strip():
            raise ErrorValidacion("El nombre es obligatorio.")

        self._identificacion = identificacion.strip()
        self._nombre = nombre.strip()

    @property
    def identificacion(self):
        return self._identificacion

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def describir(self):
        pass


# ==========================================
# 3. CLASE CLIENTE
# ==========================================

class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):

        super().__init__(identificacion, nombre)

        self.__correo = None
        self.__telefono = None

        self.correo = correo
        self.telefono = telefono

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, nuevo_correo):

        if not isinstance(nuevo_correo, str):
            raise ErrorValidacion("El correo debe ser texto.")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", nuevo_correo):
            raise ErrorValidacion("El correo electronico no es valido.")

        self.__correo = nuevo_correo

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):

        if not isinstance(nuevo_telefono, str):
            raise ErrorValidacion("El telefono debe ser texto.")

        if not re.fullmatch(r"\d{7,15}", nuevo_telefono):
            raise ErrorValidacion(
                "El telefono debe tener entre 7 y 15 digitos."
            )

        self.__telefono = nuevo_telefono

    def describir(self):

        return (
            f"Cliente: {self.nombre}\n"
            f"Identificacion: {self.identificacion}\n"
            f"Correo: {self.correo}\n"
            f"Telefono: {self.telefono}"
        )


# ==========================================
# 4. CLASE ABSTRACTA SERVICIO
# ==========================================

class Servicio(Entidad, ABC):

    def __init__(self, identificacion, nombre, tarifa):

        super().__init__(identificacion, nombre)

        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)):
            raise ErrorValidacion("La tarifa debe ser numerica.")

        if tarifa <= 0:
            raise ErrorValidacion("La tarifa debe ser mayor que cero.")

        self._tarifa = tarifa

    @property
    def tarifa(self):
        return self._tarifa

    def validar_duracion(self, duracion):

        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ErrorValidacion("La duracion debe ser numerica.")

        if duracion <= 0:
            raise ErrorValidacion("La duracion debe ser mayor que cero.")

    def validar_parametros(self, duracion, **kwargs):
        self.validar_duracion(duracion)

    def calcular_total(self, subtotal, impuesto, descuento):

        if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
            raise ErrorValidacion("El impuesto debe ser numerico.")

        if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
            raise ErrorValidacion("El descuento debe ser numerico.")

        if not 0 <= impuesto <= 1:
            raise ErrorValidacion("El impuesto debe estar entre 0 y 1.")

        if not 0 <= descuento <= 1:
            raise ErrorValidacion("El descuento debe estar entre 0 y 1.")

        total = subtotal * (1 - descuento) * (1 + impuesto)

        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0, **kwargs):
        pass

    @abstractmethod
    def describir(self):
        pass


# ==========================================
# 5. SERVICIO DE RESERVA DE SALAS
# ==========================================

class ReservaSala(Servicio):

    def validar_parametros(self, duracion, **kwargs):

        self.validar_duracion(duracion)

        capacidad = kwargs.get("capacidad")

        if isinstance(capacidad, bool) or not isinstance(capacidad, int):
            raise ErrorValidacion("La capacidad debe ser un numero entero.")

        if capacidad <= 0:
            raise ErrorValidacion("La capacidad debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **kwargs):

        self.validar_parametros(duracion, **kwargs)

        subtotal = self.tarifa * duracion

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):

        return (
            f"Reserva de sala: {self.nombre}\n"
            f"Tarifa por hora: ${self.tarifa}"
        )


# ==========================================
# 6. SERVICIO DE ALQUILER DE EQUIPOS
# ==========================================

class AlquilerEquipo(Servicio):

    def validar_parametros(self, duracion, **kwargs):

        self.validar_duracion(duracion)

        cantidad = kwargs.get("cantidad")

        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ErrorValidacion("La cantidad debe ser un numero entero.")

        if cantidad <= 0:
            raise ErrorValidacion("La cantidad debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **kwargs):

        self.validar_parametros(duracion, **kwargs)

        cantidad = kwargs["cantidad"]

        subtotal = self.tarifa * duracion * cantidad

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):

        return (
            f"Alquiler de equipos: {self.nombre}\n"
            f"Tarifa por hora y equipo: ${self.tarifa}"
        )


# ==========================================
# 7. SERVICIO DE ASESORIAS
# ==========================================

class Asesoria(Servicio):

    def validar_parametros(self, duracion, **kwargs):

        self.validar_duracion(duracion)

        modalidad = kwargs.get("modalidad")

        if not isinstance(modalidad, str) or modalidad not in (
            "virtual", "presencial"
        ):
            raise ErrorValidacion(
                "La modalidad debe ser virtual o presencial."
            )

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **kwargs):

        self.validar_parametros(duracion, **kwargs)

        modalidad = kwargs["modalidad"]

        subtotal = self.tarifa * duracion

        if modalidad == "presencial":
            subtotal *= 1.10

        return self.calcular_total(subtotal, impuesto, descuento)

    def describir(self):

        return (
            f"Asesoria especializada: {self.nombre}\n"
            f"Tarifa por hora: ${self.tarifa}"
        )


# ==========================================
# 8. PRUEBAS DE FUNCIONAMIENTO
# ==========================================

if __name__ == "__main__":

    print("================================")
    print("       SISTEMA SOFTWARE FJ")
    print("================================")

    # PRUEBA 1: REGISTRO DE CLIENTE VALIDO

    print("\nPRUEBA 1: REGISTRO DE CLIENTE")

    try:

        cliente1 = Cliente(
            "123456789",
            "Carlos Perez",
            "carlos@gmail.com",
            "3001234567"
        )

        print(cliente1.describir())

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 2: CLIENTE CON CORREO INCORRECTO

    print("\nPRUEBA 2: VALIDACION DE CORREO")

    try:

        cliente2 = Cliente(
            "987654321",
            "Maria Lopez",
            "correoincorrecto",
            "3101234567"
        )

        print(cliente2.describir())

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 3: CLIENTE CON TELEFONO INCORRECTO

    print("\nPRUEBA 3: VALIDACION DE TELEFONO")

    try:

        cliente3 = Cliente(
            "456789123",
            "Ana Torres",
            "ana@gmail.com",
            "123"
        )

        print(cliente3.describir())

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 4: CREACION DE SERVICIOS

    print("\nPRUEBA 4: SERVICIOS DISPONIBLES")

    try:

        servicios = [

            ReservaSala("S01", "Sala de reuniones", 50000),

            AlquilerEquipo("S02", "Computador", 15000),

            Asesoria("S03", "Asesoria de software", 80000)

        ]

        for servicio in servicios:
            print("\n" + servicio.describir())

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 5: CALCULO DE COSTOS

    print("\nPRUEBA 5: CALCULO DE COSTOS")

    try:

        print("Costo de sala: $", servicios[0].calcular_costo(
            2, impuesto=0.19, descuento=0.10, capacidad=10
        ))

        print("Costo de equipos: $", servicios[1].calcular_costo(
            3, impuesto=0.19, descuento=0.05, cantidad=2
        ))

        print("Costo de asesoria: $", servicios[2].calcular_costo(
            2, impuesto=0.19, descuento=0, modalidad="presencial"
        ))

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 6: DURACION INCORRECTA

    print("\nPRUEBA 6: VALIDACION DE DURACION")

    try:

        servicios[0].calcular_costo(
            -2, capacidad=10
        )

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 7: CANTIDAD INCORRECTA

    print("\nPRUEBA 7: VALIDACION DE EQUIPOS")

    try:

        servicios[1].calcular_costo(
            2, cantidad=0
        )

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 8: MODALIDAD INCORRECTA

    print("\nPRUEBA 8: VALIDACION DE ASESORIA")

    try:

        servicios[2].calcular_costo(
            2, modalidad="incorrecta"
        )

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 9: TARIFA INCORRECTA

    print("\nPRUEBA 9: VALIDACION DE TARIFA")

    try:

        servicio_invalido = ReservaSala(
            "S04", "Sala invalida", -5000
        )

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    # PRUEBA 10: CALCULO CON IMPUESTO INCORRECTO

    print("\nPRUEBA 10: VALIDACION DE IMPUESTOS")

    try:

        servicios[0].calcular_costo(
            2, impuesto=1.5, capacidad=10
        )

    except ErrorValidacion as error:
        print("Error de validacion:", error)

    finally:

        print("\n================================")
        print(" FINALIZARON TODAS LAS PRUEBAS")
        print("================================")

