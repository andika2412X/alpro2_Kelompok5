from manim import *

# Fungsi Animasi Selamat Datang
class KasirAnimasi(Scene):
    def construct(self):
        kotak = Square(side_length=2, color=BLUE)
        teks = Text("Selamat Datang di Mesin Kasir").scale(0.8)

        self.play(Create(kotak))
        self.play(Write(teks))
        self.wait(2)