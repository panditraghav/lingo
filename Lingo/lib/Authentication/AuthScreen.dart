import 'package:flutter/material.dart';

class Authscreen extends StatefulWidget {
  const Authscreen({super.key});

  @override
  _AuthscreenState createState() => _AuthscreenState();
}

class _AuthscreenState extends State<Authscreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF121212), // Dark background
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0D0D0D), Color(0xFF1A1A1A), Color(0xFF2C2C2C)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset('assets/images/lingoo2.png', height: 120),

            const SizedBox(height: 50),

            // Login Button with dark style
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4F46E5), // Accent purple
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(
                  horizontal: 30,
                  vertical: 12,
                ),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(25),
                ),
                elevation: 5,
              ),
              onPressed: () {
                Navigator.pushNamed(context, '/login');
                // TODO: Handle Login action
              },
              child: const Text(
                'Login',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),

            const SizedBox(height: 18),
            const Text(
              'OR',
              style: TextStyle(color: Colors.white38, fontSize: 20),
            ),

            const SizedBox(height: 18),

            // Google Sign-In Button with dark theme
            TextButton(
              onPressed: () {
                Navigator.pushNamed(context, '/signin');
                // TODO: Navigate to sign-in screen
              },
              child: const Text(
                'New User Registration ',
                style: TextStyle(color: Colors.white70, fontSize: 18),
              ),
            ),

            const SizedBox(height: 18),
          ],
        ),
      ),
    );
  }
}
