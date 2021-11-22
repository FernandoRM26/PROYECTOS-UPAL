from datetime import datetime
now = datetime.now()
class ATM:
    clientes,saldo_pen,saldo_usd,mov_pen,mov_usd = {},{},{},{},{}

    def __init__(self):
        self.usuario, self.contrasenia = None, None        
    
    def iniciar_sesion(self,i=0):
        if i == 3:
            self.usuario,self.contrasenia = None, None 
            print('Supero limite de intentos')
            return ATM.menu_principal(self)
        self.usuario = input('Ingrese usuario\n-> ')
        self.usuario = self.usuario.lower()
        if self.usuario == None:
            print('No existe datos de usuario')
            return ATM.iniciar_sesion(self,i+1)
        elif self.usuario not in ATM.clientes:
            print('No existe datos de usuario')
            return ATM.iniciar_sesion(self,i+1)
        else:
            print(f'Bienvenid@ |{self.usuario.upper()}|')
            self.contrasenia = int(input('Ingrese Contraseña\n-> '))
            if ATM.clientes[self.usuario] == self.contrasenia:
                print('Inicio sesion correctamente')
                return ATM.operaciones(self)
            else:
                print('La contraseña es incorrecta intente nuevamente')
                return ATM.iniciar_sesion(self,i+1)
            
    def cerrar_sesion(self):
        self.usuario, self.contrasenia = None, None
        ATM.menu_principal(self)

    def consultar(self, i = 0): #   i suma los intentos (Si cumple retorna al menu operaciones)
        if i == 3:      #   Control de intentos 
            print('Supero limite de intentos')
            return ATM.operaciones(self) 
        opcion = int(input('¿QUE DESEA CONSULTAR?\n1. Todos los saldos\n2. Movimientos\n-> '))
        contra = int(input('Ingrese su clave secreta\n-> '))
        if ATM.clientes[self.usuario] != contra: #  Control de contraseña
            print('Contraseña incorrecta\nIntente nuenvamente')
            return ATM.consultar(self,i+1) #    Recursividad
        else:
            if opcion == 1: #   Todos los saldos PEN y USD
                print(f'Su saldo:\n Soles : {ATM.saldo_pen[self.usuario]}\nDolares : {ATM.saldo_usd[self.usuario]}')
            elif opcion == 2: # Movimientos segun moneda PEN / USD
                opcion = int(input('1. Soles\n2. Dolares\n-> '))
                if opcion == 1:
                    for i in ATM.mov_pen[self.usuario]: #   Imprime los ultimos 15 movimientos moneda PEN y su saldo actual
                        print(i)
                    print('saldo final :\tS/ ', ATM.saldo_pen[self.usuario])
                elif opcion == 2:
                    for i in ATM.mov_usd[self.usuario]: #   Imprime los ultimos 15 movimientos moneda USD y su saldo actual
                        print(i)
                    print('saldo final :\t$ ', ATM.saldo_usd[self.usuario])
                else:
                    print('Opcion incorrecta\nIntente nuevamente')
                    return ATM.consultar(self,i+1) #    Recursividad 
            else:
                print('Opcion incorrecta\nIntente nuevamente')
                return ATM.consultar(self,i+1) # Recursividad
        return ATM.operaciones(self)
    
    def depositar(self, valor,opcion):
        if valor < 0: # Valida el monto
            print('Monto ingresado no es valido')
            return ATM.operaciones(self)
        if opcion == 1: #   Deposita el valor en moneda PEN
            ATM.saldo_pen[self.usuario] = ATM.saldo_pen[self.usuario] + valor
            ATM.mov_pen[self.usuario].insert(0,f'Deposito\tS/ {valor}') #   Acumula los movimientos en PEN en una lista
            print(f'DEPOSITO EN SOLES\nNombre :\t{self.usuario.upper()}\nMonto  :\tS/ {valor}\n{now.date()}\t{now.hour}:{now.minute}:{now.second}') #    Voucher
            if len(ATM.mov_pen[self.usuario]) == 15: #  Controla el maximo de 15 movimientos
                ATM.mov_pen[self.usuario].pop() #   Desencolado
        elif opcion == 2: #   Deposita el valor en moneda USD
            ATM.saldo_usd[self.usuario] = ATM.saldo_usd[self.usuario] + valor
            ATM.mov_usd[self.usuario].insert(0,f'Deposito\t$ {valor}') #   Acumula los movimientos en USD en una lista
            print(f'DEPOSITO EN DOLARES\nNombre :\t{self.usuario.upper()}\nMonto  :\t$ {valor}\n{now.date()}\t{now.hour}:{now.minute}:{now.second}') #    Voucher
            if len(ATM.mov_usd[self.usuario]) == 15: #  Controla el maximo de 15 movimientos
                ATM.mov_usd[self.usuario].pop() # Desencolado
        return ATM.operaciones(self)

    def retiro(self,valor,opcion):
        if valor < 0: # Valida el monto
            print('Monto ingresado no es valido')
            return ATM.operaciones(self)
        if opcion == 1: 
            if ATM.saldo_pen[self.usuario] < valor: #   Valida el saldo PEN 
                print(f'Usted no cuenta con ese monto\nSu saldo actual es S/ {ATM.saldo_pen[self.usuario]}')            
            elif ATM.saldo_pen[self.usuario] > valor: # Realiza la opracion PEN
                ATM.saldo_pen[self.usuario] = ATM.saldo_pen[self.usuario] - valor # Reduce el saldo PEN
                ATM.mov_pen[self.usuario].insert(0,f'Retiro {valor}') # Añade el movimiento PEN
                print(f'\nRETIRO EN SOLES\nNombre :\t{self.usuario.upper()}\nMonto  :\tS/ {valor}\nSaldo  :\tS/ {ATM.saldo_pen[self.usuario]}\n{now.date()}\t{now.hour}:{now.minute}:{now.second}') #    Voucher
                if len(ATM.mov_pen[self.usuario]) == 15: #  Verifica maximo ultimos movimientos PEN 15
                    ATM.mov_pen[self.usuario].pop()
        elif opcion == 2:
            if ATM.saldo_usd[self.usuario] < valor: # Verifica el Saldo USD
                print(f'Usted no cuenta con ese monto\nSu saldo actual es $ {ATM.saldo_usd[self.usuario]}')
            elif ATM.saldo_usd[self.usuario] > valor: # Realiza la opracion PEN
                ATM.saldo_usd[self.usuario] = ATM.saldo_usd[self.usuario] - valor # Reduce el saldo USD
                ATM.mov_usd[self.usuario].insert(0,f'Retiro {valor}') # Añade el movimiento USD
                print(f'RETIRO EN DOLARES\nNombre :\t{self.usuario.upper()}\nMonto  :\t$ {valor}\nSaldo  :\t$ {ATM.saldo_usd[self.usuario]}\n{now.date()}\t{now.hour}:{now.minute}:{now.second}') #    Voucher
                if len(ATM.mov_usd[self.usuario]) == 15: #Verifica maximo ultimos movimientos PEN 15
                    ATM.mov_usd[self.usuario].pop()
        return ATM.operaciones(self)
    
    def cambio_pin(self,i=0):
        if i == 3:
            print('Supero limite de intentos')
            return ATM.menu_principal(self)
        pin = int(input('Ingrese su clave actual\n-> '))        
        if ATM.clientes[self.usuario] == pin:
            pin_1,pin_2 = int(input('Ingrese su nueva clave\n-> ')),int(input('Confirme su nueva clave\n-> '))
            if pin_1 != pin_2:
                print('Contraseña no coinciden'),ATM.cambio_pin(self,i+1)        
        if pin_1 == pin_2:
            ATM.clientes[self.usuario] = pin_2
            print('Se cambio la clave correctamente')
            return ATM.operaciones(self)

    def nuevo_cliente(self,i=0):
        if i == 3: 
            print('Supero limite de intentos'),ATM.menu_principal(self)        
        clave = input('Ingrese usuario\n-> ')
        clave = clave.lower()
        for x in ATM.clientes:
            if clave in x:
                print('Usuario ya existe\nPRUEBE CON OTRO NOMBRE DE USUARIO'),ATM.nuevo_cliente(self,i+1)     
        pin_1,pin_2 = int(input('Ingrese su nueva clave\n-> ')),int(input('Confirme su nueva clave\n-> '))
        while pin_1 != pin_2:
            print('Contraseña no coinciden, intente nuevamente')
            pin_1,pin_2,i= int(input('Ingrese su nueva clave\n-> ')),int(input('Confirme su nueva clave\n-> ')),i+1
            if i == 2:
                print('Supero limite de intentos'),ATM.menu_principal(self)            
        if pin_1 == pin_2:
            ATM.clientes[clave],ATM.saldo_pen[clave],ATM.saldo_usd[clave],ATM.mov_pen[clave],ATM.mov_usd[clave] =  pin_2,0,0,[],[]
            print(f'Se registro a usuario |{clave.upper()}| exitosamente'),ATM.menu_principal(self)
    
    def operaciones(self,i=0):
        if i == 3: # Recursividad
            print('Supero limite de intentos'),ATM.cerrar_sesion(self)
        print('Operaciones\n1 Consultar\n2. Depositar\n3. Retirar\n4. Cambiar clave secreta\n5. Cerrar sesion')
        opcion = int(input('-> '))       
        if opcion == 1:              
            ATM.consultar(self)
        elif opcion == 2:
            opcion = int(input('1. Soles\n2. Dolares\n-> '))
            if opcion not in [1,2]:
                print('Opcion incorrecta'),ATM.operaciones(self)
            else:                   
                ATM.depositar(self,int(input('Ingrese monto a depositar\n-> ')),opcion)
        elif opcion == 3:
            opcion = int(input('1. Soles\n2. Dolares\n-> '))
            if opcion not in [1,2]:
                print('Opcion incorrecta'),ATM.operaciones(self)
            else:
                ATM.retiro(self,int(input('Ingrese monto a retirar\n-> ')),opcion)
        elif opcion == 4:
            ATM.cambio_pin(self)
        elif opcion == 6:
            ATM.nuevo_cliente(self) 
        elif opcion == 5:
            ATM.cerrar_sesion(self)
        else:
            print('Opcion invalida intente nuevamente'),ATM.operaciones(self,i+1)

    def menu_principal(self):
        opcion = int(input('Menu principal\n1. Iniciar sesion\n2. Registrarse\n->'))
        if opcion == 1:
            ATM.iniciar_sesion(self)
        elif opcion == 2:
            ATM.nuevo_cliente(self)

usuario = ATM()
usuario.menu_principal()
