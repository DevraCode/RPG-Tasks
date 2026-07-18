
// dart format off
import 'package:android_app/api_services/user_services.dart';
import 'package:flutter/material.dart';

class RegistroScreen extends StatefulWidget {
  const RegistroScreen({super.key});

  @override
  State<RegistroScreen> createState() => _RegistroScreenState();
}

class _RegistroScreenState extends State<RegistroScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usuarioController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();


  bool _isLoading = false;

  @override
  void dispose() {
    _usuarioController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Registro de Héroe')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: _usuarioController,
                decoration: const InputDecoration(labelText: 'Nombre de usuario', border: OutlineInputBorder()),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: 'Correo electrónico', border: OutlineInputBorder()),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Contraseña', border: OutlineInputBorder()),
              ),
              const SizedBox(height: 24),
              // dart format off
              ElevatedButton(
                onPressed: _isLoading ? null : () async {
                  
                  if (!_formKey.currentState!.validate()) return;

                  
                  setState(() => _isLoading = true);

                  try {
                    
                    final authService = AuthService();

                    // Datos simulados de momento
                    final String idExternoSimulado = "EXT_${DateTime.now().millisecondsSinceEpoch}";
                    final String idPlataformaSimulada = "PLAT_${DateTime.now().microsecondsSinceEpoch}";

                    
                    final usuarioCreado = await authService.registrarUsuario(
                      idExternoSimulado,                  
                      _usuarioController.text.trim(),     
                      _passwordController.text,           
                      _emailController.text.trim(),       
                      "NOVATO",
                      0,
                      "es",                           
                      idPlataformaSimulada,               
                    );

                    
                    setState(() => _isLoading = false);

                    
                    if (usuarioCreado != null && mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('¡Registro exitoso! Bienvenido, ${usuarioCreado.nombreUsuario}'), 
                          backgroundColor: Colors.green
                        ),
                      );
                      
                      
                      Navigator.pop(context);
                    } else if (mounted) {
                      throw Exception('El servidor respondió pero no devolvió los datos del jugador.');
                    }

                  } catch (e) {
                    
                    setState(() => _isLoading = false);
                    if (mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          
                          content: Text(e.toString().replaceAll('Exception: ', '')), 
                          backgroundColor: Colors.red
                        ),
                      );
                    }
                  }
                },
                child: _isLoading 
                  ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white)) 
                  : const Text('Crear Cuenta de Héroe'),
              )
            ],
          ),
        ),
      ),
    );
  }
}