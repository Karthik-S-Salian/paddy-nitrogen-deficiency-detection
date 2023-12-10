import 'package:flutter/material.dart';
import 'package:frontend/pages/display_picture.dart';
import 'package:image_picker/image_picker.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  void onPress(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (BuildContext context) {
        return SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Center(
              child: Column(
                children: [
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size.fromHeight(50),
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () {
                      _pickImageFromCamera(context);
                    },
                    child: const Text("From Camera"),
                  ),
                  const SizedBox(
                    height: 30,
                  ),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size.fromHeight(50),
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () {
                      _pickImageFromGallery(context);
                    },
                    child: const Text("From Gallery"),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void navigateToNext(BuildContext context, String path) {
    Navigator.of(context).push(
      MaterialPageRoute(
          builder: (context) => DisplayPictureScreen(imagePath: path)),
    );
  }

  Future<void> _pickImageFromGallery(BuildContext context) async {
    await ImagePicker()
        .pickImage(source: ImageSource.gallery)
        .then((returnedImage) {
      if (returnedImage == null) return;

      navigateToNext(context, returnedImage.path);
    });
  }

  Future<void> _pickImageFromCamera(BuildContext context) async {
    await ImagePicker()
        .pickImage(source: ImageSource.camera)
        .then((returnedImage) {
      if (returnedImage == null) return;
      navigateToNext(context, returnedImage.path);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text("Home"),
      ),
      body: const Center(
        child: Text("hello farmer"),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => onPress(context),
        child: const Icon(Icons.camera_alt),
      ),
    );
  }
}
