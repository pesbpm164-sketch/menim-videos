from manim import *
import numpy as np

class IntegrationFlow30Sec(Scene):
    def construct(self):
        intro = Text("Integration: Accumulating Change", font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        left_axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[-1, 6, 1],
            x_length=5.5, y_length=3.5
        ).shift(LEFT*3.5 + DOWN*0.5)

        right_axes = Axes(
            x_range=[-0.5, 3.5, 1],
            y_range=[-1, 6, 1],
            x_length=5.5, y_length=3.5
        ).shift(RIGHT*3.5 + DOWN*0.5)

        int_arrow = Arrow(LEFT*0.5, RIGHT*0.5, color=YELLOW, buff=0.2).shift(UP*2.5)
        int_label = MathTex(r"\int dx", color=YELLOW).next_to(int_arrow, UP, buff=0.2).scale(0.9)

        self.play(Create(left_axes), Create(right_axes), Create(int_arrow), Write(int_label))

        # 1. x^2 -> x^3/3 with area filling (0-10s)
        f1_l = MathTex(r"f(x)=x^2", color=BLUE).next_to(left_axes, UP, buff=0.4).scale(0.8)
        df1_l = MathTex(r"F(x)=\frac{x^3}{3}", color=RED).next_to(right_axes, UP, buff=0.4).scale(0.8)

        f1_g = left_axes.plot(lambda x: x**2, x_range=[0, 3], color=BLUE)
        df1_g = right_axes.plot(lambda x: x**3/3, x_range=[0, 3], color=RED)

        self.play(Write(f1_l), Write(df1_l), Create(f1_g), Create(df1_g), run_time=2)

        tracker = ValueTracker(0.1)
        area = always_redraw(lambda: left_axes.get_area(f1_g, x_range=[0, tracker.get_value()], color=[BLUE, GREEN], opacity=0.5))
        dot_f = always_redraw(lambda: Dot(color=BLUE).move_to(left_axes.c2p(tracker.get_value(), tracker.get_value()**2)).scale(0.7))
        dot_df = always_redraw(lambda: Dot(color=RED).move_to(right_axes.c2p(tracker.get_value(), tracker.get_value()**3/3)).scale(0.7))
        conn = always_redraw(lambda: DashedLine(dot_f.get_center(), dot_df.get_center(), color=YELLOW, dash_length=0.1))

        self.add(area, dot_f, dot_df, conn)
        self.play(tracker.animate.set_value(2.5), run_time=5, rate_func=linear)
        self.remove(area, dot_f, dot_df, conn)
        self.wait(0.5)
        self.play(FadeOut(f1_g), FadeOut(df1_g), FadeOut(f1_l), FadeOut(df1_l))

        # 2. sin -> -cos (10-20s)
        f2_l = MathTex(r"f(x)=\sin x", color=BLUE).next_to(left_axes, UP, buff=0.4).scale(0.8)
        df2_l = MathTex(r"F(x)=-\cos x", color=RED).next_to(right_axes, UP, buff=0.4).scale(0.8)

        f2_g = left_axes.plot(lambda x: np.sin(x), x_range=[0, 3.14], color=BLUE)
        df2_g = right_axes.plot(lambda x: -np.cos(x), x_range=[0, 3.14], color=RED)

        self.play(Write(f2_l), Write(df2_l), Create(f2_g), Create(df2_g), run_time=2)

        tracker2 = ValueTracker(0.1)
        area2 = always_redraw(lambda: left_axes.get_area(f2_g, x_range=[0, tracker2.get_value()], color=[BLUE, GREEN], opacity=0.5))
        dot_f2 = always_redraw(lambda: Dot(color=BLUE).move_to(left_axes.c2p(tracker2.get_value(), np.sin(tracker2.get_value()))).scale(0.7))
        dot_df2 = always_redraw(lambda: Dot(color=RED).move_to(right_axes.c2p(tracker2.get_value(), -np.cos(tracker2.get_value()))).scale(0.7))
        conn2 = always_redraw(lambda: DashedLine(dot_f2.get_center(), dot_df2.get_center(), color=YELLOW, dash_length=0.1))

        self.add(area2, dot_f2, dot_df2, conn2)
        self.play(tracker2.animate.set_value(3.0), run_time=5, rate_func=linear)
        self.remove(area2, dot_f2, dot_df2, conn2)
        self.play(FadeOut(f2_g), FadeOut(df2_g), FadeOut(f2_l), FadeOut(df2_l), FadeOut(left_axes), FadeOut(right_axes), FadeOut(int_arrow), FadeOut(int_label))

        # Final quote
        final = VGroup(
            Text('"Integration is the art of', font_size=32),
            Text('accumulating infinite small pieces."', font_size=32),
            MathTex(r"\text{— Integral: Sum of Change}", color=YELLOW).scale(0.7)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=1.2)
        title = MathTex(r"\text{Visualizing } f(x) \rightarrow \int f(x)dx").to_edge(UP, buff=0.5)
        self.play(Write(title), Write(final), run_time=3)
        self.wait(2)

class IntegrationQuote(Scene):
    def construct(self):
        quote = VGroup(
            Text("Integration: Where we add up", font_size=36),
            Text("the whispers of change", font_size=36),
        ).arrange(DOWN, buff=0.2)
        author = Text("— From sum to substance", font_size=24, color=YELLOW).next_to(quote, DOWN, buff=0.5)
        self.play(Write(quote), run_time=2)
        self.play(Write(author))
        self.wait(3)