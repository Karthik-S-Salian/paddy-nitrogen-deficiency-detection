import 'package:flutter/material.dart';

class Result extends StatelessWidget {
  final String message;
  const Result({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text("Result"),
      ),
      body: Center(
        child: Text(message),
      ),
    );
  }
}
