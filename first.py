from manim import *
import numpy as np

class SinWave(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 1],
            axis_config={"color": WHITE},
            x_length=10, y_length=4
        )
        labels = axes.get_axis_labels(x_label="x", y_label="y = sin x")

        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE, x_range=[-2*PI, 2*PI])
        formula = MathTex(r"y = \sin x").to_edge(UP).set_color(BLUE)
        deriv = MathTex(r"\frac{d}{dx}\sin x = \cos x").next_to(formula, DOWN).set_color(YELLOW)

        self.play(Create(axes), Write(labels))
        self.play(Create(sin_graph), Write(formula))
        self.play(Write(deriv))
        self.wait(2)

class CosWave(Scene):
    def construct(self):
        axes = Axes(x_range=[-2*PI, 2*PI, PI/2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED, x_range=[-2*PI, 2*PI])
        formula = MathTex(r"y = \cos x").to_edge(UP).set_color(RED)
        deriv = MathTex(r"\frac{d}{dx}\cos x = -\sin x").next_to(formula, DOWN)

        self.play(Create(axes))
        self.play(Create(cos_graph), Write(formula), Write(deriv))
        self.wait(2)

class UnitCircleDerivation(Scene):
    def construct(self):
        # Unit circle showing where sin and cos come from
        circle = Circle(radius=2, color=WHITE)
        dot = Dot(color=YELLOW).move_to(circle.point_at_angle(0))

        radius = Line(ORIGIN, dot.get_center(), color=YELLOW)
        x_line = DashedLine(dot.get_center(), [dot.get_center()[0], 0, 0], color=RED)
        y_line = DashedLine(dot.get_center(), [0, dot.get_center()[1], 0], color=BLUE)

        theta_label = MathTex(r"\theta").next_to(ORIGIN, RIGHT, buff=0.3)
        sin_label = MathTex(r"\sin\theta", color=BLUE).next_to(y_line, LEFT)
        cos_label = MathTex(r"\cos\theta", color=RED).next_to(x_line, DOWN)
        identity = MathTex(r"\sin^2\theta + \cos^2\theta = 1").to_edge(UP)

        self.play(Create(circle), Write(identity))
        self.play(Create(radius), Create(x_line), Create(y_line), Create(dot))
        self.play(Write(theta_label), Write(sin_label), Write(cos_label))

        # animate around circle
        self.play(MoveAlongPath(dot, circle), Rotate(radius, 2*PI, about_point=ORIGIN), run_time=6, rate_func=linear)
        self.wait(1)

class AllTrigWaves(Scene):
    def construct(self):
        axes = Axes(x_range=[-2*PI, 2*PI, PI], y_range=[-2, 2, 1], x_length=10, y_length=5)

        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE, x_range=[-2*PI, 2*PI])
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED, x_range=[-2*PI, 2*PI])
        # tan with breaks
        tan_graph = axes.plot(lambda x: np.tan(x) if abs(np.cos(x))>0.15 else np.nan,
                              color=GREEN, x_range=[-2*PI, 2*PI], discontinuities=[-3*PI/2, -PI/2, PI/2, 3*PI/2])

        legend = VGroup(
            MathTex(r"\sin x", color=BLUE),
            MathTex(r"\cos x", color=RED),
            MathTex(r"\tan x", color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UR)

        self.play(Create(axes))
        self.play(Create(sin_graph), Create(cos_graph), Create(tan_graph), Write(legend))
        self.wait(2)
