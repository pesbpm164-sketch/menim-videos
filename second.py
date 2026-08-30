from manim import *
import numpy as np

# second.py - Main 30 sec video with connecting line showing differentiation happening
# This is the video you asked: line connecting x^2 to 2x and moving

class DifferentiationFlow30Sec(Scene):
    def construct(self):
        # Intro quote
        intro = Text("Differentiation: Measuring Instant Change", font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        # Two axes - left for f(x), right for f'(x) - gap prevents arrow touch
        left_axes = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-1, 5, 1],
            x_length=5.5, y_length=3.5
        ).shift(LEFT*3.5 + DOWN*0.5)

        right_axes = Axes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-3, 3, 1],
            x_length=5.5, y_length=3.5
        ).shift(RIGHT*3.5 + DOWN*0.5)

        diff_arrow = Arrow(LEFT*0.5, RIGHT*0.5, color=YELLOW, buff=0.2).shift(UP*2.5)
        diff_label = MathTex(r"\frac{d}{dx}", color=YELLOW).next_to(diff_arrow, UP, buff=0.2).scale(0.9)

        self.play(Create(left_axes), Create(right_axes), Create(diff_arrow), Write(diff_label))

        # === 1. x^2 -> 2x with moving connecting line (0-9s) ===
        f1_l = MathTex(r"f(x)=x^2", color=BLUE).next_to(left_axes, UP, buff=0.4).scale(0.8)
        df1_l = MathTex(r"f'(x)=2x", color=RED).next_to(right_axes, UP, buff=0.4).scale(0.8)
        f1_g = left_axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=BLUE)
        df1_g = right_axes.plot(lambda x: 2*x, x_range=[-2.5, 2.5], color=RED)

        self.play(Write(f1_l), Write(df1_l), Create(f1_g), Create(df1_g), run_time=2)

        # Your requested connecting line that moves as differentiation happens
        tracker = ValueTracker(-2.0)
        dot_f = always_redraw(lambda: Dot(color=BLUE).move_to(left_axes.c2p(tracker.get_value(), tracker.get_value()**2)).scale(0.7))
        dot_df = always_redraw(lambda: Dot(color=RED).move_to(right_axes.c2p(tracker.get_value(), 2*tracker.get_value())).scale(0.7))
        conn = always_redraw(lambda: DashedLine(dot_f.get_center(), dot_df.get_center(), color=YELLOW, dash_length=0.1))

        self.add(dot_f, dot_df, conn)
        self.play(tracker.animate.set_value(2.0), run_time=4, rate_func=linear)
        self.remove(dot_f, dot_df, conn)
        self.wait(0.5)
        self.play(FadeOut(f1_g), FadeOut(df1_g), FadeOut(f1_l), FadeOut(df1_l))

        # === 2. sin x -> cos x (9-18s) ===
        f2_l = MathTex(r"f(x)=\sin x", color=BLUE).next_to(left_axes, UP, buff=0.4).scale(0.8)
        df2_l = MathTex(r"f'(x)=\cos x", color=RED).next_to(right_axes, UP, buff=0.4).scale(0.8)
        f2_g = left_axes.plot(lambda x: np.sin(x), x_range=[-3, 3], color=BLUE)
        df2_g = right_axes.plot(lambda x: np.cos(x), x_range=[-3, 3], color=RED)

        self.play(Write(f2_l), Write(df2_l), Create(f2_g), Create(df2_g), run_time=2)
        tracker2 = ValueTracker(-2.5)
        dot_f2 = always_redraw(lambda: Dot(color=BLUE).move_to(left_axes.c2p(tracker2.get_value(), np.sin(tracker2.get_value()))).scale(0.7))
        dot_df2 = always_redraw(lambda: Dot(color=RED).move_to(right_axes.c2p(tracker2.get_value(), np.cos(tracker2.get_value()))).scale(0.7))
        conn2 = always_redraw(lambda: DashedLine(dot_f2.get_center(), dot_df2.get_center(), color=YELLOW, dash_length=0.1))
        self.add(dot_f2, dot_df2, conn2)
        self.play(tracker2.animate.set_value(2.5), run_time=4, rate_func=linear)
        self.remove(dot_f2, dot_df2, conn2)
        self.wait(0.5)
        self.play(FadeOut(f2_g), FadeOut(df2_g), FadeOut(f2_l), FadeOut(df2_l))

        # === 3. x^3 -> 3x^2 (18-27s) ===
        f3_l = MathTex(r"f(x)=x^3", color=BLUE).next_to(left_axes, UP, buff=0.4).scale(0.8)
        df3_l = MathTex(r"f'(x)=3x^2", color=RED).next_to(right_axes, UP, buff=0.4).scale(0.8)
        f3_g = left_axes.plot(lambda x: x**3, x_range=[-1.8, 1.8], color=BLUE)
        df3_g = right_axes.plot(lambda x: 3*x**2, x_range=[-1.8, 1.8], color=RED)

        self.play(Write(f3_l), Write(df3_l), Create(f3_g), Create(df3_g), run_time=2)
        tracker3 = ValueTracker(-1.5)
        dot_f3 = always_redraw(lambda: Dot(color=BLUE).move_to(left_axes.c2p(tracker3.get_value(), tracker3.get_value()**3)).scale(0.7))
        dot_df3 = always_redraw(lambda: Dot(color=RED).move_to(right_axes.c2p(tracker3.get_value(), 3*tracker3.get_value()**2)).scale(0.7))
        conn3 = always_redraw(lambda: DashedLine(dot_f3.get_center(), dot_df3.get_center(), color=YELLOW, dash_length=0.1))
        self.add(dot_f3, dot_df3, conn3)
        self.play(tracker3.animate.set_value(1.5), run_time=4, rate_func=linear)
        self.remove(dot_f3, dot_df3, conn3)

        self.play(FadeOut(f3_g), FadeOut(df3_g), FadeOut(f3_l), FadeOut(df3_l), FadeOut(left_axes), FadeOut(right_axes), FadeOut(diff_arrow), FadeOut(diff_label))

        # Final quote
        final = VGroup(
            Text('"Differentiation is the art of', font_size=32),
            Text('seeing change in a frozen moment."', font_size=32),
            MathTex(r"\text{— Derivative: Heartbeat of Change}", color=YELLOW).scale(0.7)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.2)
        title = MathTex(r"\text{Visualizing } f(x) \rightarrow f'(x)").to_edge(UP, buff=0.5)
        self.play(Write(title), Write(final), run_time=3)
        self.wait(2)

class DifferentiationQuote(Scene):
    def construct(self):
        quote = VGroup(
            MathTex(r"\text{``The derivative is the instantaneous", font_size=36),
            MathTex(r"\text{rate of change — how a curve breathes.''}", font_size=36),
        ).arrange(DOWN, buff=0.2)
        author = Text("— For your differentiation video", font_size=24, color=YELLOW).next_to(quote, DOWN, buff=0.5)
        self.play(Write(quote), run_time=2)
        self.play(Write(author))
        self.wait(3)
