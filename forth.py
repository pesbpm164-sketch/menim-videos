from manim import *
import numpy as np

class InclineFlow30Sec(Scene):
    def construct(self):
        theta = 30 * DEGREES
        sin_t = np.sin(theta)
        cos_t = np.cos(theta)

        # Incline setup
        base = Line(LEFT*4 + DOWN*2, RIGHT*3 + DOWN*2, color=WHITE)
        incline = Line(LEFT*4 + UP*1, RIGHT*3 + DOWN*2, color=BLUE, stroke_width=8)

        title = Text("Object on an Incline: Forces & Motion", font_size=32).to_edge(UP, buff=0.4)

        # Block starting at top
        block = Square(side_length=0.5, color=RED, fill_opacity=0.9).rotate(-theta)
        start_pos = LEFT*3 + UP*0.3
        end_pos = RIGHT*1.5 + DOWN*1.4
        block.move_to(start_pos)

        # Angle
        angle_label = MathTex(r"\theta", color=YELLOW).scale(0.8).move_to(RIGHT*2 + DOWN*1.3)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Write(angle_label), run_time=1.5)
        self.play(FadeIn(block))
        self.wait(1)

        # Show forces at start
        mg = Arrow(block.get_center(), block.get_center() + DOWN*1.2, color=WHITE, buff=0, stroke_width=4)
        mg_text = MathTex(r"mg", color=WHITE).next_to(mg, RIGHT, buff=0.1).scale(0.6)

        n_force = Arrow(block.get_center(), block.get_center() + UP*1.0*cos_t + RIGHT*1.0*sin_t, color=BLUE, buff=0, stroke_width=4)
        n_text = MathTex(r"N=mg\cos\theta", color=BLUE).next_to(n_force, UP, buff=0.1).scale(0.5)

        friction = Arrow(block.get_center(), block.get_center() + LEFT*0.8*cos_t + UP*0.8*sin_t, color=YELLOW, buff=0, stroke_width=4)
        f_text = MathTex(r"f=\mu N", color=YELLOW).next_to(friction, LEFT, buff=0.1).scale(0.5)

        self.play(Create(mg), Write(mg_text), Create(n_force), Write(n_text), Create(friction), Write(f_text))
        self.wait(1.5)
        self.play(FadeOut(mg), FadeOut(mg_text), FadeOut(n_force), FadeOut(n_text), FadeOut(friction), FadeOut(f_text))

        # Slide animation with tracker
        tracker = ValueTracker(0)

        # Block sliding along incline direction
        def get_pos(alpha):
            return start_pos + (end_pos - start_pos) * alpha

        moving_block = always_redraw(lambda: Square(side_length=0.5, color=RED, fill_opacity=0.9).rotate(-theta).move_to(get_pos(tracker.get_value())))

        # Velocity arrow that grows
        vel_arrow = always_redraw(lambda: Arrow(
            get_pos(tracker.get_value()),
            get_pos(tracker.get_value()) + RIGHT*0.5*tracker.get_value()*cos_t + DOWN*0.5*tracker.get_value()*sin_t,
            color=GREEN, buff=0, stroke_width=3
        ).shift(RIGHT*0.3))

        self.add(moving_block, vel_arrow)
        self.remove(block)
        self.play(tracker.animate.set_value(1), run_time=5, rate_func=rate_functions.ease_in_quad)
        self.wait(1)
        self.remove(moving_block, vel_arrow)

        final_block = Square(side_length=0.5, color=RED, fill_opacity=0.9).rotate(-theta).move_to(end_pos)
        self.add(final_block)

        # Final equations
        eq = VGroup(
            MathTex(r"mg\sin\theta - f = ma", color=YELLOW).scale(0.8),
            MathTex(r"a = g(\sin\theta - \mu\cos\theta)", color=GREEN).scale(0.8),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.8)

        self.play(Write(eq))
        self.wait(2)

        self.play(FadeOut(base), FadeOut(incline), FadeOut(final_block), FadeOut(angle_label), FadeOut(title), FadeOut(eq))

        # Quote
        quote = VGroup(
            Text('"On an incline, gravity always', font_size=32),
            Text('finds a component to pull you down."', font_size=32),
            MathTex(r"\text{— Physics of Sliding}", color=YELLOW).scale(0.7)
        ).arrange(DOWN, buff=0.3)

        self.play(Write(quote), run_time=2)
        self.wait(2)

class InclineWithFriction(Scene):
    def construct(self):
        theta = 35 * DEGREES
        incline = Line(LEFT*4 + UP*1, RIGHT*3 + DOWN*2, color=BLUE, stroke_width=8)
        base = Line(LEFT*4 + DOWN*2, RIGHT*3 + DOWN*2, color=WHITE)
        block = Square(0.5, color=RED, fill_opacity=0.9).rotate(-theta).move_to(LEFT*1 + DOWN*0.2)

        forces = VGroup(
            MathTex(r"mg\sin\theta", color=ORANGE).scale(0.6),
            MathTex(r"mg\cos\theta", color=GREEN).scale(0.6),
            MathTex(r"N", color=BLUE).scale(0.6),
            MathTex(r"f_s = \mu_s N", color=YELLOW).scale(0.6),
        ).arrange(DOWN, buff=0.2).to_edge(UR, buff=0.5)

        self.play(Create(incline), Create(base), FadeIn(block), Write(forces))
        self.wait(3)