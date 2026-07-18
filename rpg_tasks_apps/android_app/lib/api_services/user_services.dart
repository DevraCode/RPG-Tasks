import 'package:dio/dio.dart';
import '../models/user_model.dart';
import 'api_client.dart';

class AuthService {
  final Dio _dio = ApiClient.dio;

  Future<UsuarioModel?> registrarUsuario(String idExternoUsuario, String nombreUsuario, String passwordUsuario, String emailUsuario, String rango, int tipoUsuario, String idiomaUsuario, String idUsuarioEnPlataforma,
  ) async {
    try {
      final response = await _dio.post(
        '/usuarios/registro',

        data: {
          "id_externo_usuario": idExternoUsuario,
          "nombre_usuario": nombreUsuario,
          "password_usuario": passwordUsuario,
          "email_usuario": emailUsuario,
          "rango": "NOVATO",
          "tipo_usuario": 0,
          "idioma_usuario": idiomaUsuario,
          "id_plataforma": 2,
          "nombre_plataforma": "ANDROID",
          "id_usuario_en_plataforma": idUsuarioEnPlataforma,
        },
      );

      if (response.statusCode == 201 && response.data != null) {
        return UsuarioModel.fromJson(response.data);
      }
    } on DioException catch (e) {
      _manejarError(e);
    }
    return null;
  }

  void _manejarError(DioException e) {
    if (e.response != null) {
      throw Exception(e.response?.data['detail'] ?? 'Error en el servidor');
    } else {
      throw Exception('Error de conexión. Verifica tu internet.');
    }
  }
}
