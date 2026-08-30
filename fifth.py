from manim import *

class EquationsOfMotionIntegration(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        title = Text("Equations of Motion via Integration", font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1)

        # STEP BY STEP DERIVATION - latex, like your first 4 cells style
        eq1 = MathTex(r"a = \frac{dv}{dt}", color=WHITE).scale(1.1)
        eq2 = MathTex(r"dv = a\,dt", color=ORANGE).scale(1.1)
        eq3 = MathTex(r"\int_{u}^{v} dv = \int_{0}^{t} a\,dt", color=GREEN).scale(1.0)
        eq4 = MathTex(r"v - u = at", color=BLUE).scale(1.1)
        eq5 = MathTex(r"v = u + at", color=YELLOW).scale(1.2)  # FIRST EQUATION

        eq6 = MathTex(r"v = \frac{ds}{dt}", color=WHITE).scale(1.1)
        eq7 = MathTex(r"ds = v\,dt = (u+at)\,dt", color=ORANGE).scale(1.0)
        eq8 = MathTex(r"\int_{0}^{s} ds = \int_{0}^{t} (u+at)\,dt", color=GREEN).scale(1.0)
        eq9 = MathTex(r"s = ut + \frac{1}{2}at^2", color=BLUE).scale(1.2)  # SECOND EQUATION

        eq10 = MathTex(r"a = v\frac{dv}{ds}", color=WHITE).scale(1.1)
        eq11 = MathTex(r"a\,ds = v\,dv", color=ORANGE).scale(1.1)
        eq12 = MathTex(r"\int_{0}^{s} a\,ds = \int_{u}^{v} v\,dv", color=GREEN).scale(1.0)
        eq13 = MathTex(r"as = \frac{v^2 - u^2}{2}", color=BLUE).scale(1.1)
        eq14 = MathTex(r"v^2 = u^2 + 2as", color=YELLOW).scale(1.2)  # THIRD EQUATION

        # FIRST EQUATION derivation
        self.play(Write(eq1), run_time=1)
        self.wait(0.5)
        self.play(Transform(eq1, eq2), run_time=1)
        self.play(Transform(eq1, eq3), run_time=1)
        self.play(Transform(eq1, eq4), run_time=1)
        self.play(Transform(eq1, eq5), run_time=1)
        self.wait(0.5)
        first_box = SurroundingRectangle(eq1, color=YELLOW, buff=0.2)
        first_label = Text("1st: v = u + at", font_size=22, color=YELLOW).next_to(first_box, DOWN, buff=0.2)
        self.play(Create(first_box), Write(first_label), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(eq1), FadeOut(first_box), FadeOut(first_label), run_time=0.8)

        # SECOND EQUATION
        self.play(Write(eq6), run_time=1)
        self.play(Transform(eq6, eq7), run_time=1)
        self.play(Transform(eq6, eq8), run_time=1)
        self.play(Transform(eq6, eq9), run_time=1)
        self.wait(0.5)
        second_box = SurroundingRectangle(eq6, color=BLUE, buff=0.2)
        second_label = Text("2nd: s = ut + ½at²", font_size=22, color=BLUE).next_to(second_box, DOWN, buff=0.2)
        self.play(Create(second_box), Write(second_label), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(eq6), FadeOut(second_box), FadeOut(second_label), run_time=0.8)

        # THIRD EQUATION
        self.play(Write(eq10), run_time=1)
        self.play(Transform(eq10, eq11), run_time=1)
        self.play(Transform(eq10, eq12), run_time=1)
        self.play(Transform(eq10, eq13), run_time=1)
        self.play(Transform(eq10, eq14), run_time=1)
        self.wait(0.5)
        third_box = SurroundingRectangle(eq10, color=YELLOW, buff=0.2)
        third_label = Text("3rd: v² = u² + 2as", font_size=22, color=YELLOW).next_to(third_box, DOWN, buff=0.2)
        self.play(Create(third_box), Write(third_label), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(eq10), FadeOut(third_box), FadeOut(third_label))

        # FINAL SUMMARY - all 3
        summary = VGroup(
            MathTex(r"v = u + at", color=YELLOW).scale(1.1),
            MathTex(r"s = ut + \frac{1}{2}at^2", color=BLUE).scale(1.1),
            MathTex(r"v^2 = u^2 + 2as", color=GREEN).scale(1.1),
        ).arrange(DOWN, buff=0.6).center().shift(DOWN*0.3)
        summary_title = Text("All Three Equations (via Integration)", font_size=28, color=WHITE).to_edge(UP, buff=0.4)
        
        self.play(Transform(title, summary_title), run_time=0.8)
        for eq in summary:
            self.play(Write(eq), run_time=1)
        self.wait(2)

class SimpleIntegrationQuote(Scene):
    # Short version for quick render - same as your first.py style
    def construct(self):
        title = Text("Derivation: v = u + at via Integration", font_size=30).to_edge(UP)
        self.play(Write(title))
        eqs = VGroup(
            MathTex(r"a = \frac{dv}{dt}", color=WHITE),
            MathTex(r"dv = a\,dt", color=ORANGE),
            MathTex(r"\int_{u}^{v} dv = \int_{0}^{t} a\,dt", color=GREEN),
            MathTex(r"v - u = at", color=BLUE),
            MathTex(r"v = u + at", color=YELLOW),
        ).arrange(DOWN, buff=0.5).center()
        for e in eqs:
            self.play(Write(e), run_time=1)
            self.wait(0.4)
        self.wait(1)
