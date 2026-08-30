from manim import *
import numpy as np

class DetailedInclineSimulation(Scene):
    def construct(self):
        base_len = 4.5
        height = 2.0
        interior = np.arctan(height / base_len)
        
        origin = LEFT*0.5 + DOWN*1.8
        base_end = origin + RIGHT*base_len
        top = origin + UP*height

        base = Line(origin, base_end, color=WHITE, stroke_width=4)
        incline = Line(top, base_end, color=BLUE, stroke_width=10)
        left_wall = Line(origin, top, color=WHITE, stroke_width=2)
        left_wall.set_opacity(0.15)

        title = Text("Object on an Inclined Plane", font_size=32).to_edge(UP, buff=0.4)

        arc = Arc(radius=0.5, start_angle=PI - interior, angle=interior, color=YELLOW, stroke_width=4)
        arc.move_arc_center_to(base_end)
        theta_label = MathTex(r"\theta", color=YELLOW).scale(0.8).move_to(base_end + LEFT*0.9 + UP*0.2)

        block_size = 0.55
        incline_angle = np.arctan2(-height, base_len)
        def point_on_incline(t):
            return top + (base_end - top) * t
        norm = np.array([height, base_len, 0])
        norm = norm / np.linalg.norm(norm)
        offset = norm * 0.30
        start_pos = point_on_incline(0.15) + offset

        block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(start_pos)

        # LEFT LIST - color matched
        legend = VGroup(
            MathTex(r"\vec{W}=mg", color=WHITE).scale(0.8),
            MathTex(r"mg\sin\theta", color=ORANGE).scale(0.8),
            MathTex(r"mg\cos\theta", color=GREEN).scale(0.8),
            MathTex(r"\vec{N}=mg\cos\theta", color=BLUE).scale(0.8),
            MathTex(r"\vec{f}_k=\mu_k N", color=YELLOW).scale(0.8),
            MathTex(r"F_{net}=mg\sin\theta-f_k", color=WHITE).scale(0.6),
            MathTex(r"a=g(\sin\theta-\mu_k\cos\theta)", color=PINK).scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.5).shift(DOWN*0.3)

        legend_box = SurroundingRectangle(legend, color=WHITE, buff=0.25, stroke_width=1.5, stroke_opacity=0.4, corner_radius=0.1)

        self.play(Write(title))
        self.play(Create(base), Create(incline), Create(left_wall), Create(arc), Write(theta_label), FadeIn(block), run_time=1.2)
        self.play(Create(legend_box), Write(legend), run_time=1.5)

        # BIG arrows for explanation (first image - bigger)
        incline_unit = (base_end - top) / np.linalg.norm(base_end - top)
        perp_unit = -norm

        mg_big = Arrow(block.get_center(), block.get_center() + DOWN*1.6, color=WHITE, buff=0, stroke_width=8)
        mg_parallel_big = DashedLine(block.get_center(), block.get_center() + incline_unit*1.2, color=ORANGE, stroke_width=6, dash_length=0.12)
        mg_parallel_big.add_tip(tip_length=0.2)
        mg_perp_big = DashedLine(block.get_center(), block.get_center() + perp_unit*1.1, color=GREEN, stroke_width=6, dash_length=0.12)
        mg_perp_big.add_tip(tip_length=0.2)
        n_big = Arrow(block.get_center(), block.get_center() + norm*1.2, color=BLUE, buff=0, stroke_width=8)
        f_big = Arrow(block.get_center(), block.get_center() - incline_unit*1.0, color=YELLOW, buff=0, stroke_width=8)

        dotted_h = DashedLine(block.get_center() + incline_unit*1.2, block.get_center() + incline_unit*1.2 + perp_unit*1.1, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.3)
        dotted_v = DashedLine(block.get_center() + perp_unit*1.1, block.get_center() + incline_unit*1.2 + perp_unit*1.1, color=WHITE, stroke_width=2, dash_length=0.08, stroke_opacity=0.3)

        self.play(Create(mg_big), Create(mg_parallel_big), Create(mg_perp_big), Create(n_big), Create(f_big), Create(dotted_h), Create(dotted_v), run_time=2)
        self.wait(1.5)

        # SMALL arrows for sliding (second image - smaller, intuitive)
        mg_small = Arrow(block.get_center(), block.get_center() + DOWN*1.1, color=WHITE, buff=0, stroke_width=6)
        mg_parallel_small = DashedLine(block.get_center(), block.get_center() + incline_unit*0.8, color=ORANGE, stroke_width=5, dash_length=0.1)
        mg_parallel_small.add_tip(tip_length=0.15)
        mg_perp_small = DashedLine(block.get_center(), block.get_center() + perp_unit*0.7, color=GREEN, stroke_width=5, dash_length=0.1)
        mg_perp_small.add_tip(tip_length=0.15)
        n_small = Arrow(block.get_center(), block.get_center() + norm*0.8, color=BLUE, buff=0, stroke_width=6)
        f_small = Arrow(block.get_center(), block.get_center() - incline_unit*0.6, color=YELLOW, buff=0, stroke_width=6)

        # SMOOTH SHRINK - no jerk, animate big -> small
        self.play(
            Transform(mg_big, mg_small),
            Transform(mg_parallel_big, mg_parallel_small),
            Transform(mg_perp_big, mg_perp_small),
            Transform(n_big, n_small),
            Transform(f_big, f_small),
            FadeOut(dotted_h), FadeOut(dotted_v),
            run_time=1.2, rate_func=smooth
        )
        self.wait(0.5)

        # Now switch to always_redraw with SAME small size - no jerk
        tracker = ValueTracker(0.15)
        moving_block = always_redraw(lambda: Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(tracker.get_value()) + offset))
        moving_mg = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + DOWN*1.1, color=WHITE, buff=0, stroke_width=6, stroke_opacity=0.9))
        moving_parallel = always_redraw(lambda: DashedLine(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + incline_unit*0.8, color=ORANGE, stroke_width=5, dash_length=0.1, stroke_opacity=0.9).add_tip(tip_length=0.15))
        moving_perp = always_redraw(lambda: DashedLine(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + perp_unit*0.7, color=GREEN, stroke_width=5, dash_length=0.1, stroke_opacity=0.9).add_tip(tip_length=0.15))
        moving_n = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset + norm*0.8, color=BLUE, buff=0, stroke_width=6, stroke_opacity=0.9))
        moving_f = always_redraw(lambda: Arrow(point_on_incline(tracker.get_value()) + offset, point_on_incline(tracker.get_value()) + offset - incline_unit*0.6, color=YELLOW, buff=0, stroke_width=6, stroke_opacity=0.9))

        self.add(moving_block, moving_mg, moving_parallel, moving_perp, moving_n, moving_f)
        self.remove(block, mg_big, mg_parallel_big, mg_perp_big, n_big, f_big)

        # Smooth slide - no lag
        self.play(tracker.animate.set_value(0.78), run_time=5, rate_func=rate_functions.ease_in_quad)
        self.remove(moving_block, moving_mg, moving_parallel, moving_perp, moving_n, moving_f)

        final_block = Square(side_length=block_size, color=RED, fill_opacity=0.9).rotate(incline_angle).move_to(point_on_incline(0.78) + offset)
        self.add(final_block)
        self.wait(1.5)
