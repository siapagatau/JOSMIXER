# Aturan R8/ProGuard (dipakai bila isMinifyEnabled = true di release).
# JNI: nama method external di AudioEngine dipetakan ke fungsi C++ (native-lib.cpp) -> jangan di-rename.
-keepclasseswithmembernames class * { native <methods>; }
-keep class com.karaoke.reverbmic.AudioEngine { *; }
# AndroidSVG membaca atribut lewat refleksi ringan; org.json & javax.xml bagian dari platform Android.
-keep class com.caverock.androidsvg.** { *; }
-dontwarn com.caverock.androidsvg.**
