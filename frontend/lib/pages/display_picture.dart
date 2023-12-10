import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:frontend/pages/result.dart';
import 'package:http/http.dart' as http;

class DisplayPictureScreen extends StatelessWidget {
  final String imagePath;

  const DisplayPictureScreen({super.key, required this.imagePath});

  Future<String?> _sendImageToServer(File? imageFile) async {
    try {
      if (imageFile == null) {
        throw Exception('Image file is null');
      }

      print("sending request");
      //showLoadingDialog(context); // Show loading indicator
      final uri = Uri.parse('${dotenv.env['BACKEND_BASE_URL']}/predict');
      final request = http.MultipartRequest('POST', uri)
        ..files.add(http.MultipartFile(
            'image', imageFile.readAsBytes().asStream(), imageFile.lengthSync(),
            filename: "image" //basename(imageFile.path),
            ));

      final response = await http.Response.fromStream(await request.send());

      if (response.statusCode != 200) {
        throw Exception('response status not good');
      }

      print(response.body);
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return data["cls"].toString();
    } catch (e) {
      print('Error: $e');
      return null;
      //showErrorDialog(context, 'Error sending image to server');
    } finally {
      //Navigator.pop(context); // Dismiss loading indicator
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: Text("display")),
        body: Column(
          children: [
            Expanded(
              child: Image(
                image: FileImage(File(imagePath)),
                width: double.infinity,
                height: double.infinity,
                loadingBuilder: (context, child, loadingProgress) {
                  if (loadingProgress == null) {
                    debugPrint('image loading null');
                    return child;
                  }
                  debugPrint('image loading...');
                  return const Center(child: CircularProgressIndicator());
                },
              ),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (context) {
                      return FutureBuilder(
                        future: _sendImageToServer(File(imagePath)),
                        builder: (context, snapshot) {
                          if (snapshot.connectionState ==
                              ConnectionState.waiting) {
                            // While waiting for the future to complete, show a circular progress indicator
                            return const Scaffold(
                                body:
                                    Center(child: CircularProgressIndicator()));
                          } else if (snapshot.hasError) {
                            // If an error occurs, display an error message
                            return Scaffold(
                                body: Center(
                                    child: Text('Error: ${snapshot.error}')));
                          } else if (snapshot.hasData) {
                            // If data is available, navigate to the Result screen
                            return Result(message: snapshot.data.toString());
                          } else {
                            return Container(); // Handle other states as needed
                          }
                        },
                      );
                    },
                  ),
                );
              },
              child: const Text("Upload"),
            ),
          ],
        ));
  }
}
