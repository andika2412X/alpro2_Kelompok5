from manim import *

class TransaksiBerhasil(Scene):
    def construct(self):
        teks = Text("Transaksi Berhasil!", color=BLUE)
        kotak = Square(side_length=2, color=RED)
        lingkaran = Circle(radius=1, color=BLUE)

        # Posisi awal kotak
        self.play(Create(kotak))
        self.wait(1)

        # Transformasi kotak menjadi lingkaran
        self.play(Transform(kotak, lingkaran))
        self.wait(1)
        self.play(Write(teks))
        self.wait(2)