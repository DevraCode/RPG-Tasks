//Modelo para el Usuario
//Tendrá los datos necesarios para pedirlos en los repositorios
//El resto de campos(id del usuario, fecha registro, etc) se encargarán de rellenarlos el caso de uso del core y la base de datos(datos por defecto)

class UsuarioModel {
  final String? idExternoUsuario; //Necesario para la búsqueda y el inicio de sesión
  final String? nombreUsuario;
  final String? passwordUsuario;
  final String? emailUsuario;
  final String? idiomaUsuario;
  final int? idPlataforma;
  final String? idUsuarioEnPlataforma;
  final String? tokenUsuario;

  UsuarioModel({
    this.idExternoUsuario,
    this.nombreUsuario,
    this.passwordUsuario,
    this.emailUsuario,
    this.idiomaUsuario,
    this.idPlataforma,
    this.idUsuarioEnPlataforma,
    this.tokenUsuario
  });

  factory UsuarioModel.fromJson(Map<String, dynamic> json) {
    return UsuarioModel(
      idExternoUsuario: json['id_externo_usuario'] as String? ?? " ",
      nombreUsuario: json['nombre_usuario'] as String? ?? " ",
      passwordUsuario: json['password_usuario'] as String? ?? " ",
      emailUsuario: json['email_usuario'] as String? ?? " ",
      idiomaUsuario: json['idioma_usuario'] as String? ?? " ",
      idPlataforma: json['id_plataforma'] as int? ?? 0,
      idUsuarioEnPlataforma: json['id_usuario_en_plataforma'] as String? ?? " ",
      tokenUsuario: json['token_usuario'] as String? ?? " ",
    );
  }
}
