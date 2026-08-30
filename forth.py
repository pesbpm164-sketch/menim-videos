from manim import *
import numpy as np

class InclineFlow30Sec(Scene):
    def construct(self):
        base_len = 5.5
        height = 2.2
        interior_angle = np.arctan(height / base_len)
        
        origin = LEFT*3 + DOWN*1.5
        base_end = origin + RIGHT*base_len
        top = origin + UP*height

        base = Line(origin, base_end, color=WHITE, stroke_width=4)
        incline = Line(top, base_end, color=BLUE, stroke_width=10)
        left_wall = Line(origin, top, color=WHITE, stroke_width=2)
        left_wall.set_opacity(0.2)  # FIXED: was opacity= - now set_opacity

        title = Text("Object on an Incline: Forces & Motion", font_size=30).to_edge(UP, buff=0.4)

        arc = Arc(radius=0.6, start_angle=PI, angle=interior_angle, color=YELLOW, stroke_width=3).move_arc_center_to(base_end)
        theta_label = MathTex(r"\theta", color=YELLOW).scale(0.8).move_to(base_end + LEFT*1.0 + UP*0.35)

        block_size = 0.6
        incline_angle = np.arctan2(-height, base_len)

        def point_on_incline(t):
            return top + (base_end - top) * t

        norm = np.array([height, base_len, 0])
        norm = norm / np.linalg.norm(norm)
        offset = norm * 0.32

        start_t = 0.12
        end_t = 0.82
        start_pos = point_on_incline(start_t) + offset
        end_pos = point_on_incline(end_t) + offset

        block = Square(side_length=block_size, color=RED, fill_opacity=0.9)
        block.rotate(incline_angle)
        block.move_to(start_pos)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Create(left_wall), Create(arc), Write(theta_label), run_time=1.5)
        self.play(FadeIn(block))
        self.wait(1)

        mg = Arrow(block.get_center(), block.get_center() + DOWN*1.0, color=WHITE, buff=0, stroke_width=5)
        mg_text = MathTex(r"mg", color=WHITE).scale(0.7).next_to(mg, RIGHT, buff=0.1)

        n_force = Arrow(block.get_center(), block.get_center() + norm*0.9, color=BLUE, buff=0, stroke_width=5)
        n_text = MathTex(r"N=mg\cos\theta", color=BLUE).scale(0.55).next_to(n_force, UP, buff=0.1)

        incline_unit = (top - base_end) / np.linalg.norm(top - base_end)
        friction = Arrow(block.get_center(), block.get_center() + incline_unit*0.7, color=YELLOW, buff=0, stroke_width=5)
        f_text = MathTex(r"f=\mu N", color=YELLOW).scale(0.6).next_to(friction, LEFT, buff=0.15)

        self.play(Create(mg), Write(mg_text), Create(n_force), Write(n_text), Create(friction), Write(f_text))
        self.wait(1.5)
        self.play(FadeOut(mg), FadeOut(mg_text), FadeOut(n_force), FadeOut(n_text), FadeOut(friction), FadeOut(f_text))

        tracker = ValueTracker(start_t)

        moving_block = always_redraw(lambda: Square(side_length=block_size, color=RED, fill_opacity=0.9)
                                     .rotate(incline_angle)
                                     .move_to(point_on_incline(tracker.get_value()) + offset))

        self.add(moving_block)
        self.remove(block)
        self.play(tracker.animate.set_value(end_t), run_time=4.5, rate_func=rate_functions.ease_in_quad)
        self.remove(moving_block)

        final_block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(end_pos)
        self.add(final_block)

        eq = VGroup(
            MathTex(r"mg\sin\theta - f = ma", color=YELLOW).scale(0.8),
            MathTex(r"a = g(\sin\theta - \mu\cos\theta)", color=GREEN).scale(0.8),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)

        self.play(Write(eq))
        self.wait(2)
        self.play(FadeOut(base), FadeOut(incline), FadeOut(left_wall), FadeOut(final_block), FadeOut(arc), FadeOut(theta_label), FadeOut(title), FadeOut(eq))

        quote = VGroup(
            Text('"On an incline, gravity always', font_size=30),
            Text('finds a component to pull you down."', font_size=30),
        ).arrange(DOWN, buff=0.2)
        self.play(Write(quote), run_time=2)
        self.wait(2)
