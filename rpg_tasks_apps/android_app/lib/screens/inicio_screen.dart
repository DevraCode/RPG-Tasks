import 'package:flutter/material.dart';
import 'registro_screen.dart';
import 'login_screen.dart'; 

//dart format off
class InicioScreen extends StatelessWidget {
  const InicioScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        
        decoration: BoxDecoration(
          gradient: LinearGradient(begin: Alignment.topCenter, end: Alignment.bottomCenter, colors: [const Color.fromARGB(255, 192, 224, 194).withOpacity(0.8), Colors.black87]),
        ),
        child: SafeArea(

          child: Padding(padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 40.0),

            child: Column(

              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              crossAxisAlignment: CrossAxisAlignment.stretch,

              children: [
                const SizedBox(height: 20),

                Column(
                  children: [
                    const Icon(Icons.sunny, size: 100, color: Colors.amber,),

                    const SizedBox(height: 20),

                    Text('RPG TASKS',
                      style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontWeight: FontWeight.bold, color: Colors.amber,letterSpacing: 3)),

                    const SizedBox(height: 12),
                    Text('¡Mejora tu productividad como si fuera un juego de Rol!', textAlign: TextAlign.center, style: Theme.of(context,).textTheme.bodyLarge?.copyWith(color: Colors.white70)),
                  ]),

                
                Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    
                    ElevatedButton(onPressed: () {
                        
                      Navigator.push(context, MaterialPageRoute(builder: (context) => const RegistroScreen()));
                      },

                      //Botón de Registro
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color.fromARGB(255, 173, 140, 67),
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 18),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        elevation: 4,),

                      child: const Text('REGISTRO',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 1.2))
                    ),
                    
                    const SizedBox(height: 20), //Espacio para separar los botones

                    //Botón de Inicio de Sesión
                    OutlinedButton(onPressed: () {
                      Navigator.push(context, MaterialPageRoute(builder: (context) => const LoginScreen()));
                      },

                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.amber,
                        side: const BorderSide(color: Colors.amber, width: 2),
                        padding: const EdgeInsets.symmetric(vertical: 18),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                      ),

                      child: const Text(
                        'INICIAR SESIÓN',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 1.2)
                      ),
                    ),

                    const SizedBox(height: 20), //Otro espacio para separar
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
