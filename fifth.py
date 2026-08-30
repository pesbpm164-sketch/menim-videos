from manim import *
import numpy as np

class SimplePendulumSimulation(Scene):
    def construct(self):
        # Pivot on top center-right
        pivot = UP*2.0 + RIGHT*1.5
        L = 3.0
        theta0 = 30 * DEGREES  # initial angle
        g = 9.8
        omega = np.sqrt(g / L)

        title = Text("Simple Pendulum", font_size=32).to_edge(UP, buff=0.4)
        
        # Ground / ceiling
        ceiling = Line(pivot + LEFT*2, pivot + RIGHT*2, color=WHITE, stroke_width=3)
        pivot_dot = Dot(pivot, color=WHITE, radius=0.08)

        # LEFT LIST - color matched, no overlap
        legend = VGroup(
            MathTex(r"\vec{W}=mg", color=WHITE).scale(0.85),
            MathTex(r"mg\sin\theta", color=ORANGE).scale(0.85),
            MathTex(r"mg\cos\theta", color=GREEN).scale(0.85),
            MathTex(r"\vec{T}= \text{tension}", color=BLUE).scale(0.85),
            MathTex(r"F_{restoring}=-mg\sin\theta", color=YELLOW).scale(0.65),
            MathTex(r"a=-g\sin\theta", color=WHITE).scale(0.7),
            MathTex(r"T_{period}=2\pi\sqrt{L/g}", color=GREEN).scale(0.65),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.5).shift(DOWN*0.2)
        legend_box = SurroundingRectangle(legend, color=WHITE, buff=0.25, stroke_width=1.5, stroke_opacity=0.4, corner_radius=0.1)

        self.play(Write(title), Create(ceiling), FadeIn(pivot_dot))
        self.play(Create(legend_box), Write(legend), run_time=1.5)

        # Angle tracker for smooth oscillation
        time_tracker = ValueTracker(0)

        def get_theta():
            # Simple harmonic approx: theta = theta0 * cos(omega*t)
            return theta0 * np.cos(omega * time_tracker.get_value())

        def bob_position(theta):
            return pivot + RIGHT * L * np.sin(theta) + DOWN * L * np.cos(theta)

        # Always redraw components
        string = always_redraw(lambda: Line(pivot, bob_position(get_theta()), color=WHITE, stroke_width=4))
        bob = always_redraw(lambda: Dot(bob_position(get_theta()), color=RED, radius=0.25).set_fill(RED, opacity=0.9))

        # Arc for angle
        arc = always_redraw(lambda: Arc(radius=0.5, start_angle=-90*DEGREES, angle=get_theta(), color=YELLOW, stroke_width=3).move_arc_center_to(pivot))
        theta_label = always_redraw(lambda: MathTex(r"\theta", color=YELLOW).scale(0.7).move_to(pivot + DOWN*0.8 + RIGHT*0.3*np.sign(get_theta()) if abs(get_theta())>0.1 else pivot+DOWN*0.8))

        # Forces - color matched to legend
        # Weight mg - white down
        mg_arrow = always_redraw(lambda: Arrow(bob_position(get_theta()), bob_position(get_theta()) + DOWN*1.2, color=WHITE, buff=0, stroke_width=6))
        # Tension T - blue along string up to pivot
        tension_arrow = always_redraw(lambda: Arrow(bob_position(get_theta()), bob_position(get_theta()) + (pivot - bob_position(get_theta()))/L * 1.0, color=BLUE, buff=0, stroke_width=6))
        # mg cos - green along string down (radial component)
        mg_cos_arrow = always_redraw(lambda: DashedLine(bob_position(get_theta()), bob_position(get_theta()) + (bob_position(get_theta()) - pivot)/L * 0.8, color=GREEN, stroke_width=5, dash_length=0.1).add_tip(tip_length=0.15))
        # mg sin - orange perpendicular to string (tangential restoring)
        def perp_dir(theta):
            # Perpendicular to string, towards equilibrium
            # String direction vector
            return np.array([-np.cos(theta), -np.sin(theta), 0])  # tangential
        mg_sin_arrow = always_redraw(lambda: DashedLine(bob_position(get_theta()), bob_position(get_theta()) + perp_dir(get_theta())*0.8*np.sin(get_theta()), color=ORANGE, stroke_width=5, dash_length=0.1).add_tip(tip_length=0.15))

        self.play(Create(string), FadeIn(bob), Create(arc), Write(theta_label), run_time=1)
        self.play(Create(mg_arrow), Create(tension_arrow), Create(mg_cos_arrow), Create(mg_sin_arrow), run_time=1.5)
        self.wait(1)

        # Smooth oscillation - no jerk
        self.play(time_tracker.animate.set_value(10), run_time=10, rate_func=linear)

        self.wait(1)

class PendulumDerivation(Scene):
    def construct(self):
        title = Text("Pendulum Equation via Integration", font_size=28).to_edge(UP)
        self.play(Write(title))

        eqs = VGroup(
            MathTex(r"\tau = I \alpha = -mgL\sin\theta", color=YELLOW).scale(0.9),
            MathTex(r"mL^2 \frac{d^2\theta}{dt^2} = -mgL\sin\theta", color=WHITE).scale(0.85),
            MathTex(r"\frac{d^2\theta}{dt^2} + \frac{g}{L}\sin\theta = 0", color=BLUE).scale(0.9),
            MathTex(r"\text{Small angle: } \sin\theta \approx \theta", color=GRAY).scale(0.75),
            MathTex(r"\frac{d^2\theta}{dt^2} + \frac{g}{L}\theta = 0", color=GREEN).scale(0.9),
            MathTex(r"\theta(t)=\theta_0\cos(\omega t), \quad \omega=\sqrt{g/L}", color=YELLOW).scale(0.85),
            MathTex(r"T = 2\pi\sqrt{L/g}", color=ORANGE).scale(0.9),
        ).arrange(DOWN, buff=0.4).center()

        for eq in eqs:
            self.play(Write(eq), run_time=1)
            self.wait(0.5)
        self.wait(2)
