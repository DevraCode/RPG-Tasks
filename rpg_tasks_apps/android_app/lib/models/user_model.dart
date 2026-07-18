class UsuarioModel {
  final int? idUsuario;
  final String? idExternoUsuario;
  final String? nombreUsuario;
  final String? passwordUsuario;
  final String? emailUsuario;
  final DateTime? fechaRegistro;
  final bool? activo;
  final String? rango;
  final int? tipoUsuario;
  final String? idiomaUsuario;
  final int? idPlataforma;
  final String? nombrePlataforma;
  final String? idUsuarioEnPlataforma;

  UsuarioModel({
    this.idUsuario,
    this.idExternoUsuario,
    this.nombreUsuario,
    this.passwordUsuario,
    this.emailUsuario,
    this.fechaRegistro,
    this.activo,
    this.rango,
    this.tipoUsuario,
    this.idiomaUsuario,
    this.idPlataforma,
    this.nombrePlataforma,
    this.idUsuarioEnPlataforma,
  });

  factory UsuarioModel.fromJson(Map<String, dynamic> json) {
    return UsuarioModel(
      idUsuario: json['id_usuario'] as int,
      idExternoUsuario: json['id_externo_usuario'] as String,
      nombreUsuario: json['nombre_usuario'] as String,
      passwordUsuario: json['password_usuario'] as String,
      emailUsuario: json['email_usuario'] as String,
      fechaRegistro: json['fecha_registro'] as DateTime,
      activo: json['activo'] as bool,
      rango: json['rango'] as String,
      tipoUsuario: json['tipo_usuario'] as int,
      idiomaUsuario: json['idioma_usuario'] as String,
      idPlataforma: json['id_plataforma'] as int,
      nombrePlataforma: json['nombre_plataforma'] as String,
      idUsuarioEnPlataforma: json['id_usuario_en_plataforma'] as String,
    );
  }
}
