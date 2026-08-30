from manim import *
import numpy as np

class InclineFlow30Sec(Scene):
    def construct(self):
        base_len = 5.5
        height = 2.2
        interior = np.arctan(height / base_len)  # small angle ~21 deg
        
        origin = LEFT*3 + DOWN*1.5
        base_end = origin + RIGHT*base_len
        top = origin + UP*height

        base = Line(origin, base_end, color=WHITE, stroke_width=4)
        incline = Line(top, base_end, color=BLUE, stroke_width=10)
        left_wall = Line(origin, top, color=WHITE, stroke_width=2)
        left_wall.set_opacity(0.15)

        title = Text("Object on an Incline: Forces & Motion", font_size=30).to_edge(UP, buff=0.4)

        # FIXED ARC - small inside arc, not huge circle
        # Arc centered at base_end, from incline direction to base direction (small 21 deg)
        arc = Arc(radius=0.7, start_angle=PI - interior, angle=interior, color=YELLOW, stroke_width=6)
        arc.move_arc_center_to(base_end)
        
        # FIXED THETA - inside triangle, BELOW blue line, ABOVE white base
        # Blue line at LEFT*1.6 is UP*0.64, so UP*0.3 is well below it, inside
        theta_label = MathTex(r"\theta", color=YELLOW).scale(1.0)
        theta_label.move_to(base_end + LEFT*1.3 + UP*0.25)

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

        block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(start_pos)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Create(left_wall))
        self.play(Create(arc), Write(theta_label), run_time=0.8)
        self.play(FadeIn(block))
        self.wait(1)

        mg = Arrow(block.get_center(), block.get_center() + DOWN*1.0, color=WHITE, buff=0, stroke_width=5)
        mg_text = MathTex(r"mg", color=WHITE).scale(0.7).next_to(mg, RIGHT, buff=0.1)
        n_force = Arrow(block.get_center(), block.get_center() + norm*0.9, color=BLUE, buff=0, stroke_width=5)
        n_text = MathTex(r"N", color=BLUE).scale(0.7).next_to(n_force, UP, buff=0.1)
        incline_unit = (top - base_end) / np.linalg.norm(top - base_end)
        friction = Arrow(block.get_center(), block.get_center() + incline_unit*0.7, color=YELLOW, buff=0, stroke_width=5)
        f_text = MathTex(r"f", color=YELLOW).scale(0.7).next_to(friction, LEFT, buff=0.1)

        self.play(Create(mg), Write(mg_text), Create(n_force), Write(n_text), Create(friction), Write(f_text))
        self.wait(1.5)
        self.play(FadeOut(mg), FadeOut(mg_text), FadeOut(n_force), FadeOut(n_text), FadeOut(friction), FadeOut(f_text))

        tracker = ValueTracker(start_t)
        moving_block = always_redraw(lambda: Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(tracker.get_value()) + offset))
        self.add(moving_block)
        self.remove(block)
        self.play(tracker.animate.set_value(end_t), run_time=4.5, rate_func=rate_functions.ease_in_quad)
        self.remove(moving_block)

        final_block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(end_pos)
        self.add(final_block)

        eq = VGroup(MathTex(r"a = g(\sin\theta - \mu\cos\theta)", color=GREEN).scale(0.9),).to_edge(DOWN, buff=0.8)
        self.play(Write(eq))
        self.wait(2)
