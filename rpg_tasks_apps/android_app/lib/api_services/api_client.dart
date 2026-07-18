import 'package:dio/dio.dart';

class ApiClient {
  static final Dio _dio = Dio(
    BaseOptions(
      //baseUrl: 'http://10.0.2.2:8000/api',
      baseUrl: 'http://localhost:8000/api', //De momento voy a usar el web server
      connectTimeout: const Duration(seconds: 5),
      receiveTimeout: const Duration(seconds: 5),
    ),
  );

  static Dio get dio => _dio;
}
